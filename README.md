# Multi-threaded Chat Service mit festen Räumen

Dieses Projekt implementiert einen **multi-threaded Chat-Service** in Python auf Basis von TCP-Sockets.  
Mehrere Clients können sich gleichzeitig mit dem Server verbinden und in **vordefinierten Chat-Räumen** kommunizieren.

Die Anwendung besteht aus zwei Skripten:
- `server.py` – Chat-Server
- `client.py` – Konsolen-Client

---

## Funktionen

- Multi-threaded Server (ein Thread pro Client)
- Gleichzeitige Verbindung mehrerer Clients
- Feste Chat-Räume:
  - `lobby` (Standardraum)
  - `work`
  - `support`
  - `team`
- Nachrichten werden nur innerhalb des gleichen Raums gesendet
- Raumwechsel per Befehl
- Saubere Trennung zwischen Server und Client

---

## Voraussetzungen

- Python **3.9 oder neuer**
- Keine zusätzlichen Python-Bibliotheken notwendig
- Getestet unter macOS und Linux

---

## Schritt 1: Server starten

1. Öffne ein Terminal
2. Wechsle in das Projektverzeichnis
3. Starte den Server mit folgendem Befehl:

```bash
python3 server.py

## Erwartete Ausgabe 
Server started on 127.0.0.1:6321
```
---

## Client Starten

1. Öffne ein neuer Terminal
2. wechsle erneut in das Projetverzeichnis
3. Starte den Client mit:

```bash
python3 client.py
```
4. Gib einen Benutzernamen ein:

```bash
Enter your name:
```

## Schritt 3: mehrere Clients verbinden

- Wiederhole Schritt 2 in weiteren Terminals
- Jeder gestartete Client verbindet sich mit dem gleichen Server
- Der Server verarbeitet jeden Client in einem eigenen Thread

## Chat Befehle

Innerhalb des Chats stehen folgende Befehle zur Verfügung:

```bash
| Befehl        | Beschreibung                               |
|---------------|--------------------------------------------|
| `/rooms`      | Zeigt alle verfügbaren Chat-Räume          |
| `/join lobby` | Wechsel in den Raum `lobby`                |
| `/join work`  | Wechsel in den Raum `work`                 |
| `/join support` | Wechsel in den Raum `support`            |
| `/join team`  | Wechsel in den Raum `team`                 |
| `bye`         | Beendet die Verbindung zum Server          |
```

## Standardverhalten
- Jeder Client startet automatisch im Raum lobby
- Nachrichten werden nur an Clients im gleichen Raum gesendet
- Eigene Nachrichten werden ebenfalls vom Server zurückgesendet

## Beenden der Anwendung
- Client beenden:
Im Chat bye eingeben
- Server beenden:
Im Server-Terminal CTRL + C drücken




