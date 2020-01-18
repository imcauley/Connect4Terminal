import socket

class Server:

    def __init__(self):
        self.ROW_NUM = 6
        self.COL_NUM = 7

        PORT_A = 1212
        PORT_B = 1213

        self.winner = None

        self.board = []
        for _ in range(7):
            self.board.append([0]*7)

        self.player_a = socket.socket()
        self.player_a.bind(('', PORT_A))
        self.player_a.listen(5)

        self.player_b = socket.socket()
        self.player_b.bind(('', PORT_B))
        self.player_b.listen(5)

        self.current_turn = False

        self.game_loop()

    def game_loop(self):
        current_player = None

        a, _ = self.player_a.accept()
        b, _ = self.player_b.accept()

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
        

    def check_spot(self, row, col):
        for i in range(4):
            
            if i + row > 0 and i + row <= self.ROW_NUM:
                if 