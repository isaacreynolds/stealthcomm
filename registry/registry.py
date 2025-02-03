import socket
import ssl
import json
import threading

servers = []
CERT_FILE = 'registry.crt'
KEY_FILE = 'registry.key'

import socket
import ssl
import json
import threading

servers = []
servers_lock = threading.Lock()  # NEW: Thread safety for servers list
CERT_FILE = 'registry.crt'
KEY_FILE = 'registry.key'

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        request = json.loads(data.decode('utf-8'))
        
        if request['type'] == 'register_server':
            with open('secret.key', 'rb') as f:
                valid_key = f.read().decode()
                
            if request.get('key') != valid_key:
                client_socket.send(json.dumps({'status': 'invalid_key'}).encode())
                return
                
            with servers_lock:  # THREAD-SAFE MODIFICATION
                servers.append({
                    'ip': request['ip'],
                    'port': request['port'],
                    'users': 0
                })
                
            client_socket.send(json.dumps({'status': 'success'}).encode())
            
        elif request['type'] == 'get_servers':
            with servers_lock:  # THREAD-SAFE READ
                client_socket.send(json.dumps({'servers': servers.copy()}).encode())
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()
def start_registry():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = context.wrap_socket(server, server_side=True)
    server.bind(('0.0.0.0', 5556))
    server.listen(5)
    print("Registry running on 0.0.0.0:5556")
    
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_registry()