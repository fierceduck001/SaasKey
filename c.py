import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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

# Replace HOST with the appropriate server IP address if needed
HOST = '10.0.2.15'

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
        add_message("[🌐 SERVER] Connection successful!")
    except:
        messagebox.showerror("Connection Error", f"Unable to connect to server {HOST}:{PORT}")

    username = username_entry.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid Username", "Please provide a username")

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

            add_message(f"[👤 {username}] {content}")

def add_message(message):
    message_text.config(state=tk.NORMAL)
    message_text.insert(tk.END, message + '\n')
    message_text.see(tk.END)
    message_text.config(state=tk.DISABLED)

root = ttk.Window()
root.title("🔒 SaasKey - Secure Chat")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# First slide
slide1 = ttk.Frame(notebook)
notebook.add(slide1, text='Chat')

container = ttk.Frame(slide1, padding="10")
container.pack(fill='both', expand=True)

username_label = ttk.Label(container, text="Enter your username:", font=FONT)
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

username_entry = ttk.Entry(container, font=FONT, width=30)  # Increase the width as needed
username_entry.grid(row=0, column=1, padx=5, pady=5)

connect_button = ttk.Button(container, text="Connect", command=connect, bootstyle=SUCCESS)
connect_button.grid(row=0, column=2, padx=5, pady=5)

message_text = scrolledtext.ScrolledText(container, wrap=tk.WORD, font=FONT, state=tk.DISABLED)
message_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

message_entry = ttk.Entry(container, font=FONT, width=50)  # Increase the width as needed
message_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

send_button = ttk.Button(container, text="Send", command=send_message, bootstyle=SUCCESS)
send_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

slide2 = ttk.Frame(notebook)
notebook.add(slide2, text='Information')

# Label to provide information about the chat application
info_label = ttk.Label(slide2, text="Welcome to SaasKey - Secure Chat", font=FONT, foreground="blue")
info_label.pack(padx=10, pady=10)

# Text widget to display additional information about the chat application
info_text = scrolledtext.ScrolledText(slide2, wrap=tk.WORD, font=FONT, state=tk.NORMAL, height=10)
info_text.pack(fill='both', expand=True, padx=10, pady=5)

# Additional information about the chat application
info_text.insert(tk.END, "🔒 Welcome to SaasKey - Your Ultimate Secure Chat Solution! 🔒\n\n"
                         "SaasKey empowers you to communicate securely, ensuring the utmost privacy and "
                         "security of your conversations. Here's what makes SaasKey exceptional:\n\n"
                         "🔐 End-to-end Encryption: Your messages are encrypted using the advanced "
                         "ElGamal encryption method, ensuring that only you and your recipient can "
                         "decrypt and read them.\n\n"
                         "🎨 User-friendly Interface: SaasKey offers an intuitive and visually appealing "
                         "interface, making it easy for you to navigate and enjoy a seamless chatting experience.\n\n"
                         "💬 Real-time Messaging: Chat in real-time with friends, family, and colleagues, "
                         "regardless of your location. SaasKey ensures instant delivery of your messages.\n\n"
                         "🔗 Secure Connection: Connect to the server securely, safeguarding your data "
                         "from unauthorized access and cyber threats.\n\n"
                         "⚙️ Easy-to-use Settings: Customize your chat experience with SaasKey's "
                         "user-friendly settings, allowing you to tailor the app to your preferences.\n\n"
                         "🌟 Enjoy secure and private communication with SaasKey! Get started today and "
                         "experience the next level of chat security. 🌟\n")

info_text.config(state=tk.DISABLED)

root.mainloop()
