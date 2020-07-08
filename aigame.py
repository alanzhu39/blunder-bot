import chess
import time

visited = {}

# White is max, black is min, returns (move, value) tuple
def alphabetaWithMove(board, depth, alpha, beta, isWhite, useVisited):
    boardFEN = board.fen()
    toggle = False
    if depth == 0 or board.is_game_over():
        if not useVisited:
            return evaluate(board)
        elif boardFEN not in visited:
            visited[boardFEN] = evaluate(board)
        return (None, visited[boardFEN])
    if isWhite:
        value = -float('inf')
        bestMove = None
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            if boardFEN in visited and toggle:
                newVal = visited[boardFEN]
            else:
                newVal = alphabetaWithMove(board, depth - 1, alpha, beta, False, useVisited)[1]
            if newVal > value:
                bestMove = move
            value = max(value, newVal)
            board.pop()
            alpha = max(alpha, value)
            if alpha > beta:
                break
        return (bestMove, value)
    else:
        value = float('inf')
        bestMove = None
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            if boardFEN in visited and toggle:
                newVal = visited[boardFEN]
            else:
                newVal = alphabetaWithMove(board, depth - 1, alpha, beta, True, useVisited)[1]
            if newVal < value:
                bestMove = move
            value = min(value, newVal)
            board.pop()
            beta = min(beta, value)
            if beta < alpha:
                break
        return (bestMove, value)

board = chess.Board()
depth = 4
start = 0
stop = 0
white = True

while True:
    visited = {}
    start = time.perf_counter()
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), white, white)[0]
    stop = time.perf_counter()
    side = "White" if white else "Black"
    print(side + " played " + str(aiMove) + " in " + str(stop - start) + " seconds.")
    board.push(aiMove)
    white = not white
    if board.is_game_over():
        print('AI wins!')
        break
