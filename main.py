import chess
from movepicker import getAIMove

board = chess.Board()
depth = 5
aiIsWhite = False

side = input("Enter AI side: ")
aiIsWhite = side == 'white'
if aiIsWhite:
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), True)
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
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), aiIsWhite)
    board.push(aiMove)
    print("Blunder Bot played " + str(aiMove))
    print(board)
    if board.is_game_over():
        print('AI wins!')
        break
