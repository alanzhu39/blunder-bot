import chess
import time
from evaluate import evaluate

visited = {}

# White is max, black is min, returns (move, value) tuple
def alphabetaWithMove(board, depth, alpha, beta, isWhite, useVisited):
    boardFEN = board.fen()
    if depth == 0 or board.is_game_over():
        if not useVisited:
            return (None, evaluate(board))
        elif boardFEN not in visited:
            visited[boardFEN] = (0, evaluate(board), None)
        return (None, visited[boardFEN][1])
    if isWhite:
        value = -float('inf')
        bestMove = None
        copy = [move for move in board.legal_moves]
        if boardFEN in visited and visited[boardFEN][0] >= depth:
            value = visited[boardFEN][1]
            bestMove = visited[boardFEN][2]
        else:
            for move in copy:
                board.push(move)
                newVal = alphabetaWithMove(board, depth - 1, alpha, beta, False, useVisited)[1]
                if newVal > value:
                    bestMove = move
                value = max(value, newVal)
                board.pop()
                alpha = max(alpha, value)
                if alpha > beta:
                    break
            if useVisited:
                visited[boardFEN] = (depth, value, bestMove)
        return (bestMove, value)
    else:
        value = float('inf')
        bestMove = None
        copy = [move for move in board.legal_moves]
        if boardFEN in visited and visited[boardFEN][0] >= depth:
            value = visited[boardFEN][1]
            bestMove = visited[boardFEN][2]
        else:
            for move in copy:
                board.push(move)
                newVal = alphabetaWithMove(board, depth - 1, alpha, beta, True, useVisited)[1]
                if newVal < value:
                    bestMove = move
                value = min(value, newVal)
                board.pop()
                beta = min(beta, value)
                if beta < alpha:
                    break
            if useVisited:
                visited[boardFEN] = (depth, value, bestMove)
        return (bestMove, value)

board = chess.Board()
depth = 4
start = 0
stop = 0
isWhite = True
side = "White" if isWhite else "Black"
blackTimes = []
whiteTimes = []

while True:
    visited = {}
    repeats.add(board.fen())
    start = time.perf_counter()
    aiMove = alphabetaWithMove(board, depth, -float('inf'), float('inf'), isWhite, not isWhite)[0]
    stop = time.perf_counter()
    side = "White" if isWhite else "Black"
    if isWhite:
        whiteTimes.append(stop - start)
    else:
        blackTimes.append(stop - start)
    print(side + " played " + str(aiMove) + " in " + str(stop - start) + " seconds.")
    board.push(aiMove)
    isWhite = not isWhite
    if board.is_game_over():
        print(side + ' wins!')
        break
    elif len(board.move_stack) >= 30:
        break

print("Average white time (not using visited): " + str(sum(whiteTimes)/len(whiteTimes)))
print("Average black time (using visited): " + str(sum(blackTimes)/len(blackTimes)))
