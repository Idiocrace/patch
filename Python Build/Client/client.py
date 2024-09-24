import socket
import threading

print('PATCH')
print('We are not responsible for any actions by another client or a server host.')
print('Your connection information may be cached.')

HOST = input('Chatroom Address: ')
PORT = int(input('Chatroom Port: '))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    username_selected = False
    while not username_selected:
      username = input("Enter your username: ")
      s.sendall(f'[αΣ¤Θ]{username}'.encode('utf-8'))
      if s.recv(1024).decode('utf-8') == '[µσαΣ]':
        print('Name already taken! Please pick another name')
        continue
      username_selected = True
    print(f"Connected to server!")

    def receive_messages():
        while True:
            try:
                data = s.recv(1024).decode('utf-8')
                if data:
                    print(data)
                else:
                    break
            except ConnectionResetError:
                print("Connection was reset by the server.")
                break

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        message = input(f"{username}: ")
        if message:
            message = f"{username}: {message}"
            s.sendall(message.encode('utf-8'))
        else:
            if input('Enter "E" to exit: ').lower() == 'e':
                break
            else:
                print('Cancelled')

    receive_thread.join()

print("Disconnected from server")
