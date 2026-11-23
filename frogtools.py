import os, platform, socket, subprocess, secrets, string, datetime, urllib.request, urllib.parse, hashlib, base64, uuid, ast, operator

G = "\033[92m"; C = "\033[96m"; Y = "\033[93m"; R = "\033[0m"; DIM = "\033[2m"
REPORTS = "reports"
OPS = {ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul, ast.Div:operator.truediv, ast.FloorDiv:operator.floordiv, ast.Mod:operator.mod, ast.Pow:operator.pow, ast.USub:operator.neg, ast.UAdd:operator.pos}

def safe_calc(expr):
    tree=ast.parse(expr, mode="eval")
    def walk(n):
        if isinstance(n, ast.Expression): return walk(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            if isinstance(n.op,ast.Pow) and abs(walk(n.right))>8: raise ValueError("Puissance trop grande.")
            return OPS[type(n.op)](walk(n.left),walk(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](walk(n.operand))
        raise ValueError("Expression non autorisée.")
    return walk(tree)

def banner():
    print(G + "  __    __                 _____           _\n / _|  / _|               | Tools |__  __| |\n| |_  | |_   Frog         | Frog / _|/ _` |\n|  _| |  _|               |____/\\__|\\__,_|\n" + R)
    print(DIM+"  Toolkit local • diagnostics & utilitaires"+R)

def help_menu():
    print(C+"\n COMMANDES"+R)
    print("""  help                  Liste des commandes
  network                Informations réseau de base
  ping <hôte>            Test de connexion
  dns <nom>              Résolution DNS
  trace <hôte>           Traceroute
  system                 Infos système
  whoami                 Compte Windows
  headers <URL>          En-têtes HTTP d'un site
  httpcheck <URL>         Vérifier réponse d'une URL
  calc <expression>       Calculatrice
  hash <texte>            SHA-256 d'un texte
  encode <texte>           Encode en Base64
  decode <texte>           Decode Base64
  password [longueur]     Générer un mot de passe
  uuid                    Créer un UUID
  date                    Afficher date et heure
  report                  Créer un rapport local
  clear                   Nettoyer le terminal
  about                   À propos
  exit                    Quitter
""")

def run_cmd(args):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=15)
        return p.stdout or p.stderr or "(aucune sortie)"
    except Exception as e: return f"Erreur: {e}"

def network():
    print("Machine:",socket.gethostname())
    try: print("IP locale:",socket.gethostbyname(socket.gethostname()))
    except Exception as e: print("IP locale indisponible:",e)
    print(run_cmd(["ipconfig"] if os.name=="nt" else ["ip","addr"]))

def validate_host(h):
    return bool(h) and not any(c in h for c in ";&|<>$'\\")

def ping(h):
    if not validate_host(h): print("Usage: ping nom-hôte"); return
    print(run_cmd(["ping","-n" if os.name=="nt" else "-c","4",h]))

def dns(name):
    if not validate_host(name): print("Usage: dns domaine"); return
    try:
        ips=sorted({x[4][0] for x in socket.getaddrinfo(name,None)})
        print("\n".join(ips))
    except Exception as e: print("DNS:",e)

def trace(h):
    if not validate_host(h): print("Usage: trace nom-hôte"); return
    cmd=["tracert","-d",h] if os.name=="nt" else ["traceroute","-n",h]
    print(run_cmd(cmd))

def system():
    print(f"OS       : {platform.platform()}\nPython   : {platform.python_version()}\nMachine  : {platform.machine()}\nCPU      : {platform.processor() or 'non renseigné'}")

def fetch(url, method="GET"):
    try:
        p=urllib.parse.urlparse(url)
        if p.scheme not in ("http","https") or not p.hostname: print("URL invalide (http/https)."); return
        req=urllib.request.Request(url,headers={"User-Agent":"FrogTools/1.0"},method=method)
        with urllib.request.urlopen(req,timeout=8) as res:
            print("Statut:",res.status, res.reason)
            if method=="HEAD":
                for k,v in res.headers.items(): print(f"{k}: {v}")
    except Exception as e: print("Requête:",e)

def password(length=20):
    try: length=max(8,min(128,int(length)))
    except ValueError: length=20
    chars=string.ascii_letters+string.digits+"!@#$%^&*()-_=+"
    print(''.join(secrets.choice(chars) for _ in range(length)))

def report():
    os.makedirs(REPORTS,exist_ok=True)
    path=os.path.join(REPORTS,"rapport-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt")
    with open(path,"w",encoding="utf-8") as f:
        f.write("FrogTools report\n"+str(datetime.datetime.now())+"\n")
        f.write("OS: "+platform.platform()+"\nHost: "+socket.gethostname()+"\n")
        try: f.write("IP: "+socket.gethostbyname(socket.gethostname())+"\n")
        except Exception: pass
    print("Rapport enregistré:",path)


def disk():
    print(run_cmd(["wmic","logicaldisk","get","caption,freespace,size"] if os.name=="nt" else ["df","-h"]))

def processes():
    print(run_cmd(["tasklist"] if os.name=="nt" else ["ps","-eo","pid,comm,%cpu,%mem"]))

def ports():
    print(run_cmd(["netstat","-ano"] if os.name=="nt" else ["ss","-tuln"]))

def portcheck(arg):
    try:
        host,port=arg.rsplit(":",1)
        port=int(port)
        if not validate_host(host) or not 1<=port<=65535: raise ValueError()
        with socket.create_connection((host,port),timeout=3):
            print(f"Port {port} accessible sur {host}")
    except Exception: print("Usage: portcheck hôte:port (test ponctuel)")

def open_download():
    url="https://github.com/saku168/FrogTools/releases"
    print("Page des versions:",url)
    try:
        if os.name=="nt": os.startfile(url)
        elif platform.system()=="Darwin": subprocess.Popen(["open",url])
        else: subprocess.Popen(["xdg-open",url])
    except Exception: print("Ouvre ce lien dans ton navigateur:",url)

\ndef main():
    os.system("")
    banner(); print("Tapez "+G+"help"+R+" pour voir les commandes.\n")
    while True:
        try: line=input(G+"frog"+R+DIM+" > "+R).strip()
        except (KeyboardInterrupt,EOFError): print(); break
        if not line: continue
        cmd,*args=line.split(maxsplit=1); cmd=cmd.lower(); arg=args[0] if args else ""
        if cmd=="help": help_menu()
        elif cmd=="network": network()
        elif cmd=="ping": ping(arg)
        elif cmd=="dns": dns(arg)
        elif cmd=="trace": trace(arg)
        elif cmd=="system": system()
        elif cmd=="whoami": print(run_cmd(["whoami"]))
        elif cmd=="headers": fetch(arg,"HEAD")
        elif cmd=="httpcheck": fetch(arg,"GET")
        elif cmd=="calc":
            try: print(safe_calc(arg))
            except Exception as e: print("Calcul invalide:",e)
        elif cmd=="hash": print(hashlib.sha256(arg.encode()).hexdigest() if arg else "Usage: hash texte")
        elif cmd=="encode": print(base64.b64encode(arg.encode()).decode() if arg else "Usage: encode texte")
        elif cmd=="decode":
            try: print(base64.b64decode(arg,validate=True).decode())
            except Exception: print("Base64 invalide.")
        elif cmd=="password": password(arg or 20)
        elif cmd=="uuid": print(uuid.uuid4())
        elif cmd=="date": print(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        elif cmd=="report": report()
        elif cmd=="clear": os.system("cls" if os.name=="nt" else "clear"); banner()
        elif cmd=="about": print("FrogTools v1.2 • Diagnostics & utilitaires\\nGitHub: https://github.com/saku168/FrogTools\\nTéléchargements: https://github.com/saku168/FrogTools/releases\\nCommande download: ouvre la page des versions.")
        elif cmd in ("exit","quit"): break
        else: print(Y+"Commande inconnue. Tapez help."+R)
if __name__=="__main__": main()
