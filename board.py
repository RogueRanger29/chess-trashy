import pygame
from helper import WIDTH, HEIGHT, LIGHT, DARK, DEFAULT_BOARD

board = DEFAULT_BOARD.copy()
def draw_board(screen: pygame.Surface):    
    square_width = WIDTH/8
    square_height = HEIGHT/8
    for row in range(8):
        for col in range(8):
            square = pygame.Rect(col*square_width, row*square_height, square_width, square_height)
            if (row+col)%2:
                color = DARK
            else:
                color = LIGHT
            
            pygame.draw.rect(screen, color, square)
            
def draw_pieces(screen: pygame.Surface):
    piece_width = WIDTH/8
    piece_height = HEIGHT/8
    piece_size = (piece_width, piece_height)
    for row, rank in enumerate(board):
        for col, piece in enumerate(rank):
            if piece != ' ':
                if piece.isupper():
                    piece_image = pygame.image.load(f'whitepiece/{piece}.png').convert_alpha()
                    piece_image = pygame.transform.scale(piece_image, piece_size)
                    screen.blit(piece_image, (col*piece_width, row*piece_height))
                else:
                    piece_image = pygame.image.load(f'blackpiece/{piece}.png').convert_alpha()
                    piece_image = pygame.transform.scale(piece_image, piece_size)
                    screen.blit(piece_image, (col*piece_width, row*piece_height))