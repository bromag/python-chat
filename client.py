import socket
from threading import Thread
import os
import argparse          # für Startparameter
import json              # um Host/Port aus Datei zu lesen


class Client:
    # Erstellt einen TCP-Socket über IPv4 und verbindet sich mit dem Server
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")

        self.talk_to_server()

    # Startet die Kommunikation mit dem Server
    def talk_to_server(self):
        # Zuerst den Namen an den Server senden
        self.socket.send(self.name.encode('utf-8'))

        # Thread zum Empfangen von Nachrichten starten
        Thread(target=self.receive_messages, daemon=True).start()

        # Nachrichten senden
        self.send_messages()

    # Schleife zum Senden von Nachrichten
    def send_messages(self):
        while True:
            client_input = input("")

            # Benutzer möchte die Verbindung beenden
            if client_input.strip().lower() == "bye":
                self.socket.send(f"{self.name}:bye".encode("utf-8"))
                os._exit(0)

            # Chat-Nachricht an den Server senden
            self.socket.send(client_input.encode("utf-8"))

    # Schleife zum Empfangen von Nachrichten
    def receive_messages(self):
        while True:
            # Nachricht vom Server empfangen
            server_message = self.socket.recv(1024).decode('utf-8')

            # Falls keine Nachricht mehr kommt, Verbindung beenden
            if not server_message.strip():
                print("Connection closed by server.")
                os._exit(0)

            print(server_message)


# Einstiegspunkt des Clients
if __name__ == "__main__":
    # argparse erlaubt optionale Übergabe von Host/Port
    parser = argparse.ArgumentParser(description="Chat client")
    parser.add_argument("--host", default=None, help="Server host (optional)")
    parser.add_argument("--port", type=int, default=None, help="Server port (optional)")
    parser.add_argument("--addrfile", default="server_addr.json", help="Address file from server")
    args = parser.parse_args()

    host = args.host
    port = args.port

    # Wenn Host oder Port nicht angegeben sind,
    # werden sie automatisch aus der Datei gelesen
    if host is None or port is None:
        with open(args.addrfile, "r", encoding="utf-8") as f:
            addr = json.load(f)
            host = host or addr["host"]
            port = port or addr["port"]
    # ------------

    Client(host, port)