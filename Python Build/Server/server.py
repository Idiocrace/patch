import socket
import random
import string
import threading
import hashlib
from configparser import ConfigParser
import os
import sys
import tkinter as tk
from time import sleep
from PIL import Image

config = ConfigParser()
config.read('server.cfg')

runtime_modifiers = config.get('_', '__', fallback='').split('/')

def _print(*args):
    if '?windowed' in runtime_modifiers:
        for arg in args:
            app.log(arg)
        return
    elif not '?dev' in runtime_modifiers:
        return '<patch.soft_error.display.console.print:"The required runtime mod is not applied">'
    for arg in args:
        print(arg)

if not os.path.exists('server.cfg'):
    _print('No config located. Please create a config file named "server.cfg".')
    input("Press enter to exit...")
    sys.exit()

# Server hosting info
NAME = config.get('Hosting', 'server_name', fallback='Unnamed Server').replace('"', '')
IP = config.get('Hosting', 'server_ip', fallback='localhost').replace('"', '')
PORT = int(config.get('Hosting', 'server_port', fallback='62510').replace('"', ''))
# ACCOUNT = config.get('Server', 'account', fallback='unspecified') # Will be used later

# Logging info
LOG_CHAT = config.get('Logging', 'log_chats', fallback=False).replace('"', '')
CACHE_USERS = config.get('Logging', 'cache_users', fallback=True).replace('"', '')

client_list = []  # List to store connected clients

client_dict = {}

def handle_client(client_socket, address):
    """Handles communication with a connected client."""
    _print(f"Client connected from {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if not message.startswith('[αΣ¤Θ]'):
                    _print(f"{message}")  # _print received message directly (includes username)
                    broadcast_message(message, client_socket)  # Broadcast to all clients
                else:
                    if not client_socket in client_dict:
                        if not any(name__ == message.replace('[αΣ¤Θ]', '') for name__ in dictionary.values()):
                            client_dict[client_socket] = message.replace('[αΣ¤Θ]', '')
                            _print(f'Client {client_socket} registered as {message.replace('[αΣ¤Θ]', '')}')
                    else:
                        _print('Connected client message tagged with username tag. Ignoring and broadcasting')
                        _print(message)
                        broadcast_message(message, client_socket)
            else:
                client_list.remove(client_socket)
                client_socket.close()
                _print(f"Client {address} disconnected!")
                break
        except ConnectionResetError:  # Handle client disconnection gracefully
            client_list.remove(client_socket)
            client_socket.close()
            _print(f"Client {address} disconnected!")
            break

def broadcast_message(message, sender_socket):
    """Broadcasts a message to all connected clients except the sender."""
    for client_socket in client_list:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except ConnectionResetError:  # Handle client disconnection gracefully
                client_list.remove(client_socket)
                client_socket.close()
                _print(f"Client {client_list.index(client_socket)} disconnected!")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP, PORT))
        s.listen()
        _print(f"Server \"{NAME}\" listening on {IP}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_list.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

class HostApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Patch Host App')

        self.root.iconbitmap('res/icon.ico')

        self.console_frame = tk.Frame(self.root, borderwidth=2, relief='groove')
        self.console_frame.pack(padx=10, pady=(2, 10), fill='both', expand=True)
        self.console_header_label = tk.Label(self.console_frame, text='Console', anchor='w', font=('Arial', 12))
        self.console_header_label.pack(padx=5, pady=5, fill='x')
        self._console = tk.Label(self.console_frame, text='Running windowed host...', anchor='w', justify='left')
        self._console.pack(padx=5, pady=5, fill='x')

    def window(self):
        self.root.mainloop()

    def log(self, text_):
        current = self._console.cget('text')
        self._console.config(text=f'{current}\n{text_}')
        self.root.update_idletasks()

    def start(self):
        threading.Thread(target=main, daemon=True).start()
        self.window()

if '?windowed' in runtime_modifiers:
    app = HostApp()
    app.start()

else:
    main()