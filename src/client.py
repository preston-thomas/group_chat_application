import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def connect():
    print("buttons Works")

def send_message():
    print("button send Works")

root = tk.Tk()
root.geometry("600x600")
root.title("Chat with Friends")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg="grey")
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg="white")
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg="grey")
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter Username: ", font=("Arial", 16), bg="black", fg="white")
username_label.pack(side=tk.LEFT, padx=10, pady=10)

username_textbox = tk.Entry(top_frame, font=("Arial", 16), bg="black", fg="white", width=20)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join Chat", font=("Arial, 18"), bg="blue", fg="white", command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=("Arial, 16"), bg="grey", fg="white", width=35)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=("Arial, 18"), bg="blue", fg="white", command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=("Arial", 14), bg="grey", fg="white", width=65, height=25)
message_box.pack(side=tk.TOP)




HOST = "127.0.0.1"
PORT = 8000
def listen_for_messages_from_server(client):
    while True:
        message = client.recv(2048).decode("utf-8")
        if message != '':
            username = message.split(":")[0]
            content = message.split(":")[1]
            print(f"{username}: {content}")
        else:
            print("Message from server empty.")

    
def send_message_to_server(client):
    while True:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode("utf-8"))
        else:
            print("Message empty.")
            exit(0)

def communicate_with_server(client):
    username = input("What is your name?: ")
    if username != '':
        client.sendall(username.encode("utf-8"))
    else:
        print("Must have a name.")
        exit(0)
    
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    send_message_to_server(client)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    root.mainloop()

    try: 
        client.connect((HOST, PORT))
        print("Connected to the server.")
    
    except:
        print("Unable to connect to the server.")
    
    communicate_with_server(client)

if __name__ == "__main__":
    main()