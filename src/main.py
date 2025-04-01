"""
Preston Thomas & Evan Gronewold
CIS 457: Group Chat Assignment
Professor Dulimarta
"""

import socket
import threading

# Server Configuration
HOST = '127.0.0.1'
PORT = 12345
clients = []

# Broadcast message to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle client connections
def handle_client(client_socket, addr):
    print(f"New connection: {addr}")
    clients.append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break
    
    print(f"Client {addr} disconnected")
    clients.remove(client_socket)
    client_socket.close()

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
