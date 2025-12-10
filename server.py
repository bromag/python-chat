import socket
from threading import Thread

class Server:
    clients = []  # same as in video

    # Create TCP socket over IPV4. Accept at max 5 connections.
    def __init__(self, HOST, PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        print(f"Server started on {HOST}:{PORT}")

    # Listen for incoming connections on the main thread. When a connection
    # is accepted, create a new thread to handle the client.
    def start(self):  # method name same as video
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} has been established.")
            
            client_name = client_socket.recv(1024).decode('utf-8').strip()
            client = {'socket': client_socket, 'name': client_name}

            # call the correct broadcast method name
            self.broadcast_message(f"{client_name} has joined the chat.\n", client_socket)
            
            # use 'clients' (lowercase) like in the class attribute
            self.clients.append(client)
            
            # call the correct handler function name
            Thread(target=self.handle_new_client, args=(client,), daemon=True).start()

    # Handle communication with a connected client
    def handle_new_client(self, client):
        client_socket = client['socket']
        client_name = client['name']

        while True:
            client_message = client_socket.recv(1024).decode('utf-8')

            # client leaves if they send "name:bye" or an empty message
            if client_message.strip() == client_name + ":bye" or not client_message.strip():
                self.remove_client(client)
                client_socket.close()
                break
            else:
                self.broadcast_message(f"{client_name}: {client_message}", client_socket)

    # this must be a *method* of the class, not nested in the function
    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            client_socket = client['socket']
            if client_socket != sender_socket:
                client_socket.send(message.encode('utf-8'))

    # this is missing in your paste but needed because you call remove_client()
    def remove_client(self, client):
        client_socket = client['socket']
        client_name = client['name']

        if client in self.clients:
            self.clients.remove(client)

        print(f"{client_name} has left the chat.")
        self.broadcast_message(f"{client_name} has left the chat.\n", client_socket)

        try:
            client_socket.close()
        except OSError:
            pass


# this must be at top level, not inside a method
# start the server
if __name__ == "__main__":
    server = Server('127.0.0.1', 6321)
    # call start()
    server.start()