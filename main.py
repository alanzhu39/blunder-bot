import chess
import time
from movepicker import getAIMove, alphabetaWithMove, visited, maxVisited, minVisited

board = chess.Board()
depth = 4
aiIsWhite = False
start = 0
stop = 0

side = input("Enter AI side: ")
aiIsWhite = side == 'white'
if aiIsWhite:
    start = time.perf_counter()
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), True, True)[0]
    stop = time.perf_counter()
    print("Blunder Bot played " + str(aiMove) + " in " + str(stop - start) + " seconds.")
    board.push(aiMove)
    print(board)

while True:
    humanMove = input("Please enter your move: ")
    if humanMove == 'exit':
        exit()
    humanMove = chess.Move.from_uci(humanMove)
    board.push(humanMove)
    if board.is_game_over():
        print('Human wins!')
        break
    maxVisited = {}
    minVisited = {}
    start = time.perf_counter()
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), aiIsWhite, True)[0]
    stop = time.perf_counter()
    print("Blunder Bot played " + str(aiMove) + " in " + str(stop - start) + " seconds.")
    board.push(aiMove)
    print("Blunder Bot played " + str(aiMove))
    print(board)
    if board.is_game_over():
        print('AI wins!')
        break
