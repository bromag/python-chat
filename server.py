import socket
from threading import Thread

class Server:
    # Liste aller verbundenen Clients.
    # Jeder Eintrag ist ein Dict: {"socket": <socket>, "name": <str>, "room": <str>}
    clients = []

    # FIXE Räume: Es dürfen nur diese Räume existieren (keine neuen erstellen).
    rooms = {"lobby", "work", "support", "team"}

    # Standardraum: Jeder Client startet automatisch in der Lobby.
    default_room = "lobby"

    def __init__(self, host, port):
        # TCP/IPv4 Socket erstellen
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Erlaubt schnelles Neustarten, ohne "Address already in use"
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Socket an Host/Port binden
        self.server_socket.bind((host, port))

        # Server beginnt zu lauschen (max. 5 wartende Verbindungen im Backlog)
        self.server_socket.listen(5)

        # Statusausgabe
        print(f"Server started on {host}:{port}")

    def start(self):
        # Hauptloop: akzeptiert laufend neue Verbindungen
        while True:
            # Blockiert, bis sich ein Client verbindet
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")

            # Erwartet als erstes Paket: den Namen des Clients
            name = client_socket.recv(1024).decode("utf-8").strip()

            # Client-Datenstruktur mit Start-Raum
            client = {"socket": client_socket, "name": name, "room": self.default_room}

            # Client zur globalen Liste hinzufügen
            self.clients.append(client)

            # Dem Client erklären, wo er ist und wie er den Chat benutzt
            self.send_to(client, f"You joined '{self.default_room}'. Use /join <room>, /rooms, bye.\n")
            self.send_to(client, "Available rooms: lobby, work, support, team\n")

            # Den Raum informieren, dass der Client beigetreten ist
            self.broadcast_room(f"[{client['room']}] {name} joined.\n", client)

            # Für jeden Client einen eigenen Thread starten (Multi-Threading)
            Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        # Socket und Name für schnelleren Zugriff
        s = client["socket"]
        name = client["name"]

        # Loop: verarbeitet Nachrichten dieses Clients
        while True:
            # Blockiert, bis Daten eintreffen
            data = s.recv(1024)

            # Wenn keine Daten mehr kommen: Client hat Verbindung geschlossen
            if not data:
                self.remove_client(client)
                break

            # Nachricht dekodieren und Whitespace entfernen
            msg = data.decode("utf-8").strip()

            # Leere Nachricht ignorieren
            if not msg:
                continue

            # Beenden, wenn Client "bye" schreibt
            if msg.lower() == "bye":
                self.remove_client(client)
                break

            # Command: Räume anzeigen
            if msg == "/ls":
                self.send_to(client, "Rooms: lobby, work, support, team\n")
                continue

            # Command: Raum wechseln
            if msg.startswith("/cd "):
                # Gewünschter Raumname (alles klein, damit /join Work auch geht)
                requested = msg.split(" ", 1)[1].strip().lower()

                # Nur erlaubte Räume akzeptieren (keine neuen Räume erstellen)
                if requested not in self.rooms:
                    self.send_to(client, "Room does not exist. Use /rooms to see allowed rooms.\n")
                    continue

                # Raumwechsel durchführen
                self.change_room(client, requested)
                continue
            
            # Command: Kann user im Chatraum anzeigen
            if msg == "/users":
                room = client["room"]
                users = [c["name"]for c in self.clients if c["room"] == room]
                self.send_to(
                    client,
                    f"users in '{room}' ({len(users)}): " + ", ".join(users) + "\n"
                )
                continue

            # Normale Chat-Nachricht: nur an Clients im selben Raum senden
            self.broadcast_room(f"{name}: {msg}\n", client)

    def broadcast_room(self, message, sender_client):
        # Raum des Absenders bestimmen
        room = sender_client["room"]

        # An alle Clients senden, die im selben Raum sind (inkl. Sender)
        for c in self.clients:
            # Andere Räume überspringen
            if c["room"] != room:
                continue

            try:
                # Nachricht an den Client senden
                c["socket"].send(message.encode("utf-8"))
            except OSError:
                # Falls Senden fehlschlägt: Client entfernen
                self.remove_client(c)

    def send_to(self, client, message):
        # Hilfsfunktion: Nachricht nur an einen bestimmten Client senden
        try:
            client["socket"].send(message.encode("utf-8"))
        except OSError:
            # Falls Socket nicht mehr gültig ist: ignorieren
            pass

    def change_room(self, client, new_room):
        # Aktuellen Raum merken
        old_room = client["room"]
        name = client["name"]

        # Wenn bereits im gewünschten Raum: Info an Client und abbrechen
        if new_room == old_room:
            self.send_to(client, f"You are already in '{new_room}'.\n")
            return

        # Dem alten Raum mitteilen, dass der Client ihn verlässt
        self.broadcast_room(f"[{old_room}] {name} left.\n", client)

        # Raum im Client-Dict aktualisieren
        client["room"] = new_room

        # Client selbst informieren
        self.send_to(client, f"You joined '{new_room}'.\n")

        # Dem neuen Raum mitteilen, dass der Client beigetreten ist
        self.broadcast_room(f"[{new_room}] {name} joined.\n", client)

    def remove_client(self, client):
        # Client aus der Liste entfernen (wenn vorhanden)
        if client in self.clients:
            self.clients.remove(client)

        # Für Log-Ausgabe
        name = client["name"]
        room = client["room"]
        print(f"{name} disconnected.")

        # Allen verbleibenden Clients im selben Raum mitteilen, dass er gegangen ist
        for c in list(self.clients):
            if c["room"] == room:
                try:
                    c["socket"].send(f"[{room}] {name} left.\n".encode("utf-8"))
                except OSError:
                    pass

        # Socket schliessen (best-effort)
        try:
            client["socket"].close()
        except OSError:
            pass

# Startpunkt des Programms: nur wenn diese Datei direkt ausgeführt wird
if __name__ == "__main__":
    # Server auf localhost:6321 starten
    Server("127.0.0.1", 6321).start()