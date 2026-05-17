import pygame
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD

board = DEFAULT_BOARD.copy()
overlayboard = [[0 for x in range(8)] for _ in range(8)]
clicking = False
def set_click_state(click: bool):
    global clicking
    clicking = click
def draw_board(screen: pygame.Surface):    
    for row in range(8):
        for col in range(8):
            square = pygame.Rect(col*SQUARE_WIDTH, row*SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
            if (row+col)%2:
                color = DARK
            else:
                color = LIGHT
            
            pygame.draw.rect(screen, color, square)
            
def draw_pieces(screen: pygame.Surface):
    piece_width = SQUARE_WIDTH
    piece_height = SQUARE_HEIGHT
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
                    
def test_set_overlayer():
    if clicking:
        row = int(pygame.mouse.get_pos()[1]//SQUARE_HEIGHT)
        col = int(pygame.mouse.get_pos()[0]//SQUARE_WIDTH)
        overlayboard[row][col] = int(not(overlayboard[row][col]))
        

def draw_overlay(screen: pygame.Surface):
    for r, rank in enumerate(overlayboard):
        for c, v in enumerate(rank):
            if v:
                rect = pygame.Rect(c*SQUARE_WIDTH, r*SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
                pygame.draw.rect(screen, (255, 0, 0), rect)
                