import socket
import json
import sys 

class Client:
    def __init__(self):
        self.current_board = []
        self.current_player = ''
        self.winner = ''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect(('', 1213))
            print("connected")
        except socket.error:
            print("couldn't connect")
            exit(0)

        self.sock.sendall(b'ready')
        self.player_id = self.sock.recv(34).decode('utf-8')
        print(self.player_id)

        self.sock.recv(38)
        
        self.client_loop()

    def client_loop(self):
        while True:
            self.sync_with_server()
            self.print_board()

            if(self.winner != '-'):
                self.print_winner()
                break

            if(self.current_player == self.player_id):
                move = self.get_player_move()
                self.send_move(move)


    def sync_with_server(self):
        state = self.sock.recv(333)
        print(state)
        state = json.loads(state.decode('utf-8'))
        self.current_board = state['board']
        self.current_player = state['active']
        self.winner = state['winner']


    def print_winner(self):
        print("\n")
        win = """
⭐⭐⭐⭐⭐⭐⭐
⭐  YOU WON  ⭐
⭐⭐⭐⭐⭐⭐⭐
        """
        lose = """
  ❌❌❌❌❌❌❌
❌   YOU LOST   ❌
  ❌❌❌❌❌❌❌
        """

        if(self.winner == self.player_id):
            print(win)
        else:
            print(lose)

    def print_board(self):
        output = ""
        for row in self.current_board[::-1]:
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
            if(col.isdigit() and int(col) > 0 and int(col) <= len(self.current_board[0])):
                valid_input = True
            else:
                print("\nnot valid input, try again")

        col = str(int(col) - 1)
        return col

    def send_move(self, move):
        message = self.player_id
        message += move
        message = bytes(message, 'utf-8')
        print(message)
        print(sys.getsizeof(message))
        self.sock.sendall(message)

if __name__ == "__main__":
    Client()