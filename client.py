import socket
from threading import Thread
import os

class Client:
    # Create TCP socket over IPV4 and connect to server.
    def __init__(self, HOST, PORT):
        self.socket = socket.socket()
        self.socket.connect((HOST, PORT))
        self.name = input("Enter your name: ")

        self.talk_to_server()
    # message sending and receiving
    def talk_to_server(self):
        # send name first
        self.socket.send(self.name.encode('utf-8'))

        # start receiving thread
        Thread(target=self.receive_messages, daemon=True).start()

        # handle sending
        self.send_messages()

    # message sending loop
    def send_messages(self):
        while True:
            client_input = input("")

            # user wants to exit
            if client_input.strip().lower() == "bye":
                self.socket.send(f"{self.name}:bye".encode("utf-8"))
                os._exit(0)

            # send chat message
            self.socket.send(client_input.encode("utf-8"))
    
    # message receiving loop
    def receive_messages(self):
        while True:
            # receive message from server
            server_message = self.socket.recv(1024).decode('utf-8')
            if not server_message.strip():
                print("Connection closed by server.")
                os._exit(0)

            print(server_message)

# client entry point
if __name__ == "__main__":
    Client('127.0.0.1', 6321)