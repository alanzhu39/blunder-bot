import chess

# Positive evaluation means favors white, negative favors black
def evaluate(board):
    evaluation = 0
    weights = {}
    weights[gameOver] = 1
    weights[material] = 2
    weights[badPawns] = 1
    weights[centerPawns] = 0.8
    for func in weights:
        evaluation += weights[func] * func(board)
    return evaluation

# 200 for mate
def gameOver(board):
    if board.is_game_over() and board.is_checkmate():
        side = board.turn
        if side == chess.WHITE:
            return 200
        return -200
    return 0

# Pure material advantage by points
def material(board):
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    values = [1, 3, 3, 5, 9]
    result = 0
    for i in range(len(pieces)):
        result += len(board.pieces(pieces[i], chess.WHITE)) * values[i]
        result -= len(board.pieces(pieces[i], chess.BLACK)) * values[i]
    return result

# Detects doubled and isolated pawns, -0.5 for each
def badPawns(board):
    result = 0
    whitePawns = board.pieces(chess.PAWN, chess.WHITE)
    blackPawns = board.pieces(chess.PAWN, chess.WHITE)
    whiteFileCount = [len(whitePawns.intersection(file)) for file in chess.BB_FILES]
    blackFileCount = [len(blackPawns.intersection(file)) for file in chess.BB_FILES]
    # Doubled pawns
    for i in range(len(whiteFileCount)):
        count = whiteFileCount[i]
        if count > 1:
            result -= 0.5 * (count - 1)
        count = blackFileCount[i]
        if count > 1:
            result += 0.5 * (count - 1)
    # Isolated pawns
    for i in range(len(chess.BB_FILES)):
        if whiteFileCount[i] > 0:
            isolated = True
            if i > 0:
                isolated = isolated and whiteFileCount[i - 1] == 0
            if i < len(chess.BB_FILES) - 1:
                isolated = isolated and whiteFileCount[i + 1] == 0
            if isolated:
                result -= 0.5 * whiteFileCount[i]
        if blackFileCount[i] > 0:
            isolated = True
            if i > 0:
                isolated = isolated and blackFileCount[i - 1] == 0
            if i < len(chess.BB_FILES) - 1:
                isolated = isolated and blackFileCount[i + 1] == 0
            if isolated:
                result += 0.5 * blackFileCount[i]
    return result

# 1 point for each pawn in the center
def centerPawns(board):
    result = 0
    result += len(chess.BB_CENTER.intersection(board.pieces(chess.PAWN, chess.WHITE)))
    result -= len(chess.BB_CENTER.intersection(board.pieces(chess.PAWN, chess.BLACK)))
    return result
