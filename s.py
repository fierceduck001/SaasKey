import sys
import socket
import threading
import secrets
import el_gamal

BANNER = """
███████╗ █████╗  █████╗ ███████╗██╗  ██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝╚██╗ ██╔╝
███████╗███████║███████║███████╗█████╔╝ █████╗   ╚████╔╝ 
╚════██║██╔══██║██╔══██║╚════██║██╔═██╗ ██╔══╝    ╚██╔╝  
███████║██║  ██║██║  ██║███████║██║  ██╗███████╗   ██║   
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝  
"""

# Check if a command line argument is provided for the port number
if len(sys.argv) != 2:
    print("Usage: python3 server.py [PORT_NUMBER]")
    sys.exit(1)

try:
    # Attempt to parse the port number from the command line argument
    PORT = int(sys.argv[1])
except ValueError:
    print("Error: Port number must be an integer")
    sys.exit(1)

LISTENER_LIMIT = 10
active_clients = []  # List of all currently connected users


# Function to choose which security method to use
def chooseMethod():
    lst = ["DES", "ELGAMAL"]
    print(BANNER)
    print("🔒 W E L C O M E   T O   S E C U R E   C H A T 🔒")
    
    print("2- ElGamal encryption Method")
    num = input("E N C R Y P T I O N: ")
    print(f"\033[95m ENCRYPTON MODE HAS BEEN STARTED\033[0m ")
    return num


def getMethod():
    return flagmethod


# Function to listen for upcoming messages from a client
def listen_for_messages(client, username, key, elgamapublickey):
    while 1:
        message = client.recv(2048).decode('utf-8')
        print("RECV : ", message)
        if message != '':
            final_msg = username + '~' + message + '~' + key + "~" + flagmethod + "~" + elgamapublickey
            send_messages_to_all(final_msg)
            print("rsaaaaaaa:   ", final_msg)
        else:
            print(f"❌ The message sent from {username} is empty")



# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())
    print("SEND : ", message.encode())


# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


# Function to handle client
def client_handler(client, key):
    while 1:
        username = client.recv(2048).decode('utf-8')
        print("RECV : ", username)
        if username != '':
            active_clients.append((username, client, key))
            key = secrets.token_hex(8).upper()
            elgamalpublickey = ",".join(map(str, ElgamalKey))
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" + flagmethod + "~" + elgamalpublickey
            send_messages_to_all(prompt_message)
            print(f"👥 {username} has joined the chat!")
            print("🔑 Session key successfully generated for", username)
            break
        else:
            print("❌ Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client, username, key, elgamalpublickey,)).start()


# Main function
def main():
    global ElgamalKey
    ElgamalKey = el_gamal.generate_public_key()
    global flagmethod
    flagmethod = chooseMethod()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', PORT))
        print(f"\033[92m🚀 Server is up and running on port {PORT}! Let's start chatting securely! 🚀\033[0m")
    except:
        print(f"❌ Unable to bind to port {PORT}")
    server.listen(LISTENER_LIMIT)
    while 1:
        client, address = server.accept()
        print(f"📡 Successfully connected to client {address[0]} {address[1]}")
        key = ""
        threading.Thread(target=client_handler, args=(client, key,)).start()


if __name__ == '__main__':
    main()
