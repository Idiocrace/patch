import socket
import threading

print('PATCH')
print('We are not responsible for any actions by another client or a server host.')
print('Your connection information may be cached.')

HOST = input('Chatroom Address: ')
PORT = int(input('Chatroom Port: '))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.settimeout(5)  # Set timeout for recv to avoid indefinite blocking
    username_selected = False
    
    while not username_selected:
        username = input("Enter your username: ")
        print("Sending username to server...")
        s.sendall(f'[αΣ¤Θ]{username}'.encode('utf-8'))
        
        try:
            server_response = s.recv(1024).decode('utf-8')
            print(f"Server response: {server_response}")
            if server_response == '[µσαΣ]':
                print('Name already taken! Please pick another name')
                continue
            username_selected = True
        except socket.timeout:
            print("No response from server, retrying...")
            continue
    
    print(f"Connected to server as {username}!")

    def receive_messages():
        while True:
            try:
                data = s.recv(1024).decode('utf-8')
                if data:
                    print(data)
                else:
                    print("Server disconnected.")
                    break
            except socket.timeout:
                continue  # Don't block if no data is received within the timeout
            except ConnectionResetError:
                print("Connection was reset by the server.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    try:
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
    except KeyboardInterrupt:
        print("Interrupted by user")

    receive_thread.join()

print("Disconnected from server")
