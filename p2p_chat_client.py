import threading
from cryptography.fernet import Fernet
import socket
import traceback
import json
import os
import tkinter as tk
from tkinter import scrolledtext, simpledialog

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

# Receive messages from the server
def receive_messages(sock, chat_display):
    while True:
        try:
            encrypted_message = sock.recv(1024)
            message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
            if message:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"User: {message}\n")
                chat_display.config(state=tk.DISABLED)
                chat_display.yview(tk.END)
        except Exception as e:
            print(f"An error occurred in receive_messages: {e}")
            traceback.print_exc()
            sock.close()
            break

# Sends messages to the server
def send_messages(sock, message_entry, chat_display):
    message = message_entry.get()
    if message:
        encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
        sock.send(encrypted_message)
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {message}\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        message_entry.delete(0, tk.END)

# grabs all the servers from the central server registry program
def get_active_servers():
    registry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    registry_socket.connect(('127.0.0.1', 5556))
    request = json.dumps({'type': 'get_servers'})
    registry_socket.send(request.encode('utf-8'))
    response = json.loads(registry_socket.recv(1024).decode('utf-8'))
    registry_socket.close()
    return response['servers']

# Main client mode function
def client_mode():
    servers = get_active_servers()
    if servers:
        server_ip, server_port = servers[0]  # this connects to the first available server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))

        root = tk.Tk()
        root.title("StealthComm Chat Client")

        chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED)
        chat_display.pack(padx=10, pady=10)

        message_entry = tk.Entry(root, width=50)
        message_entry.pack(padx=10, pady=10)
        message_entry.bind("<Return>", lambda event: send_messages(sock, message_entry, chat_display))

        send_button = tk.Button(root, text="Send", command=lambda: send_messages(sock, message_entry, chat_display))
        send_button.pack(padx=10, pady=10)

        threading.Thread(target=receive_messages, args=(sock, chat_display), daemon=True).start()

        root.mainloop()
    else:
        print("No available servers found.")

if __name__ == "__main__":
    client_mode()