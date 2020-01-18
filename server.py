import socket
import json
import sys

class Server:

    def __init__(self):
        self.ROW_NUM = 6
        self.COL_NUM = 7
        self.winner = None

        PORT = 1212

        self.board = []
        for _ in range(7):
            self.board.append([0]*7)

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



        while(not self.winner):

            if(self.current_turn):
                current_player = a
            else:
                current_player = b

            place = current_player.recv(8)

            self.make_move(place)
            self.check_board()

            self.current_turn = not self.current_turn

        a.close()
        b.close()

    def make_move(self, place):
        marker = 1
        if self.current_turn:
            marker = 2

        for c in range(7):
            if(self.board[place][c] != 0):
                self.board[place][c] = marker
                break

    def check_board(self):
        pass

    def check_spot(self, row, col):
        for i in range(4):
            
            if i + row > 0 and i + row <= self.ROW_NUM:
                pass

    def create_package(self):
        package = {}
        package['board'] = self.board

        return json.dumps(package)

if __name__ == "__main__":
    Server()