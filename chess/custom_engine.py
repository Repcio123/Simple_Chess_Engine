from random import random
from consts import Consts
import chess
import chess.engine
from pieces import PIECE_VALUES, CENTER_SQUARES, PIECE_SQUARE_TABLE


def evaluate_board(board):
    score = 0
    if board.is_checkmate() and board.turn == chess.WHITE:
        return float('inf')
    if board.is_checkmate() and board.turn == chess.BLACK:
        return -float('inf')
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.piece_type
            color = piece.color
            score += PIECE_VALUES[piece_type] if color == chess.WHITE else - \
                PIECE_VALUES[piece_type]
            if piece_type in PIECE_SQUARE_TABLE:
                if color == chess.WHITE:
                    score += PIECE_SQUARE_TABLE[piece_type][square]
                else:
                    score -= PIECE_SQUARE_TABLE[piece_type][chess.square_mirror(
                        square)]
            if square in CENTER_SQUARES and piece_type in (chess.KNIGHT, chess.BISHOP):
                score += 10
            if square == 27 and piece_type == chess.PAWN:
                score += 20
            if square == 28 and piece_type == chess.PAWN:
                score += 20
            if color == chess.WHITE:
                if piece_type in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT):
                    attackers = board.attackers(chess.BLACK, square)
                    if attackers:
                        score += 10
            else:
                if piece_type in (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT):
                    attackers = board.attackers(chess.WHITE, square)
                    if attackers:
                        score -= 10
    return score


def get_best_move(board, depth):
    best_score = float('inf')
    best_moves = []
    for move in board.legal_moves:
        board.push(move)
        score = negamax(board, depth - 1, -float('inf'), float('inf'))
        board.pop()
        if score < best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
    return random.choice(best_moves), best_score


def is_good_move(board, move):

    piece_type_moved = board.piece_type_at(move.from_square)
    piece_type_captured = board.piece_type_at(move.to_square)
    if piece_type_captured is not None and PIECE_VALUES.get(piece_type_captured, 0) > Consts.VALUE_THRESHOLD:
        return True

    board.push(move)
    new_position_score = evaluate_board(board)
    board.pop()

    return new_position_score > evaluate_board(board)


def negamax(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.pop()
        beta = min(beta, score)
        if alpha >= beta:
            break

    return beta


def get_custom_move_scores(board, depth):
    move_scores = {}
    for move in board.legal_moves:
        board.push(move)
        score = negamax(board, depth - 1, -float('inf'), float('inf'))
        move_scores[move] = -score
        board.pop()
    return move_scores
