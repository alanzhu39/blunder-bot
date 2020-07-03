import chess
from movepicker import alphabeta

board = chess.Board()
depth = 3
aiIsWhite = False

side = input("Enter AI side: ")
aiIsWhite = side == 'white'
if aiIsWhite:
    aiMove = alphabeta(board, depth, -float('inf'), float('inf'), True)
    board.push(aiMove)

while True:
    humanMove = input("Please enter your move: ")
    while humanMove not in board.legal_moves:
        if humanMove == 'exit':
            break
        if humanMove == 'print':
            print(board)
        humanMove = input("Please enter your move: ")
    board.push(humanMove)
    if board.is_game_over():
        print('Human wins!')
        break
    aiMove = alphabeta(board, depth, -float('inf'), float('inf'), aiIsWhite)
    board.push(aiMove)
    if board.is_game_over():
        print('AI wins!')
        break
