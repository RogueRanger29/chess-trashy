import pygame
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD

board = DEFAULT_BOARD.copy()
overlayboard = [[0 for x in range(8)] for _ in range(8)]
clicking = False

selected_row = -1
selected_col = -1
selected_piece = ""

turn = "w"

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
                    
                    
def colour(piece):
    return "w" if piece.isupper() else "b"
                    
def move():
    global selected_row, selected_col, selected_piece, turn
    if clicking:
        clicked_row = int(pygame.mouse.get_pos()[1]//SQUARE_HEIGHT)
        clicked_col = int(pygame.mouse.get_pos()[0]//SQUARE_WIDTH)
        clicked_piece = board[clicked_row][clicked_col]
        
        if selected_piece == "": #select piece
            if clicked_piece != " " and colour(clicked_piece) == turn: #check that there is a piece there and its ur turn
                selected_row = clicked_row
                selected_col = clicked_col
                selected_piece=clicked_piece
                selected_piece = clicked_piece
                overlayboard[clicked_row][clicked_col] = 1
        else:
            if (clicked_row, clicked_col) == (selected_row, selected_col): #deselect piece
                overlayboard[selected_row][selected_col] = 0
                selected_row = -1
                selected_col = -1
                selected_piece = ""
            
            elif colour(clicked_piece) == turn and clicked_piece != " ":
                overlayboard[selected_row][selected_col] = 0
                selected_row = clicked_row
                selected_col = clicked_col
                selected_piece = clicked_piece
                overlayboard[clicked_row][clicked_col] = 1
            
            elif clicked_piece == " " or colour(clicked_piece) !=  colour(board[selected_row][selected_col]): #check whether its empty space there or opponent colour
                board[clicked_row][clicked_col] = selected_piece
                board[selected_row][selected_col] = " "
                overlayboard[selected_row][selected_col] = 0
                selected_row = -1
                selected_col = -1
                selected_piece = ""
                turn = "b" if turn=="w" else "w"
        
def draw_overlay(screen: pygame.Surface):
    for r, rank in enumerate(overlayboard):
        for c, v in enumerate(rank):
            if v:
                rect = pygame.Rect(c*SQUARE_WIDTH, r*SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
                pygame.draw.rect(screen, (255, 0, 0), rect)
                