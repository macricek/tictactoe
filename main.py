# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pygame.locals import *
import pygame, sys, Board, Game
boardik = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


board = Board.GraphicalBoard(boardik)
board.printBoard()
game = Game.Game(board)
while True:
    game.main()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
