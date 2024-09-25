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

def _print(*args):
    if '?windowed' in runtime_modifiers:
        for arg in args:
            app.log(arg)
        return
    elif not '?dev' in runtime_modifiers:
        return '<patch.soft_error.display.console.print:"The required runtime mod is not applied">'
    for arg in args:
        print(arg)

class Cache:
    def cache(data):
        with open('res\\cache', 'a') as c:
            c.write(f'{{{data}}}!')
            _print(f'Cached data {data}')

    def cached():
        with open('res\\cache', 'r') as c:
            return c.readlines()
        _print('Retrieved cached data')

    def clear():
        open('res\\cache', 'w').close()  
        _print('Cleared cache')

runtime_modifiers = None
NAME = None
IP = None
PORT = None
LOG_CHAT = None
CACHE_USERS = None

def get_configs():
    config = ConfigParser()
    config.read('server.cfg')

    NAME = config.get('Hosting', 'server_name', fallback='Unnamed Server').replace('"', '')
    IP = config.get('Hosting', 'server_ip', fallback='localhost').replace('"', '')
    PORT = int(config.get('Hosting', 'server_port', fallback='62510').replace('"', ''))

    LOG_CHAT = config.get('Logging', 'log_chats', fallback=False).replace('"', '')
    CACHE_USERS = config.get('Logging', 'cache_users', fallback=True).replace('"', '')

    runtime_modifiers = config.get('_', '__', fallback='').split('/')

if not os.path.exists('server.cfg'):
    _print('No config located. Please create a config file named "server.cfg".')
    input("Press enter to exit...")
    sys.exit()

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
                        if not any(name__ == message.replace('[αΣ¤Θ]', '') for name__ in client_dict.values()):
                            client_dict[client_socket] = message.replace('[αΣ¤Θ]', '')
                            _print(f'Client {client_socket} registered as {message.replace('[αΣ¤Θ]', '')}')
                            client_socket.sendall('[αδπß]')
                        else:
                            client_socket.sendall('[µσαΣ]'.encode('utf-8'))
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
            client_dict[f'{conn}']
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

class HostApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def console_window(self):
        self.console_window = tk.Toplevel(self.root)
        self.console_window.title('Patch Server Console')

        self.console_window.geometry('600x200')
        self.console_window.resizable(False, False)
        self.console_window.iconbitmap('res/icon.ico')

        self.console_frame = tk.Frame(self.console_window, borderwidth=2, relief='groove')
        self.console_frame.pack(padx=10, pady=(10, 10), fill='both', expand=True)

        self.console_header_label = tk.Label(self.console_frame, text='Console', anchor='w', font=('Arial', 12))
        self.console_header_label.pack(padx=5, pady=5, fill='x')

        self._console = tk.Label(self.console_frame, text='Patch Server Console', anchor='w', justify='left')
        self._console.pack(padx=5, pady=5, fill='x')

    def info_window(self):
        self.info_window = tk.Toplevel(self.root)
        self.info_window.title('Patch Server Info')

        self.info_window.iconbitmap('res/icon.ico')

        self.info_frame = tk.Frame(self.info_window, borderwidth=2, relief='groove')
        self.info_frame.pack(padx=10, pady=(2, 10), fill='both', expand=True)

        self.info_header_label = tk.Label(self.info_frame, text='Info', anchor='w', font=('Arial', 12))
        self.info_header_label.pack(padx=5, pady=5, fill='x')

    def log(self, text_):
        current = self._console.cget('text')
        self._console.config(text=f'{current}\n{text_}')
        self.root.update_idletasks()

    def start(self):
        threading.Thread(target=main, daemon=True).start()
        self.root.mainloop()

get_configs()

if '?windowed' in runtime_modifiers:
    app = HostApp()
    #app.info_window()
    app.console_window()
    app.start()

else:
    main()