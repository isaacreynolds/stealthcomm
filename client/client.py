import socket
import ssl
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, messagebox
from cryptography.fernet import Fernet

class MatrixClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Matrix Chat")
        self.root.geometry("600x400")
        
        # Get registry IP first
        self.registry_ip = simpledialog.askstring(
            "Registry Server",
            "Enter Registry IP Address:",
            initialvalue="192.168.1.100"
        )
        if not self.registry_ip:
            self.root.destroy()
            return
            
        self.setup_styles()
        self.current_frame = None
        self.sock = None
        self.username = None
        self.secret_key = None
        self.load_secret_key()
        self.show_server_selection()
        self.root.mainloop()

    def load_secret_key(self):
        try:
            with open('secret.key', 'rb') as key_file:
                self.secret_key = Fernet(key_file.read())
        except FileNotFoundError:
            messagebox.showerror("Error", "Missing secret.key file!")
            self.root.quit()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('Matrix.TFrame', background='black')
        style.configure('Matrix.TLabel', background='black', 
                      foreground='#00b300', font=('Agency FB', 12))
        style.configure('Matrix.Treeview', background='black', 
                      fieldbackground='black', foreground='#00b300')

    def fetch_servers(self):
        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations('registry.crt')
            
            with socket.create_connection((self.registry_ip, 5556)) as sock:
                with context.wrap_socket(sock, server_hostname='registry') as ssock:
                    ssock.send(json.dumps({'type': 'get_servers'}).encode())
                    response = json.loads(ssock.recv(4096).decode())
                    
                    self.server_tree.delete(*self.server_tree.get_children())
                    for server in response.get('servers', []):
                        self.server_tree.insert('', 'end', 
                                              values=(f"{server['ip']}:{server['port']}", 
                                                      server['users']))
        except Exception as e:
            messagebox.showerror("Error", f"Server fetch failed: {str(e)}")

    def connect_to_server(self, ip, port):
        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_verify_locations('server.crt')
            
            self.sock = socket.create_connection((ip, int(port)))
            self.secure_sock = context.wrap_socket(self.sock, server_hostname=ip)
            
            self.secure_sock.send(self.secret_key.encrypt(b'Auth'))
            self.username = simpledialog.askstring("Name", "Chat Nickname:")
            if not self.username:
                messagebox.showwarning("Invalid", "Username required!")
                self.secure_sock.close()
                return
                
            self.show_chat_interface()
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")

    def show_chat_interface(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, style='Matrix.TFrame')
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        ttk.Label(frame, text=f"Connected as {self.username}", style='Matrix.TLabel').pack()
        
        self.chat_display = scrolledtext.ScrolledText(frame,
                                                    wrap=tk.WORD,
                                                    bg='black',
                                                    fg='#00b300',
                                                    font=('Agency FB', 12))
        self.chat_display.pack(expand=True, fill=tk.BOTH)
        self.chat_display.config(state=tk.DISABLED)
        
        self.msg_entry = ttk.Entry(frame, font=('Agency FB', 12))
        self.msg_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=10)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        
        ttk.Button(frame, text="Send", command=self.send_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Leave", command=self.leave_chat).pack(side=tk.LEFT, padx=5)

    def receive_messages(self):
        while True:
            try:
                encrypted = self.secure_sock.recv(4096)
                if not encrypted:
                    break
                message = self.secret_key.decrypt(encrypted).decode()
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, message + "\n")
                self.chat_display.config(state=tk.DISABLED)
                self.chat_display.see(tk.END)
            except:
                break

    def send_message(self):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
            
        if msg == '//leavechat':
            self.leave_chat()
            return
            
        try:
            encrypted = self.secret_key.encrypt(msg.encode())
            self.secure_sock.send(encrypted)
            self.msg_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Send failed: {str(e)}")

    def leave_chat(self):
        try:
            self.secure_sock.send(self.secret_key.encrypt(b'//leavechat'))
            self.secure_sock.close()
        except:
            pass
        self.root.destroy()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    def show_server_selection(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, style='Matrix.TFrame')
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        ttk.Label(frame, text="Available Servers", style='Matrix.TLabel').pack()
        
        self.server_tree = ttk.Treeview(frame, columns=("Server", "Users"), show="headings")
        self.server_tree.pack(expand=True, fill=tk.BOTH)
        self.server_tree.heading("Server", text="Server Address")
        self.server_tree.heading("Users", text="Users Online")
        
        ttk.Button(frame, text="Refresh", command=self.fetch_servers).pack(pady=5)
        ttk.Button(frame, text="Connect", command=self.connect_selected).pack()
        
        self.fetch_servers()

    def connect_selected(self):
        selected = self.server_tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a server first!")
            return
            
        server = self.server_tree.item(selected[0])['values'][0]
        ip, port = server.split(':')
        self.connect_to_server(ip, port)

if __name__ == "__main__":
    MatrixClient()