import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg)
        except Exception as e:
            print(f"[ERROR] {e}")
            break

def send(msg):
    client.send(msg.encode('utf-8'))


client_name = input("Enter your name: ")
send(client_name)

thread = threading.Thread(target=receive)
thread.start()

while True:
    msg = input()
    if msg == "DISCONNECT":
        send(msg)
        break
    elif msg == "QUERY":
        send(msg)
    else:
        send(msg)
