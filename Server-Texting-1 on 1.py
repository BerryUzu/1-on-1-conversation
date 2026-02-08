import socket
import threading

class ChatServer:
    def __init__(self, username, IP, port):
        self.username = username
        self.IP = IP
        self.port = port
        self.server = None
        self.client = None
        self.addr = None
        self.running = True  # flag to control loops

    def establish_connection(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.port))
        self.server.listen(1)

        print("Waiting for a client to connect...")
        self.client, self.addr = self.server.accept()
        print(f"New client connected from {self.addr}")

    def recv_loop(self):
        while self.running:
            try:
                data = self.client.recv(2048).decode().strip()
                if not data:
                    print("Alice disconnected")
                    self.running = False
                    break
                print(f"Alice> {data}")
                if data.lower() == "exit":
                    print("Alice exited.")
                    self.running = False
                    break
            except ConnectionResetError:
                print("Connection lost!")
                self.running = False
                break

    def send_loop(self):
        while self.running:
            msg = input(f"{self.username}> ")
            try:
                self.client.sendall(msg.encode())
            except BrokenPipeError:
                print("Cannot send, connection closed!")
                self.running = False
                break
            if msg.lower() == "exit":
                print(f"{self.username} exited.")
                self.running = False
                break

    def start_chat(self):
        # Start the receive loop in a separate thread
        threading.Thread(target=self.recv_loop, daemon=True).start()
        # threading.Thread(target=self.send_loop(), daemon=True).start()
        # Main thread handles sending
        self.send_loop()

        # Clean up sockets after chat ends
        self.client.close()
        self.server.close()


# ---- RUN SERVER ----
convo = ChatServer(username="Bob", IP="192.168.1.246", port=1234)  #Name of choice,Local IP, Local Port
convo.establish_connection()
convo.start_chat()

