import chess
from movepicker import getAIMove, alphabetaWithMove, visited

board = chess.Board()
depth = 4
aiIsWhite = False

side = input("Enter AI side: ")
aiIsWhite = side == 'white'
if aiIsWhite:
    aiMove = getAIMove(board, depth, True)
    print("Blunder Bot played " + str(aiMove))
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
    visited = {}
    aiMove = getAIMove(board, depth, aiIsWhite)
    board.push(aiMove)
    print("Blunder Bot played " + str(aiMove))
    print(board)
    if board.is_game_over():
        print('AI wins!')
        break
