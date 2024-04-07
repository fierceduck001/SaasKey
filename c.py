import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import el_gamal

# Check if a command line argument is provided for the port number
if len(sys.argv) != 2:
    print("Usage: python3 client.py [PORT_NUMBER]")
    sys.exit(1)

try:
    # Attempt to parse the port number from the command line argument
    PORT = int(sys.argv[1])
except ValueError:
    print("Error: Port number must be an integer")
    sys.exit(1)

# Rest of the client code remains unchanged
# Replace HOST with the appropriate server IP address if needed
HOST = '192.168.74.98'
DARK_GREY = '#485460'
MEDIUM_GREY = '#1e272e'
OCEAN_BLUE = '#60a3bc'
WHITE = "white"
FONT = ("Helvetica", 14)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mes = None

def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect", f"Unable to connect to server {HOST}:{PORT}")

    username = username_entry.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server).start()
    username_entry.config(state=tk.DISABLED)
    connect_button.config(state=tk.DISABLED)

def send_message():
    message = message_entry.get()
    if message != '':
        message_entry.delete(0, tk.END)
        message = el_gamal.incrypt_gamal(int(elgamalkey[0]), int(elgamalkey[1]), int(elgamalkey[2]), message)
        client.sendall(message.encode("utf-8"))

def listen_for_messages_from_server():
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            message = message.split("~")
            global key, flagMethod, elgamalkey
            username = message[0]
            content = message[1]
            key = message[2]
            flagMethod = int(message[3])
            elgamalkey = message[4].split(",")

            if username != "SERVER":
                if flagMethod == 2:
                    content = el_gamal.decrept_gamal(content, int(elgamalkey[3]))

            add_message(f"[{username}] {content}")

def add_message(message):
    message_text.config(state=tk.NORMAL)
    message_text.insert(tk.END, message + '\n')
    message_text.see(tk.END)
    message_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Secure Chat")

container = ttk.Frame(root, padding="10")
container.grid(row=0, column=0, sticky="nsew")

username_label = ttk.Label(container, text="Enter your alias:", font=FONT)
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

username_entry = ttk.Entry(container, font=FONT)
username_entry.grid(row=0, column=1, padx=5, pady=5)

connect_button = ttk.Button(container, text="Connect", command=connect)
connect_button.grid(row=0, column=2, padx=5, pady=5)

message_text = scrolledtext.ScrolledText(container, wrap=tk.WORD, font=FONT, state=tk.DISABLED)
message_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

message_entry = ttk.Entry(container, font=FONT)
message_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

send_button = ttk.Button(container, text="Send", command=send_message)
send_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

root.mainloop()
