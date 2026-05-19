import pygame
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD

board = DEFAULT_BOARD.copy()
overlayboard = [[0 for x in range(8)] for _ in range(8)]
clicking = False

selected_row = -1
selected_col = -1
selected_piece = ""

turn = "w"
turns = 0

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
                    
                    
def colour(piece: str):
    if piece == " ":
        return ""
    return "w" if piece.isupper() else "b"

def check_legal_moves(r: int, c: int):
    res = []
    p = board[r][c]
    #PAWN - TODO: En Passant
    if p.lower() == "p": #checks if it is A pawn
        if colour(p) == "w":  #checks for white pawn
            if r-1 >= 0: #checks that there is a spot above
                #move conditons
                if board[r-1][c] == " ": #checks that the spot is empty
                    res.append((r-1, c)) #add the spot above
                    
                    if r == 6 and board[r-2][c] == " ": #if unmoved, allow for 2 move
                       res.append((r-2, c))
                
                #take conditions
                if c+1 <= 7 and colour(board[r-1][c+1]) == "b":
                    res.append((r-1, c+1))
                if c-1 >=0 and colour(board[r-1][c-1]) == "b":
                    res.append((r-1, c-1))
        if colour(p) == "b":  #checks for white pawn
            if r+1 <= 7: #checks that there is a spot above
                #move conditons
                if board[r+1][c] == " ": #checks that the spot is empty
                    res.append((r+1, c)) #add the spot above
                    
                    if r == 1 and board[r+2][c] == " ": #if unmoved, allow for 2 move
                       res.append((r+2, c))
                
                #take conditions
                if c+1 <= 7 and colour(board[r+1][c+1]) == "w":
                    res.append((r+1, c+1))
                if c-1 >=0 and colour(board[r+1][c-1]) == "w":
                    res.append((r+1, c-1))
                    
    #knight
    if p.lower() == "n":
        temp = []
        temp.append((r+1, c+2))
        temp.append((r+1, c-2))
        temp.append((r-1, c+2))
        temp.append((r-1, c-2))
        temp.append((r+2, c+1))
        temp.append((r+2, c-1))
        temp.append((r-2, c+1))
        temp.append((r-2, c-1))
        for move in temp:
            if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
                continue
            if colour(board[move[0]][move[1]]) == colour(p): #ur own pieces
                continue
            res.append(move)
    
    #king
    if p.lower() == "k":
        temp = []
        temp.append((r-1, c-1))
        temp.append((r-1, c))
        temp.append((r-1, c+1))
        temp.append((r, c-1))
        temp.append((r, c+1))
        temp.append((r+1, c-1))
        temp.append((r+1, c))
        temp.append((r+1, c+1))
        
        for move in temp:
            if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
                continue
            if colour(board[move[0]][move[1]]) == colour(p): #ur own pieces
                continue
            res.append(move)
    
    #rook
    if p.lower() == "r":
        #check right
        for i in range(1,8):
            if c+i > 7:
                break
            if colour(board[r][c+i]) == colour(p):
                break
            if (colour(board[r][c+i]) == "w" and colour(p) == "b") or (colour(board[r][c+i]) == "b" and colour(p) == "w"):
                res.append((r, c+i))
                break
            res.append((r, c+i))
        
        #check left
        for i in range(1,8):
            if c-i < 0:
                break
            if colour(board[r][c-i]) == colour(p):
                break
            if (colour(board[r][c-i]) == "w" and colour(p) == "b") or (colour(board[r][c-i]) == "b" and colour(p) == "w"):
                res.append((r, c-i))
                break
            res.append((r, c-i))
            
        #check down
        for i in range(1,8):
            if r+i > 7:
                break
            if colour(board[r+i][c]) == colour(p):
                break
            if (colour(board[r+i][c]) == "w" and colour(p) == "b") or (colour(board[r+i][c]) == "b" and colour(p) == "w"):
                res.append((r+i, c))
                break
            res.append((r+i, c))
            
        #check up
        for i in range(1,8):
            if r-i < 0:
                break
            if colour(board[r-i][c]) == colour(p):
                break
            if (colour(board[r-i][c]) == "w" and colour(p) == "b") or (colour(board[r-i][c]) == "b" and colour(p) == "w"):
                res.append((r-i, c))
                break
            res.append((r-i, c))
    return res

                    
def move():
    global selected_row, selected_col, selected_piece, turn, turns
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
                print(check_legal_moves(selected_row, selected_col))
        else: #move/change selection
            if (clicked_row, clicked_col) == (selected_row, selected_col): #deselect piece
                overlayboard[selected_row][selected_col] = 0
                selected_row = -1
                selected_col = -1
                selected_piece = ""
            
            elif colour(clicked_piece) == turn and clicked_piece != " ": #change selection
                overlayboard[selected_row][selected_col] = 0
                selected_row = clicked_row
                selected_col = clicked_col
                selected_piece = clicked_piece
                overlayboard[clicked_row][clicked_col] = 1
            
            elif (clicked_row, clicked_col) in check_legal_moves(selected_row, selected_col): #check whether its empty space there or opponent colour
                board[clicked_row][clicked_col] = selected_piece
                board[selected_row][selected_col] = " "
                overlayboard[selected_row][selected_col] = 0
                selected_row = -1
                selected_col = -1
                selected_piece = ""
                turn = "b" if turn=="w" else "w"
                turns += 1
        
def draw_overlay(screen: pygame.Surface):
    for r, rank in enumerate(overlayboard):
        for c, v in enumerate(rank):
            if v:
                rect = pygame.Rect(c*SQUARE_WIDTH, r*SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
                pygame.draw.rect(screen, (255, 0, 0), rect)
                