# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pygame.locals import *
import argparse
import pygame, sys, Board, Game
#argparsing for turning on
val = True
parser = argparse.ArgumentParser()
parser.add_argument("AI", help="Do you want to use AI? [Yes / No]", default="true", nargs='?')
args = parser.parse_args()
result = args.AI.lower()

if result == "no":
    val = False
else:
    print("Bad argument, using default [AI is enabled]")

boardik = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
board = Board.GraphicalBoard(boardik)
board.printBoard()
game = Game.Game(board, val)
while True:
    game.main()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
