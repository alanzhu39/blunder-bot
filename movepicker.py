from evaluate import evaluate

# White is max, black is min
def alphabeta(board, depth, alpha, beta, isWhite):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    if isWhite:
        value = -float('inf')
        copy = board.legal_moves.copy()
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
        copy = board.legal_moves.copy()
        for move in copy:
            board.push(move)
            value = min(value, alphabeta(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
