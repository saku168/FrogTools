import os, platform, socket, subprocess, secrets, string, datetime, urllib.request, urllib.parse

GREEN = "\033[92m"
RESET = "\033[0m"
REPORTS = "reports"

def run_cmd(args):
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=15).stdout
    except Exception as e:
        return f"Erreur: {e}"

def banner():
    print("\n  (•ᴗ•)  FrogTools")
    print("  Outils pratiques en ligne de commande\n")

def help_menu():
    print("""Commandes:
  help             Affiche cette liste
  network          Infos réseau locales
  ping <hôte>      Test de connectivité
  dns <nom>        Résolution DNS
  trace <hôte>     Traceroute/tracert
  system           Informations système
  whoami           Utilisateur actuel
  headers <URL>    En-têtes HTTP d'une URL
  password [len]   Mot de passe aléatoire
  report           Sauvegarde un rapport local
  clear            Efface l'écran
  exit             Quitte
""")

def network():
    print("Nom de machine:", socket.gethostname())
    try: print("IP locale:", socket.gethostbyname(socket.gethostname()))
    except Exception as e: print("IP locale indisponible:", e)
    print(run_cmd(["ipconfig"] if os.name == "nt" else ["ifconfig"]))

def ping(host):
    if not host or any(c in host for c in ";&|<>$"):
        print("Usage: ping nom-hôte-ou-IP"); return
    count = "-n" if os.name == "nt" else "-c"
    print(run_cmd(["ping", count, "4", host]))

def dns(name):
    if not name or any(c in name for c in ";&|<>$"):
        print("Usage: dns nom-de-domaine"); return
    try:
        for item in socket.getaddrinfo(name, None): print(item[4][0])
    except Exception as e: print("DNS:", e)

def trace(host):
    if not host or any(c in host for c in ";&|<>$"):
        print("Usage: trace nom-hôte-ou-IP"); return
    cmd = ["tracert", "-d", host] if os.name == "nt" else ["traceroute", "-n", host]
    print(run_cmd(cmd))

def system():
    print("OS:", platform.platform())
    print("Python:", platform.python_version())
    print("Machine:", platform.machine())
    print("Processeur:", platform.processor() or "non renseigné")

def headers(url):
    try:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            print("URL invalide (http/https requis)."); return
        req = urllib.request.Request(url, headers={"User-Agent":"FrogTools/1.0"}, method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as res:
            print("Statut:", res.status)
            for k,v in res.headers.items(): print(f"{k}: {v}")
    except Exception as e: print("Requête impossible:", e)

def password(length=20):
    try: length = max(8, min(128, int(length)))
    except ValueError: length = 20
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    print("Mot de passe:", ''.join(secrets.choice(alphabet) for _ in range(length)))

def report():
    os.makedirs(REPORTS, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(REPORTS, f"rapport-{stamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"FrogTools report - {datetime.datetime.now()}\n")
        f.write(f"OS: {platform.platform()}\nHost: {socket.gethostname()}\n")
        try: f.write(f"IP: {socket.gethostbyname(socket.gethostname())}\n")
        except Exception: pass
    print("Rapport créé:", path)

def main():
    banner()
    print("Tapez help pour afficher les commandes.")
    while True:
        try: line = input(f"{GREEN}frog>{RESET} ").strip()
        except (KeyboardInterrupt, EOFError): print(); break
        parts = line.split()
        if not parts: continue
        cmd, args = parts[0].lower(), parts[1:]
        if cmd == "help": help_menu()
        elif cmd == "network": network()
        elif cmd == "ping": ping(args[0] if args else "")
        elif cmd == "dns": dns(args[0] if args else "")
        elif cmd == "trace": trace(args[0] if args else "")
        elif cmd == "system": system()
        elif cmd == "whoami": print(run_cmd(["whoami"]))
        elif cmd == "headers": headers(args[0] if args else "")
        elif cmd == "password": password(args[0] if args else 20)
        elif cmd == "report": report()
        elif cmd == "clear": os.system("cls" if os.name == "nt" else "clear")
        elif cmd in ("exit", "quit"): break
        else: print("Commande inconnue. Tapez help.")
if __name__ == "__main__": main()
