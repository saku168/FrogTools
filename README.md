# FrogTools

A small terminal toolkit for everyday diagnostics and utilities.

## Start
```sh
python frogtools.py
```
Use `help` in the prompt to see the command list.

## Commands
- `network`: basic local network information
- `ping <host>`, `dns <domain>`, `trace <host>`: connectivity diagnostics
- `system`, `whoami`: local system info
- `headers <URL>`, `httpcheck <URL>`: basic web response checks
- `calc <expression>`: simple arithmetic
- `hash <text>`: SHA-256 digest
- `encode <text>`, `decode <text>`: Base64 utilities
- `password [length]`: random password
- `uuid`, `date`, `report`, `clear`, `about`

## Build on Windows
Run `build.bat` to create `dist/FrogTools.exe`, or use the GitHub Actions workflow and download the artifact.

Only use diagnostics on networks and systems you have permission to test.
