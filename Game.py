import Board
import math
from random import seed, randint
from copy import copy, deepcopy


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
        mx, my = self.board.detectClick()
        if (mx>=200 and mx <=300) and (my>=425 and my <=475):   #detected button new game
            self.board.setWholeBoardToDefault()
            print("New game!")
            return -1, -1
        row = math.floor((my-100)/100)
        col = math.floor((mx-100)/100)
        if row >= 3 or col >= 3 or row < 0 or col < 0:
            return -1, -1
        return row, col

    def makeMove(self):
        row = -1
        col = -1
        if not self.AI:
            while row == -1 and col == -1:
                row, col = self.detectRect()
        else:
            if self.board.numOfFreeSpacesLeft() == 9:
                row = 0
                col = 0
            else:
                row, col = self.findBestMove()
        if row > -1:
            control = 1
        if control > 0:
            control = self.board.fillNumInBoard(row,col,self.id)
        if control:
            self.board.drawSymbol(self.id, row, col)
        return control


    def findBestMove(self):
        boardik_ref = Board.Board(self.board.board)     #reference
        nextmove = AI_Move(boardik_ref)
        return nextmove.findBestMove()


class AI_Move:
    board = 0
    posRow = -1
    posCol = -1

    def __init__(self,board):
        self.board = deepcopy(board)

    def minimax(self,level,max_status):
        score, resultEval = self.evaluate(level)

        if resultEval:
            self.board.status = 0
            return score

        if max_status:
            best = -1000
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board.board[i][j] == 0:
                        self.board.fillNumInBoard(i, j, 2)  #maximizer is ID 2
                        best = max(best, self.minimax(level+1, not max_status))
                        self.board.board[i][j] = 0
            return best
        else:
            best = 1000
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board.board[i][j] == 0:
                        self.board.fillNumInBoard(i, j, 1)  # minimizer is ID 1
                        best = min(best, self.minimax(level+1, not max_status))
                        self.board.board[i][j] = 0
            return best

    def findBestMove(self):
            best = -1000
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board.board[i][j] == 0:
                        self.board.fillNumInBoard(i, j, 2)  #maximizer is ID 1
                        move = self.minimax(0, False)
                        self.board.board[i][j] = 0  #remove move
                        if move > best:
                            self.posCol = j
                            self.posRow = i
                            print("Find new better move: [", i, "] [", j, "] with score:", move, " old: ", best)
                            best = move
            return self.posRow, self.posCol

    def evaluate(self, level):
        self.board.checkAll()   #check it first
        if self.board.status == 1:
            return -10 + level, True
        elif self.board.status == 2:
            return 10 - level, True
        elif self.board.status == 3:
            return 0, True
        else:
            return -1, False


class Game:
    board = None
    players = [None,None]
    activePlayer = Player(0, None, "A")
    winner = "None"

    def __init__(self, board):
        self.board = board
        self.players[0] = Player(1, self.board, "Marko")
        self.players[1] = Player(2, self.board, "AI", True) #True
        self.activePlayer = self.players[randint(0, 1)]

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
                self.switchPlayer()
        self.activePlayer.detectRect()

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

