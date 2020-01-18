import socket
import json
import sys 

class Client:
    def __init__(self):
        self.current_board = []

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


    def print_board(self, board):
        output = ""
        for row in self.current_board:
            for e in row:
                if e == '-':
                    output += '⚪️'
                if e == 'A':
                    output += '🔴'
                if e == 'B':
                    output += '🔵'
            output += '\n'

        output += '1234567'

        sys.stdout.write("\033[H")
        sys.stdout.write("\033[2J")
        sys.stdout.write("%s" % output)

if __name__ == "__main__":
    Client()