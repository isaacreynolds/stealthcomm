import socket
import threading
import json

servers = []

# Handle requests from clients (servers or chat clients)
def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        request = json.loads(data)
        
        if request['type'] == 'register_server':
            servers.append((request['ip'], request['port']))
            client_socket.send(json.dumps({'status': 'success'}).encode('utf-8'))
            print(f"New server registered: {request['ip']}:{request['port']}")
        elif request['type'] == 'get_servers':
            client_socket.send(json.dumps({'servers': servers}).encode('utf-8'))
            print(f"Client requested server list. Current servers: {servers}")
        else:
            client_socket.send(json.dumps({'status': 'error', 'message': 'Invalid request type'}).encode('utf-8'))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

# Start the central registry server
def start_registry_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5556))
    server.listen(5)
    print("Central registry server started on port 5556")

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__": 
    start_registry_server()