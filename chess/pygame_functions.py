import pygame
from consts import Consts
import chess
from consts import Consts
from custom_engine import get_custom_move_scores, get_best_move


class PygameFunctions():
    @staticmethod
    def load_and_scale_images():
        scaled_images = {}
        for symbol, filename in Consts.PIECE_IMAGES.items():
            image = pygame.image.load(f'assets/{filename}')
            scaled_image = pygame.transform.scale(
                image, (Consts.SQUARE_SIZE, Consts.SQUARE_SIZE))
            scaled_images[symbol] = scaled_image
        return scaled_images

    @staticmethod
    def draw_info_box(screen, engine_name, depth):
        info_text = f"Engine: {engine_name} | Depth: {depth}"
        info_surface = Consts.FONT.render(
            info_text, True, pygame.Color('black'), pygame.Color('white'))
        screen.blit(info_surface, (20, 20))

    @staticmethod
    def draw_board(screen, board, move_scores, selected_square, engine_name, depth):
        SCALED_PIECE_IMAGES = PygameFunctions.load_and_scale_images()
        for row in range(8):
            for col in range(8):
                color = Consts.COLORS[(row + col) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(
                    col * Consts.SQUARE_SIZE, row * Consts.SQUARE_SIZE, Consts.SQUARE_SIZE, Consts.SQUARE_SIZE))
                piece = board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_image = SCALED_PIECE_IMAGES[piece.symbol()]
                    screen.blit(
                        piece_image, (col * Consts.SQUARE_SIZE, row * Consts.SQUARE_SIZE))

        if selected_square is not None:
            col = chess.square_file(selected_square)
            row = 7 - chess.square_rank(selected_square)
            pygame.draw.rect(screen, pygame.Color('blue'),
                             pygame.Rect(col * Consts.SQUARE_SIZE, row * Consts.SQUARE_SIZE, Consts.SQUARE_SIZE, Consts.SQUARE_SIZE), 3)

        grouped_moves = {}
        for move, score in move_scores.items():
            to_square = move.to_square
            if to_square not in grouped_moves:
                grouped_moves[to_square] = []
            grouped_moves[to_square].append((move, score))

        for to_square, moves in grouped_moves.items():
            to_col = chess.square_file(to_square)
            to_row = 7 - chess.square_rank(to_square)

            best_move, best_score = min(moves, key=lambda x: x[1])

            piece = board.piece_at(best_move.from_square)
            piece_symbol = piece.symbol().upper() if piece else ''
            dest_square_name = chess.square_name(best_move.to_square)
            move_info = f"{piece_symbol} {dest_square_name}: {best_score}"

            if best_score == min(move_scores.values()):
                text_color = pygame.Color('yellow')
            else:
                text_color = pygame.Color(
                    'red') if best_score > 0 else pygame.Color('green')
            text = Consts.FONT.render(move_info, True, text_color)
            text_rect = text.get_rect(
                center=(to_col * Consts.SQUARE_SIZE + Consts.SQUARE_SIZE / 2, to_row * Consts.SQUARE_SIZE + Consts.SQUARE_SIZE / 2))
            screen.blit(text, text_rect.topleft)

        PygameFunctions.draw_info_box(screen, engine_name, depth)

    @staticmethod
    def get_stockfish_move_scores(board, depth=2):
        engine = chess.engine.SimpleEngine.popen_uci(Consts.STOCKFISH_PATH)
        move_scores = {}

        for move in board.legal_moves:
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(depth=depth))
            score = info["score"].relative.score(mate_score=10000)
            move_scores[move] = score
            board.pop()
        engine.quit()
        return move_scores

    @staticmethod
    def get_move_scores(board, depth=2, use_stockfish=True):
        if use_stockfish:
            return PygameFunctions.get_stockfish_move_scores(board, depth)
        else:
            return get_custom_move_scores(board, depth)

    @staticmethod
    def get_square_under_mouse(board):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // Consts.SQUARE_SIZE
        row = 7 - (mouse_pos[1] // Consts.SQUARE_SIZE)
        square = chess.square(col, row)
        piece = board.piece_at(square)
        return square, piece
