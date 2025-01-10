import threading
from cryptography.fernet import Fernet
import socket
import traceback
import os
import json
import tkinter as tk
from tkinter import scrolledtext

clients = []

# Load or generate the encryption key
def load_or_generate_key():
    if os.path.exists('secret.key'):
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

# Handle communication with a connected client
def handle_client(client_socket, chat_display):
    try:
        client_socket.send(cipher_suite.encrypt("Enter your username:".encode('utf-8')))
        username = cipher_suite.decrypt(client_socket.recv(1024)).decode('utf-8')
        clients.append((client_socket, username))
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User {username} connected.\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        broadcast(f"{username} has joined the chat.", client_socket, chat_display)
        
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                remove(client_socket, chat_display)
                break
            message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
            if message:
                broadcast(f"{username}: {message}", client_socket, chat_display)
            else:
                remove(client_socket, chat_display)
                break
    except Exception as e:
        print(f"An error occurred in handle_client: {e}")
        traceback.print_exc()
        remove(client_socket, chat_display)

# Broadcast a message to all clients except the sender
def broadcast(message, client_socket, chat_display):
    for client, username in clients:
        if client != client_socket:
            try:
                encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
                client.send(encrypted_message)
            except Exception as e:
                print(f"An error occurred in broadcast: {e}")
                traceback.print_exc()
                remove(client, chat_display)
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"{message}\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

# Remove a client from the list and notify others
def remove(client_socket, chat_display):
    for client, username in clients:
        if client == client_socket:
            clients.remove((client_socket, username))
            client_socket.close()
            broadcast(f"{username} has left the chat.", client_socket, chat_display)
            break

# Kick a user from the chat
def kick_user(username, chat_display):
    for client, user in clients:
        if user == username:
            remove(client, chat_display)
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"User {username} has been kicked by the server.\n")
            chat_display.config(state=tk.DISABLED)
            chat_display.yview(tk.END)
            break
    else:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"User {username} not found.\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)

# Register the server with the central registry
def register_with_registry(ip, port):
    registry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registry_socket.connect(('127.0.0.1', 5556))
    request = json.dumps({'type': 'register_server', 'ip': ip, 'port': port})
    registry_socket.send(request.encode('utf-8'))
    response = json.loads(registry_socket.recv(1024).decode('utf-8'))
    registry_socket.close()
    if response['status'] == 'success':
        print("Successfully registered with the central registry.")
    else:
        print("Failed to register with the central registry.")

# Main server mode function
def server_mode():
    def send_messages():
        while True:
            message = input("Server: ")
            if message.startswith("//kick "):
                username_to_kick = message.split(" ", 1)[1]
                kick_user(username_to_kick)
            else:
                broadcast(f"Server: {message}", None)

    # Start the thread to send messages from the server (pretty much just commands)
    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

    # Server setup with tkinter gui
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server started on {server_ip}:5555")
    print(f"Clients can connect using the IP address {server_ip} and port 5555")

    # Registers with the central registry
    register_with_registry(server_ip, 5555)

    root = tk.Tk()
    root.title("P2P Chat Server")

    chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED)
    chat_display.pack(padx=10, pady=10)

    message_entry = tk.Entry(root, width=50)
    message_entry.pack(padx=10, pady=10)
    message_entry.bind("<Return>", lambda event: broadcast(f"Server: {message_entry.get()}", None, chat_display))

    send_button = tk.Button(root, text="Send", command=lambda: broadcast(f"Server: {message_entry.get()}", None, chat_display))
    send_button.pack(padx=10, pady=10)

    # Start accepting incoming client connections
    def accept_clients():
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, chat_display))
            client_handler.start()

    threading.Thread(target=accept_clients, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    server_mode()