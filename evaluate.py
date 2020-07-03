import chess

# Positive evaluation means favors white, negative favors black
def evaluate(board):
    evaluation = 0
    weights = {}
    weights[gameOver] = 1
    weights[material] = 2
    weights[badPawns] = 1
    weights[centerPawns] = 0.8
    weights[knights] = 0.9
    weights[bishops] = 0.9
    weights[rooks] = 0.75
    weights[queens] = 0.9
    weights[kings] = 0.8
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
    result += len(board.pieces(chess.PAWN, chess.WHITE).intersection(chess.BB_CENTER))
    result -= len(board.pieces(chess.PAWN, chess.BLACK).intersection(chess.BB_CENTER))
    return result

# Various knight evaluations
def knights(board):
    result = 0
    whiteKnights = board.pieces(chess.KNIGHT, chess.WHITE)
    blackKnights = board.pieces(chess.KNIGHT, chess.BLACK)
    whitePawns = board.pieces(chess.PAWN, chess.WHITE)
    blackPawns = board.pieces(chess.PAWN, chess.WHITE)
    # Penalty as pawns disappear
    result -= len(whiteKnights) * 0.05 * (8 - len(whitePawns))
    result += len(blackKnights) * 0.05 * (8 - len(blackPawns))
    # Pawn defender bonus
    for sq in whiteKnights:
        result += 0.5 * len(board.attackers(chess.WHITE, sq).intersection(whitePawns))
    for sq in blackKnights:
        result -= 0.5 * len(board.attackers(chess.BLACK, sq).intersection(blackPawns))
    # Knight mobility
    for sq in whiteKnights:
        for attacking in board.attacks(sq):
            if len(board.attackers(chess.BLACK, attacking).intersection(blackPawns)) == 0:
                result += 0.1
    for sq in blackKnights:
        for attacking in board.attacks(sq):
            if len(board.attackers(chess.WHITE, attacking).intersection(whitePawns)) == 0:
                result -= 0.1
    return result

# Various bishop evaluations
def bishops(board):
    result = 0
    whiteBishops = board.pieces(chess.BISHOP, chess.WHITE)
    blackBishops = board.pieces(chess.BISHOP, chess.BLACK)
    whitePawns = board.pieces(chess.PAWN, chess.WHITE)
    blackPawns = board.pieces(chess.PAWN, chess.WHITE)
    # Bad bishop: bishop mobility restricted by own pawn
    for sq in whiteBishops:
        if chess.square_rank(sq) > 6:
            continue
        ranks = 0
        for rank in chess.BB_RANKS[chess.square_rank(sq) + 1:]:
            ranks = ranks | int(rank)
        files = 0
        for file in chess.BB_FILES[max(chess.square_file(sq) - 2, 0):min(chess.square_file(sq) + 3, 8)]:
            files = ranks | int(file)
        blockers = board.attacks(sq).intersection( \
            chess.SquareSet(ranks).intersection(chess.SquareSet(files)))
        result -= 0.1 * len(blockers.intersection(whitePawns))
    for sq in blackBishops:
        if chess.square_rank(sq) < 1:
            continue
        ranks = 0
        for rank in chess.BB_RANKS[:chess.square_rank(sq) - 1]:
            ranks = ranks | int(rank)
        files = 0
        for file in chess.BB_FILES[max(chess.square_file(sq) - 2, 0):min(chess.square_file(sq) + 3, 8)]:
            files = ranks | int(file)
        blockers = board.attacks(sq).intersection( \
            chess.SquareSet(ranks).intersection(chess.SquareSet(files)))
        result += 0.1 * len(blockers.intersection(blackPawns))
    # Bishop pair bonus
    if len(whiteBishops) == 2:
        result += 0.5
    if len(blackBishops) == 2:
        result -= 0.5
    return result

# Various rook evaluations
def rooks(board):
    result = 0
    whiteRooks = board.pieces(chess.ROOK, chess.WHITE)
    blackRooks = board.pieces(chess.ROOK, chess.BLACK)
    whitePawns = board.pieces(chess.PAWN, chess.WHITE)
    blackPawns = board.pieces(chess.PAWN, chess.WHITE)
    # Increasing value as pawns disappear
    result += len(whiteRooks) * 0.05 * (8 - len(whitePawns))
    result -= len(blackRooks) * 0.05 * (8 - len(blackPawns))
    # Open and semi-open file bonus
    for sq in whiteRooks:
        if len(whitePawns.intersection(chess.square_file(sq))) == 0:
            result += 0.15
            if len(blackPawns.intersection(chess.square_file(sq))) == 0:
                result += 0.25
    for sq in blackRooks:
        if len(blackPawns.intersection(chess.square_file(sq))) == 0:
            result -= 0.15
            if len(whitePawns.intersection(chess.square_file(sq))) == 0:
                result -= 0.25
    # 7th rank bonus
    for sq in whiteRooks:
        if chess.square_rank(sq) == chess.BB_RANK_7:
            result += 0.3
    for sq in blackRooks:
        if chess.square_rank(sq) == chess.BB_RANK_2:
            result -= 0.3
    # Enemy queen in same file bonus
    whiteQueen = board.pieces(chess.QUEEN, chess.WHITE)
    blackQueen = board.pieces(chess.QUEEN, chess.BLACK)
    for sq in blackQueen:
        result += len(whiteRooks.intersection(chess.square_file(sq))) * 0.1
    for sq in whiteQueen:
        result -= len(blackRooks.intersection(chess.square_file(sq))) * 0.1
    # Rooks defending each other bonus
    defended = False
    for sq in whiteRooks:
        if len(whiteRooks.intersection(board.attacks(sq))) > 0:
            defended = True
            break
    if defended:
        result += 0.2
    defended = False
    for sq in blackRooks:
        if len(blackRooks.intersection(board.attacks(sq))) > 0:
            defended = True
            break
    if defended:
        result -= 0.2
    return result

# Various queen evaluations
def queens(board):
    return 0

# Various king evaluations
def kings(board):
    return 0
