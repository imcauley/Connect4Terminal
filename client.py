import socket
import json

class Client:
    def __init__(self):
        self.current_board = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("test")
        try:
            self.sock.connect(('', 1212))
            print("connected as player a")
        except socket.error:
            print("couldn't connect as player a")

        if not self.sock:
            try:
                self.sock.connect(('', 1213))
            except socket.error:
                print("couldn't connect to server")
                exit(0)

        self.sock.sendall(b'ready')

        self.client_loop()

    def client_loop(self):
        state = self.sock.recv(2048)
        state = json.loads(state)

if __name__ == "__main__":
    Client()