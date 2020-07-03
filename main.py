import chess
from movepicker import getAIMove

board = chess.Board()
depth = 5
aiIsWhite = False

side = input("Enter AI side: ")
aiIsWhite = side == 'white'
if aiIsWhite:
    aiMove = getAIMove(board, depth, True)
    print("Blunder Bot played " + str(aiMove))
    board.push(aiMove)

while True:
    humanMove = input("Please enter your move: ")
    if humanMove == 'exit':
        exit()
    while humanMove == 'print' or humanMove == 'exit':
        if humanMove == 'exit':
            exit()
        print(board)
        humanMove = input("Please enter your move: ")
    humanMove = chess.Move.from_uci(humanMove)
    board.push(humanMove)
    if board.is_game_over():
        print('Human wins!')
        break
    aiMove = getAIMove(board, depth, aiIsWhite)
    board.push(aiMove)
    print("Blunder Bot played " + str(aiMove))
    if board.is_game_over():
        print('AI wins!')
        break
