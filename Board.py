from array import *
import math
import pygame, sys
from pygame.locals import *

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Board:
    "Board class that contains all info about it"
    sizeOfBoard = 3
    numOfElementsToWin = 3      #number of elements in row, col on diagonal that will mean one / or other player have won
    status = 0
    DISPLAY = None
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]   #board

    def __init__(self, board):
        self.board = board

    def printBoard(self):
        print("BOARD")
        for a in self.board:
            for b in a:
                print(b, end=" ")
            print()

    def fillNumInBoard(self,posR,posC,num):
        if self.board[posR][posC] == 0:
            self.board[posR][posC] = num
            return 1
        return 0

    def setWholeBoardToDefault(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.status = 0

    def pickRow(self,numOfRow):
        row = [0, 0, 0]
        for i in range(0, self.sizeOfBoard):
            row[i] = self.board[numOfRow][i]
        return row

    def pickCol(self,numOfCol):
        col = [0, 0, 0]
        for i in range(0, 3):
            col[i] = self.board[i][numOfCol]
        return col

    def pickMainDiagonal(self):
        dg = [0, 0, 0]
        for i in range(0, self.sizeOfBoard):
            dg[i] = self.board[i][i]
        return dg

    def picksideDiagonal(self):         #there is possibility of checking sizeOf, this is easier for this
        return [self.board[0][2], self.board[1][1], self.board[2][0]]

    def checkRows(self):
        for i in range(0,self.sizeOfBoard):
            status = self.check(self.pickRow(i))
            if status != 0:
                self.status = status
                break

    def checkCols(self):
        for i in range(0,self.sizeOfBoard):
            status = self.check(self.pickCol(i))
            if status != 0:
                self.status = status
                break

    def checkDiagonals(self):
        status = self.check(self.pickMainDiagonal())
        if status != 0:
            self.status = status
        else:
            status = self.check(self.picksideDiagonal())
            if status != 0:
                self.status = status

    def checkForDraw(self):
        if not self.isThereFreeSpace():
            self.status = 3

    def isThereFreeSpace(self):
        for i in self.board:
            for j in i:
                if j == 0:
                    return True
        return False

    def numOfFreeSpacesLeft(self):
        num = 0
        for i in self.board:
            for j in i:
                if j == 0:
                    num += 1
        return num

    def findNextFreeSpace(self):
        num = self.numOfFreeSpacesLeft()
        if num > 0:
            for i in self.board:
                for j in i:
                    if j == 0:
                        return num, i, j
        return num

    def checkAll(self):
        self.checkRows()
        if self.status == 0:
            self.checkCols()
        if self.status == 0:
            self.checkDiagonals()
        if self.status == 0:
            self.checkForDraw()

    def check(self, sequence):
        first = sequence[0]
        checksum = 0
        for i in sequence:
            if first != i or first == 0:
                return 0
            elif first == 1 and first == i:
                checksum += 1
            elif first == 2 and first == i:
                checksum += 2

        if checksum == 3:
            return 1
        elif checksum == 6:
            return 2
        else:
            return 0


class GraphicalBoard(Board):
    def __init__(self, board):
        self.DISPLAY = self.drawEmptyBoard()
        self.showWinner()

    def setWholeBoardToDefault(self):
        super().setWholeBoardToDefault()
        self.DISPLAY = self.drawEmptyBoard()
        self.showWinner()

    def drawEmptyBoard(self):
        pygame.init()
        DISPLAY = pygame.display.set_mode((500, 500), 0, 32)
        # colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (0, 255, 0)


        DISPLAY.fill(WHITE)

        for j in range(0, 3):
            for i in range(0, 3):
                stx = i * 100 + 100
                sty = j * 100 + 100
                pygame.draw.rect(DISPLAY, BLACK, (stx, sty, 100, 100), 2)
        pygame.draw.rect(DISPLAY, BLACK, (200, 425, 100, 50))
        pygame.draw.rect(DISPLAY, WHITE, (205, 430, 90, 40))
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render('Play again', True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (250, 450)
        DISPLAY.blit(text, textRect)

        pygame.display.update()
        return DISPLAY

    def drawSymbol(self, id, row, col):
        RED = (255,0,0)
        BLUE = (0,0,255)
        row = row*100 + 100
        col = col*100 + 100

        if id == 1:
            sty = row + 20
            stx = col + 20
            fy = row + 80
            fx = col + 80
            st = (stx,sty)
            f = (fx,fy)
            pygame.draw.line(self.DISPLAY, RED, st, f, 1)
            sty = row + 80
            stx = col + 20
            fy = row + 20
            fx = col + 80
            st = (stx, sty)
            f = (fx, fy)
            pygame.draw.line(self.DISPLAY, RED, st, f, 1)
        else:
            px = col + 50
            py = row + 50
            pos = (px, py)
            pygame.draw.circle(self.DISPLAY, BLUE, pos, 30, 1)
        pygame.display.update()

    def showWinner(self, winner="Game On"):

        pygame.draw.rect(self.DISPLAY,WHITE,(20, 20, 400, 80))

        font = pygame.font.Font('freesansbold.ttf', 32)

        if self.status == 0:
            text = font.render('Game is on', True, GREEN, WHITE)
            textRect = text.get_rect()
            textRect.center = (250, 50)
            self.DISPLAY.blit(text, textRect)
        elif self.status == 1 or self.status == 2:
            text = font.render('Winner is: ', True, BLACK, WHITE)
            textRect = text.get_rect()
            textRect.center = (180, 50)
            self.DISPLAY.blit(text, textRect)
            if self.status == 1:
                text = font.render(winner, True, RED, WHITE)
            else:
                text = font.render(winner, True, BLUE, WHITE)
            textRect = text.get_rect()
            textRect.center = (320, 50)
            self.DISPLAY.blit(text, textRect)
        else:
            text = font.render('DRAW', True, GREEN, WHITE)
            textRect = text.get_rect()
            textRect.center = (250, 50)
            self.DISPLAY.blit(text, textRect)

        pygame.display.update()

    def detectClick(self):
        left_click = False

        while True:  # while player nepickne
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_click = True
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        left_click = False
            if left_click:
                return mx, my

