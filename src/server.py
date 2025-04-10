"""
Preston Thomas & Evan Gronewold
CIS 457: Group Chat Assignment
Professor Dulimarta
"""

import socket
import threading

# List to maintain active client connections
clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket):
    """
    Send a message to all clients except the sender.
    """
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print("Error sending to a client:", e)

def handle_client(client_socket, addr):
    """
    Handle communication with a single client.
    """
    print(f"New connection from {addr}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:  # client disconnected
                break
            message = data.decode('utf-8')
            print(f"Received from {addr}: {message}")
            broadcast(message, client_socket)
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        client_socket.close()
        print(f"Connection closed: {addr}")

def main():
    host = '127.0.0.1'
    port = 5001  # Ensure this matches the client configuration
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            with clients_lock:
                clients.append(client_socket)
            t = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()