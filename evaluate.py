# Positive evaluation means favors white, negative favors black

def evaluate(board):
    evaluation = 0
    weights = {}
    weights[gameOver] = 1
    weights[material] = 2
    for func in weights:
        evaluation += weights[func] * func(board)
    return evaluation

def gameOver(board):
    if board.is_game_over() and board.is_checkmate():
        side = board.turn
        if side == chess.WHITE:
            return 200
        return -200
    return 0

def material(board):
    evaluation = 
