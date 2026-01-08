# Multi-threaded Chat Service mit festen Räumen

Dieses Projekt implementiert einen **multi-threaded Chat-Service** in Python auf Basis von TCP-Sockets.  
Mehrere Clients können sich gleichzeitig mit dem Server verbinden und in **vordefinierten Chat-Räumen** kommunizieren.

Der Server lauscht auf einem **frei wählbaren TCP-Port**, der beim Start explizit angegeben wird.  
Clients verbinden sich über die **IP-Adresse des Servers** und den angegebenen Port.

Die Anwendung besteht aus zwei Skripten:
- `server.py` – Chat-Server
- `client.py` – Konsolen-Client

---

## Funktionen

- Multi-threaded Server (ein Thread pro Client)
- Gleichzeitige Verbindung mehrerer Clients
- Fester TCP-Port (per Startparameter)
- Feste Chat-Räume:
  - `lobby` (Standardraum)
  - `work`
  - `support`
  - `team`
- Nachrichten werden nur innerhalb des gleichen Raums gesendet
- Raumwechsel per Befehl
- Saubere Trennung zwischen Server- und Client-Logik

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
python3 server.py --port 1234

## Erwartete Ausgabe 
ChatServer started on 0.0.0.0:1234
```

### Hinweis:
	• Der Server bindet sich automatisch an alle lokalen Netzwerk-Interfaces (0.0.0.0)
	• Der Server ist erreichbar über 127.0.0.1 oder über die LAN-IP des Rechners
---

## Client Starten

1. Öffne ein neuer Terminal
2. wechsle erneut in das Projetverzeichnis
3. Starte den Client mit:

```bash
python3 client.py --ip 127.0.0.1 --port 1234
```
4. Gib anschliessend einen Benutzernamen ein:
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
| `/ls`         | Zeigt alle verfügbaren Chat-Räume          |
| `/cd lobby`   | Wechsel in den Raum `lobby`                |
| `/cd work`    | Wechsel in den Raum `work`                 |
| `/cd support` | Wechsel in den Raum `support`              |
| `/cd team`    | Wechsel in den Raum `team`                 |
| `/users`      | Zeigt alle verbundene User                 |
| `/server`     | Zeigt Serverinformationen und Benutzer an  |
| `/help`       | Listet alle verfügbaren Befehle auf        |
| `bye`         | Beendet die Verbindung zum Server          |
```

## Standardverhalten
- Jeder Client startet automatisch im Raum lobby
- Nachrichten werden nur an Clients im gleichen Raum gesendet
- Eigene Nachrichten werden ebenfalls vom Server zurückgesendet

## Beenden der Anwendung
	Client beenden:
	• Im Chat bye eingeben

	Server beenden:
	• Im Server-Terminal CTRL + C drücken

---

### Technische Erklärung des Codes

## server.py – Chat-Server

## Der Server stellt die zentrale Komponente des Systems dar und übernimmt folgende Aufgaben:
	• Erstellt einen TCP-Socket (IPv4)
	• Bindet sich automatisch an alle lokalen Interfaces (0.0.0.0)
	• Lauscht auf dem übergebenen TCP-Port (--port)
	• Wartet auf eingehende Client-Verbindungen (accept)
	• Erstellt für jeden verbundenen Client einen eigenen Thread
	• Verwaltet alle Clients in einer gemeinsamen Liste
	• Ordnet jedem Client einen festen Chat-Raum zu
	• Verarbeitet Chat-Befehle (/ls, /cd, /users, /server, /help)
	• Verteilt Nachrichten ausschliesslich an Clients im gleichen Raum
	• Entfernt Clients sauber bei Verbindungsabbruch oder bei bye

Der Server enthält die gesamte Anwendungslogik für Räume, Benutzer und Nachrichtenverteilung.

---

## client.py – Chat-Client

	Der Client stellt die Benutzeroberfläche im Terminal bereit und übernimmt folgende Aufgaben:
	• Liest Startparameter (--ip, --port) mittels argparse
	• Baut eine TCP-Verbindung zum angegebenen Server auf
	• Sendet beim Verbindungsaufbau den Benutzernamen
	• Startet einen separaten Thread zum Empfangen von Nachrichten
	• Liest Benutzereingaben aus dem Terminal
	• Sendet Nachrichten und Befehle an den Server
	• Gibt empfangene Nachrichten direkt im Terminal aus
	• Beendet die Verbindung sauber bei Eingabe von bye

Der Client enthält keine Anwendungslogik für Räume oder Benutzer –
diese liegt vollständig beim Server.

---

### Multi-Threading-Konzept

	Server
	• Ein Thread pro Client
	• Parallele Verarbeitung mehrerer Benutzer

	Client
	• Hauptthread für Benutzereingaben
	• Neben-Thread für den Empfang von Nachrichten


### Architekturübersicht

```text
                         ┌─────────────────────────────────┐
                         │            server.py            │
                         │─────────────────────────────────│
                         │ TCP Socket                      │
                         │ bind(0.0.0.0, PORT)             │
                         │ listen() + accept()             │
                         │ Clients-Liste + Rooms           │
                         └───────────────┬─────────────────┘
                                         │
                  ┌──────────────────────┼──────────────────────┐
                  │                      │                      │
          ┌───────▼────────┐     ┌───────▼────────┐     ┌───────▼────────┐
          │ client.py (A)  │     │ client.py (B)  │     │ client.py (C)  │
          │ Thread: send   │     │ Thread: send   │     │ Thread: send   │
          │ Thread: receive│     │ Thread: receive│     │ Thread: receive│
          └───────┬────────┘     └───────┬────────┘     └───────┬────────┘
                  │                      │                      │
          ┌───────▼─────────────────────────────────────────────▼───────┐
          │   Nachrichtenfluss: Client → Server → Broadcast im Raum     │
          └─────────────────────────────────────────────────────────────┘
```

### Datenfluss bei einer Nachricht (Broadcast nur im gleichen Raum)

Beispiel:
	• Client A ist in lobby
	• Client C ist in lobby
	• Client B ist in work

```text
Client A (lobby)            Server                        Client C (lobby)     Client B (work)
     |                       |                                |                   |
     | "Hallo" send()        |                                |                   |
     |---------------------->|  handle_client(A): recv()      |                   |
     |                       |  msg = "Hallo"                 |                   |
     |                       |  -> broadcast_room("A: Hallo") |                   |
     |                       |------------------------------->|  recv-thread: print
     |                       |                                |     A: Hallo      |
     |                       |   (nicht an work senden)       |                   |
     |                       |------------------------------X |                   |
     |                       |                                |                   |
```

### Datenfluss bei einem Befehl (Antwort nur an den Sender)
Beispiel: Client A tippt /users
```text
Client A                    Server
  |                         |
  | "/users" send()         |
  |------------------------>|
  |                         | handle_client(A): erkennt Command
  |                         | users = [..] im aktuellen Raum
  |                         | send_to(A, "users in 'lobby': ...")
  |<------------------------|
  | print("users in ...")   |
```