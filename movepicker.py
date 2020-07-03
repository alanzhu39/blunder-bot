import chess
from evaluate import evaluate

# Performs action selection by doing alphabeta search on all children
def getAIMove(board, depth, isWhite):
    if isWhite:
        bestMove = None
        bestVal = -float('inf')
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            search = alphabeta(board, depth - 1, -float('inf'), float('inf'), False)
            if search > bestVal:
                bestVal = search
                bestMove = move
            board.pop()
        return bestMove
    else:
        bestVal = float('inf')
        bestMove = None
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            search = alphabeta(board, depth - 1, -float('inf'), float('inf'), True)
            if search < bestVal:
                bestVal = search
                bestMove = move
            board.pop()
        return bestMove

visited = {}

# White is max, black is min, returns (move, value) tuple
def alphabeta(board, depth, alpha, beta, isWhite):
    if depth == 0 or board.is_game_over():
        boardFEN = board.fen()
        if boardFEN not in visited:
            visited[boardFEN] = evaluate(board)
        return evaluate(board)
    if isWhite:
        value = -float('inf')
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            value = max(value, alphabeta(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            value = min(value, alphabeta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

# White is max, black is min, returns (move, value) tuple
def alphabetaWithMove(board, depth, alpha, beta, isWhite):
    if depth == 0 or board.is_game_over():
        boardFEN = board.fen()
        if boardFEN not in visited:
            visited[boardFEN] = evaluate(board)
        return (None, visited[boardFEN])
    if isWhite:
        value = -float('inf')
        lastMove = None
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            lastMove = move
            value = max(value, alphabetaWithMove(board, depth - 1, alpha, beta, False)[1])
            board.pop()
            alpha = max(alpha, value)
            if alpha > beta:
                break
        return (lastMove, value)
    else:
        value = float('inf')
        lastMove = None
        copy = [move for move in board.legal_moves]
        for move in copy:
            board.push(move)
            lastMove = move
            value = min(value, alphabetaWithMove(board, depth - 1, alpha, beta, True)[1])
            board.pop()
            beta = min(beta, value)
            if beta < alpha:
                break
        return (lastMove, value)
