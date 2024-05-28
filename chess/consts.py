import pygame

pygame.font.init()


class Consts():
    TITLE = "Prosty silnik szachowy"
    STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"
    WIDTH, HEIGHT = 1000, 1000
    SQUARE_SIZE = WIDTH // 8

    COLORS = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]
    FONT = pygame.font.SysFont("arial", 24)
    PIECE_IMAGES = {
        'P': 'w_pawn_.png',
        'p': 'b_pawn_.png',
        'N': 'w_knight_.png',
        'n': 'b_knight_.png',
        'B': 'w_bishop_.png',
        'b': 'b_bishop_.png',
        'R': 'w_rook_.png',
        'r': 'b_rook_.png',
        'Q': 'w_queen_.png',
        'q': 'b_queen_.png',
        'K': 'w_king_.png',
        'k': 'b_king_.png'
    }
    VAL_TRESHOLD = 300
