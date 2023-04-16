import socket
import sys
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

clients = {}

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_name = client.recv(1024).decode('utf-8')
    clients[client_name] = addr

    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == "DISCONNECT":
                del clients[client_name]
                client.close()
                break
            elif msg == "QUERY":
                client.send(str(clients).encode('utf-8'))
            else:
                recipient, message = msg.split(":", 1)
                recipient_addr = clients.get(recipient)
                if recipient_addr:
                    client.send(f"{client_name}: {message}".encode('utf-8'))
                else:
                    client.send("Recipient not found.".encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"[DISCONNECTED] {addr} disconnected.")

while True:
    client, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(client, addr))
    thread.start()
