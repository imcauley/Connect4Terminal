import socket
import json
import sys

class Server:

    def __init__(self):
        self.ROW_NUM = 6
        self.COL_NUM = 7
        self.winner = '-'

        PORT = 1213

        self.board = []
        for _ in range(7):
            self.board.append(['-']*7)

        self.player_a = None
        self.player_b = None
        self.socket = socket.socket()
        self.socket.bind(('', PORT))
        self.connect_players()
        
        self.current_turn = False

        self.game_loop()

    def connect_players(self):
        self.socket.listen(5)

        while True:
            self.player_a, _ = self.socket.accept()
            message = self.player_a.recv(38)
            if(message == b'ready'):
                self.player_a.sendall(b'A')
                print('player A connected')
                break
        
        while True:
            self.player_b, _ = self.socket.accept()
            message = self.player_b.recv(38)
            if(message == b'ready'):
                self.player_b.sendall(b'B')
                break

        print('both players connected')
        self.player_a.sendall(b'start')
        self.player_b.sendall(b'start')

    def game_loop(self):
        current_player = None

        while(self.winner == '-'):

            if(self.current_turn):
                current_player = self.player_a
            else:
                current_player = self.player_b

            self.sync_to_clients()

            message = (current_player.recv(35).decode('utf-8'))
            player = message[0]
            place = int(message[1])

            self.make_move(place, player)
            self.check_board()                

            self.current_turn = not self.current_turn

        self.sync_to_clients()
        self.player_a.close()
        self.player_b.close()

    def make_move(self, place, player):

        for c in range(7):
            if(self.board[c][place] == '-'):
                self.board[c][place] = player
                break

    def check_board(self):
        for i in range(self.ROW_NUM):
            for j in range(self.COL_NUM):
                self.check_spot(i, j)

    def check_spot(self, row, col):
        current = self.board[row][col]
        if current != '-':
            for i in range(4):
                if self.in_board(row + i, col) and current != self.board[row + i][col]:
                    break
            else:
                self.winner = current

            for i in range(4):
                if self.in_board(row, col + i) and current != self.board[row][col + i]:
                    break
            else:
                self.winner = current

            for i in range(4):
                if self.in_board(row + i, col + i) and current != self.board[row][col + i]:
                    break
            else:
                self.winner = current

    def in_board(self, row, col):
        if row >= 0 and row < self.ROW_NUM:
            if col >= 0 and col < self.COL_NUM:
                return True

        return False

    def sync_to_clients(self):
        print("starting sync")

        package = {}
        package['board'] = self.board
        package['active'] = 'A' if self.current_turn else 'B'
        package['winner'] = self.winner

        message = bytes(json.dumps(package), 'utf-8')

        print(sys.getsizeof(message))

        self.player_a.sendall(message)
        self.player_b.sendall(message)

if __name__ == "__main__":
    Server()
