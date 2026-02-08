from socket import *
from threading import *

client = socket(AF_INET, SOCK_STREAM)
client.connect(('192.168.1.246', 1234))
print("~Connection established~")

def send():
    while True:
        msg = input("Alice> ")   # blocking, only for user input; Change name as desired
        client.sendall(msg.encode())
        if msg.lower() == "exit":
            break

def receive():
    while True:
        try:
            data = client.recv(2048).decode().strip()
        except OSError:
            break  # socket closed
        if not data:
            print("\nBob disconnected")
            break
        print(f"\nBob> {data}")

        if data.lower() == "exit":
            break

def do():
    Thread(target=send).start()
    Thread(target=receive).start()

do()


