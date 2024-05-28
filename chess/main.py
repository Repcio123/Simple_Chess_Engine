import pygame
import chess
import chess.engine

from consts import Consts
from pygame_functions import PygameFunctions

pygame.init()


def main():
    screen = pygame.display.set_mode((Consts.WIDTH, Consts.HEIGHT))
    pygame.display.set_caption("Prosty silnik szachowy")
    board = chess.Board()
    depth = 2
    use_stockfish = True
    engine_info = 'Stockfish' if use_stockfish else 'Deep Search'
    move_scores = PygameFunctions.get_move_scores(board, depth, use_stockfish)

    selected_square = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                square, piece = PygameFunctions.get_square_under_mouse(board)
                if selected_square is None:
                    if piece is not None and piece.color == board.turn:
                        selected_square = square
                else:
                    move = chess.Move(
                        from_square=selected_square, to_square=square)
                    if move in board.legal_moves:
                        board.push(move)
                        move_scores = PygameFunctions.get_move_scores(
                            board, depth, use_stockfish)
                    selected_square = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    depth = depth + 1 if depth < 4 else 1
                    move_scores = PygameFunctions.get_move_scores(
                        board, depth, use_stockfish)
                elif event.key == pygame.K_e:
                    use_stockfish = not use_stockfish
                    engine_info = 'Stockfish' if use_stockfish else 'Deep Search'
                    move_scores = PygameFunctions.get_move_scores(
                        board, depth, use_stockfish)

        PygameFunctions.draw_board(screen, board, move_scores,
                                   selected_square, engine_info, depth)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
