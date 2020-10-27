import Board
import math
from random import seed,randint


class Player:
    board = None
    id = 0
    name = None
    AI = False

    def __init__(self, id, board, name, AI = False):
        self.id = id
        self.board = board
        self.name = name
        self.AI = AI

    def detectRect(self):
        mx,my = self.board.detectClick()
        row = math.floor((my-100)/100)
        col = math.floor((mx-100)/100)
        if row >= 3 or col >= 3 or row < 0 or col < 0:
            return -1, -1
        return row, col

    def makeMove(self):
        if not self.AI:
            row, col = self.detectRect()
            if row == -1:
                control = 0
            else:
                control = 1
            if control > 0:
                control = self.board.fillNumInBoard(row,col,self.id)
            if control:
                self.board.drawSymbol(self.id, row, col)
            return control
        else:
            self.findBestMove()


    def findBestMove(self):
        boardik = Board.MiniBoard(self.board)
        boardik.fillNumInBoard(1 , 1 , 2)
        boardik.printBoard()
        return 1


class Game:
    board = None
    players = [None,None]
    activePlayer = Player(0, None, "A")
    winner = "None"

    def __init__(self, board):
        self.board = board
        self.players[0] = Player(1, self.board, "Marko")
        self.players[1] = Player(2, self.board, "AI", True)
        self.activePlayer = self.players[randint(0,1)]

    def switchPlayer(self):
        if self.activePlayer == self.players[0]:
            self.activePlayer = self.players[1]
            return 2
        else:
            self.activePlayer = self.players[0]
            return 1

    def main(self):
        while not self.isGameEnded():
            control = 0
            while not control:
                control = self.activePlayer.makeMove()
                if not self.isGameEnded():
                    self.switchPlayer()
        return self.activePlayer.name

    def dedicateWinner(self):
        if self.board.status == 1:
            print("Winner is", self.players[0].name)
            self.winner = self.players[0].name
        elif self.board.status == 2:
            print("Winner is", self.players[1].name)
            self.winner = self.players[1].name
        elif self.board.status == 3:
            print("DRAW")
        else:
            print("None")
        self.board.showWinner(self.winner)

    def isGameEnded(self):
        self.board.checkAll()
        if self.board.status != 0:
            self.dedicateWinner()
            return True
        else:
            print("Game is not over yet!")
            return False

