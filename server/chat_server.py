import socket
import ssl
import json
import threading
from cryptography.fernet import Fernet

CERT_FILE = 'server.crt'
KEY_FILE = 'server.key'
servers_lock = threading.Lock()
class SecureChatServer:
    def __init__(self, registry_ip=None):
        # Allow user input for registry IP if not provided
        if not registry_ip:
            registry_ip = input("Enter the registry server IP address: ")
        # Validate IP address input by attempting to resolve it
        try:
            socket.getaddrinfo(registry_ip, None)
        except socket.gaierror:
            print(f"Invalid registry IP address: {registry_ip}")
            exit(1)
            
        self.registry_ip = registry_ip
        self.key = Fernet(open('secret.key', 'rb').read())
        self.clients = []
        self.user_count = 0
        # Register with the registry first
        self.register_with_registry()
        # Start the chat server in a separate thread so registration doesn't block it
        threading.Thread(target=self.start_server, daemon=True).start()

    def get_lan_ip(self):
        """Get actual LAN IP for network visibility"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return socket.gethostbyname(socket.gethostname())

    def register_with_registry(self):
        """Register with LAN IP instead of localhost"""
        try:
            lan_ip = self.get_lan_ip()
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations('registry.crt')
            
            # Use the user-provided registry IP
            with socket.create_connection((self.registry_ip, 5556)) as sock:
                with context.wrap_socket(sock, server_hostname='registry') as ssock:
                    ssock.send(json.dumps({
                        'type': 'register_server',
                        'ip': lan_ip,
                        'port': 5555,
                        'key': self.key._signing_key.decode()
                    }).encode())
        except Exception as e:
            print(f"Registration error: {str(e)}")

    def handle_client(self, client_socket):
        try:
            encrypted_key = client_socket.recv(1024)
            if self.key.decrypt(encrypted_key) != b'Auth':
                client_socket.close()
                return
                
            username = json.loads(self.key.decrypt(client_socket.recv(1024)).decode())['username']
            self.user_count += 1
            self.clients.append(client_socket)
            
            while True:
                encrypted = client_socket.recv(4096)
                if not encrypted:
                    break
                self.broadcast(encrypted, client_socket)
                
        except Exception as e:
            print(f"Client handling error: {str(e)}")
            client_socket.close()
        finally:
            self.user_count -= 1

    def broadcast(self, message, sender_socket):
    # Iterate over copy to prevent modification during iteration
        for client in self.clients.copy():  # COPY HERE
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Broadcast error: {str(e)}")
                with servers_lock:  # THREAD-SAFE REMOVAL
                    if client in self.clients:
                        self.clients.remove(client)

    def start_server(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(CERT_FILE, KEY_FILE)
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = context.wrap_socket(server, server_side=True)
        server.bind(('0.0.0.0', 5555))
        server.listen(5)
        print(f"Chat server running on {self.get_lan_ip()}:5555")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    SecureChatServer()