import socket
import json

class Client:
    def __init__(self):
        self.current_board = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("test")
        try:
            self.sock.connect(('', 1212))
            print("connected")
        except socket.error:
            print("couldn't connect")
            exit(0)

        self.sock.sendall(b'ready')
        self.player_id = self.sock.recv(34)
        print(self.player_id)
        self.sock.recv(38)
        
        self.client_loop()

    def client_loop(self):
        # state = self.sock.recv(2048)
        # state = json.loads(state)

        while True:
            pass

if __name__ == "__main__":
    Client()