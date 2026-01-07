import socket
from threading import Thread
import os
import argparse


class Client:
    # Erstellt einen TCP-Socket über IPv4 und verbindet sich mit dem Server
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.name = input("Enter your name: ").strip()

        self.talk_to_server()

    # Startet die Kommunikation mit dem Server
    def talk_to_server(self):
        # Zuerst den Namen an den Server senden
        self.socket.send(self.name.encode("utf-8"))

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
                # WICHTIG: Server erwartet "bye" (nicht "name:bye")
                self.socket.send("bye".encode("utf-8"))
                os._exit(0)

            # Chat-Nachricht an den Server senden
            self.socket.send(client_input.encode("utf-8"))

    # Schleife zum Empfangen von Nachrichten
    def receive_messages(self):
        while True:
            server_message = self.socket.recv(1024).decode("utf-8")

            if not server_message.strip():
                print("Connection closed by server.")
                os._exit(0)

            print(server_message, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat client")
    parser.add_argument("--ip", required=True, help="Server IP address")
    parser.add_argument("--port", type=int, required=True, help="Server TCP port")
    args = parser.parse_args()

    Client(args.ip, args.port)