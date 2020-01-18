import socket
import json
import sys 

class Client:
    def __init__(self):
        self.current_board = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        while True:
            state = self.sock.recv(303)
            state = json.loads(state.decode('utf-8'))
            self.current_board = state['board']
            self.print_board()
            move = self.get_player_move()
            self.send_move(move)


    def print_board(self):
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

        output += ' 1 2 3 4 5 6 7 \n'

        sys.stdout.write("\033[H")
        sys.stdout.write("\033[2J")
        sys.stdout.write("%s" % output)

    def get_player_move(self):
        valid_input = False

        while(not valid_input):
            message = input("input what column you want: ")
            col = message[0]
            if(col.isdigit()):
                valid_input = True
            else:
                print("not valid input, try again")

        return col

    def send_move(self, move):
        message = self.player_id
        message += bytes(move,'utf-8')
        print(message)
        print(sys.getsizeof(message))
        self.sock.sendall(message)

if __name__ == "__main__":
    Client()