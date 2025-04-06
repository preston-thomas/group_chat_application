"""
Preston Thomas & Evan Gronewold
CIS 457: Group Chat Assignment
Professor Dulimarta
"""

import socket
import threading

# Server Configuration
HOST = '127.0.0.1'
PORT = 8000
clients = []

def listen_for_messages(client, username):
    while True:

        response = client.recv(2048).decode("utf-8")
        if response != '':
            message = username + ": " + response
            send_messages_to_all_clients(message)
        else:
            print("Client response empty.")

def send_message_to_client(client, message):
    client.sendall(message.encode("utf-8"))

# function to send a message to all clients connected to the server 
def send_messages_to_all_clients(message):
    for client in clients:
        send_message_to_client(client[1], message)


def handle_client(client):
    
    # server will listen to clients and messages sent
    while True:
        username = client.recv(2048).decode("utf-8")
        if username != '':
            clients.append((username, client))
            send_messages_to_all_clients(f"{username} has joined the chat.")
            break
        else:
            print("Client Username empty.")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # bind server to host and a port
        server.bind((HOST, PORT))

    except:
        print("Unable to bind the host and port.")
    
    # set our server to listen for connections
    server.listen()

    # have a while loop to keep listening for connections
    while True:
        client, address = server.accept()
        print(f"Connection from {address} successful.")
        threading.Thread(target=handle_client, args=(client, )).start()
        print(f"Running server on {HOST}:{PORT}")

if __name__ == "__main__":
    main()
