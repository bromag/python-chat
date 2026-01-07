# Multi-threaded Chat Service mit festen Räumen

Dieses Projekt implementiert einen **multi-threaded Chat-Service** in Python auf Basis von TCP-Sockets.  
Mehrere Clients können sich gleichzeitig mit dem Server verbinden und in **vordefinierten Chat-Räumen** kommunizieren.

Der Server verwendet einen **dynamischen TCP-Port**, welcher beim Start automatisch vom Betriebssystem vergeben wird.  
Die Verbindungsinformationen werden in einer Datei gespeichert und vom Client automatisch gelesen.

Die Anwendung besteht aus zwei Skripten:
- `server.py` – Chat-Server
- `client.py` – Konsolen-Client

---

## Funktionen

- Multi-threaded Server (ein Thread pro Client)
- Gleichzeitige Verbindung mehrerer Clients
- Dynamischer TCP-Port
- Automatische Weitergabe von Host/Port über Datei
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

## Schritt 1: Server starten (dynamischer Port)

1. Öffne ein Terminal  
2. Wechsle in das Projektverzeichnis  
3. Starte den Server mit folgendem Befehl:

```bash
python3 server.py

## Erwartete Ausgabe 
ChatServer started on 127.0.0.1:<PORT>
Address written to server_addr.json
```

### Hinweis:
Der Port wird automatisch vergeben.
Host und Port werden in der Datei server_addr.json gespeichert.
---

## Client Starten

1. Öffne ein neuer Terminal
2. wechsle erneut in das Projetverzeichnis
3. Starte den Client mit:

```bash
python3 client.py
```
4. Falls kein Host oder Port als Parameter übergeben wurden, liest der Client diese automatisch aus:
```bash
server_addr.json
```
5. Gib anschliessend einen Benutzernamen ein:
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
- Client beenden:
Im Chat bye eingeben
- Server beenden:
Im Server-Terminal CTRL + C drücken

# Technische Erklärung des Codes

## server.py – Chat-Server

### Der Server stellt die zentrale Komponente des Systems dar und übernimmt folgende Aufgaben:
	•	Erstellt einen TCP-Socket und bindet sich an einen dynamischen Port (port = 0)
	•	Liest den tatsächlich vergebenen Port mit getsockname()
	•	Speichert Host und Port in einer JSON-Datei (server_addr.json)
	•	Wartet auf eingehende Client-Verbindungen (accept)
	•	Erstellt für jeden verbundenen Client einen eigenen Thread
	•	Verwaltet alle Clients in einer gemeinsamen Liste
	•	Ordnet jedem Client einen Chat-Raum zu
	•	Verarbeitet Chat-Befehle (/ls, /cd, /users, /server, /help)
	•	Verteilt Nachrichten ausschliesslich an Clients im gleichen Raum
	•	Entfernt Clients sauber bei Verbindungsabbruch oder bei bye

Der Server enthält die gesamte Logik für Räume, Benutzer und Nachrichtenverteilung.

⸻

## client.py – Chat-Client

### Der Client stellt die Benutzeroberfläche im Terminal bereit und übernimmt folgende Aufgaben:
	•	Liest optionale Startparameter (--host, --port, --addrfile) mittels argparse
	•	Falls Host oder Port fehlen, werden diese automatisch aus der JSON-Datei gelesen
	•	Baut eine TCP-Verbindung zum Server auf
	•	Sendet beim Verbindungsaufbau den Benutzernamen
	•	Startet einen separaten Thread zum Empfangen von Nachrichten
	•	Liest Benutzereingaben aus dem Terminal
	•	Sendet Nachrichten und Befehle an den Server
	•	Gibt empfangene Nachrichten direkt im Terminal aus
	•	Beendet die Verbindung sauber bei Eingabe von bye

Der Client enthält keine Geschäftslogik für Räume oder Benutzer – diese liegt vollständig beim Server.

⸻

## Multi-Threading-Konzept
	### Server:
	•	Ein Thread pro Client
	•	Parallele Verarbeitung mehrerer Benutzer
	## Client:
	•	Hauptthread für Benutzereingaben
	•	Neben-Thread für den Empfang von Nachrichten

### Architekturübersicht

```text
                         ┌─────────────────────────────────┐
                         │            server.py            │
                         │─────────────────────────────────│
                         │ TCP Socket                      │
                         │ bind(host, 0)  -> OS wählt Port │
                         │ getsockname() -> echter Port    │
                         │ schreibt server_addr.json       │
                         │ accept() (wartet auf Clients)   │
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
          │     Nachrichtenfluss: Client -> Server -> Broadcast im Raum │
          └─────────────────────────────────────────────────────────────┘