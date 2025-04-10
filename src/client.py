"""
Preston Thomas, Evan Gronewold
https://realpython.com/python-gui-tkinter/
https://www.pythonguis.com/tkinter-tutorial/
https://realpython.com/python-sockets/ 
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
import queue

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Slack Lite")
        
        # Create a thread-safe queue for messages from the server
        self.chat_queue = queue.Queue()
        
        # Chat display: a scrolled text widget for conversation
        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', wrap='word', width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # Configure a tag for styling the username (blue, bold text)
        self.chat_display.tag_config('username', foreground='blue', font=('TkDefaultFont', 10, 'bold'))
        
        # Input area: a text widget for multi-line message entry
        self.input_text = tk.Text(master, height=3, wrap='word')
        self.input_text.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        
        # Send button to dispatch the message
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=5)
        master.grid_columnconfigure(0, weight=1)
        
        # Set up the network connection
        self.host = '127.0.0.1'  # Must match server host address
        self.port = 5000         # Must match the server configuration port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            master.quit()
            return

        # Prompt for username using a simple dialog
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=master)
        if not self.username:
            self.username = "Anonymous"

        # Start a thread to continuously receive messages from the server
        self.running = True
        self.recv_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.recv_thread.start()

        # Periodically update the chat display with new messages
        self.master.after(100, self.update_chat_display)
        
        # Bind the window closing event to handle a graceful shutdown
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def send_message(self):
        # Retrieve the text from the input area and clear it
        msg = self.input_text.get("1.0", tk.END).strip()
        self.input_text.delete("1.0", tk.END)
        if msg:
            full_msg = f"{self.username}: {msg}"
            try:
                self.sock.send(full_msg.encode('utf-8'))
            except Exception as e:
                self.chat_queue.put(f"Error sending message: {e}")
                return
            # Immediately display the message locally
            self.chat_display.config(state='normal')
            self.chat_display.insert(tk.END, f"{self.username}:", 'username')
            self.chat_display.insert(tk.END, f" {msg}\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state='disabled')

    def receive_messages(self):
        # Continuously receive messages from the server
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    self.chat_queue.put(message)
                else:
                    # If no data, the connection might have been closed
                    self.running = False
                    self.chat_queue.put("Disconnected from server.")
            except Exception as e:
                self.chat_queue.put(f"Error receiving message: {e}")
                self.running = False

    def update_chat_display(self):
        # Process all messages in the queue and update the chat display
        while not self.chat_queue.empty():
            msg = self.chat_queue.get_nowait()
            self.chat_display.config(state='normal')
            if ':' in msg:
                # Split on the first colon to separate username from message
                username, rest = msg.split(':', 1)
                self.chat_display.insert(tk.END, username + ":", 'username')
                self.chat_display.insert(tk.END, rest + "\n")
            else:
                self.chat_display.insert(tk.END, msg + "\n")
            self.chat_display.see(tk.END)  # Auto-scroll to the end
            self.chat_display.config(state='disabled')
        if self.running:
            self.master.after(100, self.update_chat_display)

    def on_closing(self):
        # Gracefully shut down the connection and close the window
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()