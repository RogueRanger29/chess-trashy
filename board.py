import pygame
import copy
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD

board = copy.deepcopy(DEFAULT_BOARD)
selected_board = [[0 for x in range(8)] for _ in range(8)]
highlighted_board = [[0 for x in range(8)] for _ in range(8)]
clicking = False

selected_row = -1
selected_col = -1
selected_piece = ""

#stats for castle
w_king_moved = 0
w_l_rook_moved = 0
w_r_rook_moved = 0

b_king_moved = 0
b_l_rook_moved = 0
b_r_rook_moved = 0

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
            
        if colour(p) == "w":
            if w_king_moved == 0:
                if w_r_rook_moved == 0 and (7,5) in res and board[7][6] == " ":
                    res.append((7,6))
                if w_l_rook_moved == 0 and (7,3) in res and board[7][2] == " " and board[7][1] == " ":
                    res.append((7, 2))
                    
        if colour(p) == "b":
            if b_king_moved == 0:
                if b_r_rook_moved == 0 and (0, 5) in res and board[0][6] == " ":
                    res.append((0, 6))
                if b_l_rook_moved == 0 and (0, 3) in res and board[0][2] == " " and board[0][1] == " ":
                    res.append((0, 2))
    
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
            
    #bishop
    if p.lower() == "b":
        #check downright
        for i in range(1,8):
            if c+i > 7 or r+i>7 or r+i < 0 or c+i<0:
                break
            if colour(board[r+i][c+i]) == colour(p):
                break
            if (colour(board[r+i][c+i]) == "w" and colour(p) == "b") or (colour(board[r+i][c+i]) == "b" and colour(p) == "w"):
                res.append((r+i, c+i))
                break
            res.append((r+i, c+i))
            
        #check downleft
        for i in range(1,8):
            if c-i > 7 or r+i>7 or r+i < 0 or c-i<0:
                break
            if colour(board[r+i][c-i]) == colour(p):
                break
            if (colour(board[r+i][c-i]) == "w" and colour(p) == "b") or (colour(board[r+i][c-i]) == "b" and colour(p) == "w"):
                res.append((r+i, c-i))
                break
            res.append((r+i, c-i))
            
        #check upleft
        for i in range(1,8):
            if c-i > 7 or r-i>7 or r-i < 0 or c-i<0:
                break
            if colour(board[r-i][c-i]) == colour(p):
                break
            if (colour(board[r-i][c-i]) == "w" and colour(p) == "b") or (colour(board[r-i][c-i]) == "b" and colour(p) == "w"):
                res.append((r-i, c-i))
                break
            res.append((r-i, c-i))
            
        #check upright
        for i in range(1,8):
            if c+i > 7 or r-i>7 or r-i < 0 or c+i<0:
                break
            if colour(board[r-i][c+i]) == colour(p):
                break
            if (colour(board[r-i][c+i]) == "w" and colour(p) == "b") or (colour(board[r-i][c+i]) == "b" and colour(p) == "w"):
                res.append((r-i, c+i))
                break
            res.append((r-i, c+i))
    
    #queen
    if p.lower() == "q":
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
            
        #check downright
        for i in range(1,8):
            if c+i > 7 or r+i>7 or r+i < 0 or c+i<0:
                break
            if colour(board[r+i][c+i]) == colour(p):
                break
            if (colour(board[r+i][c+i]) == "w" and colour(p) == "b") or (colour(board[r+i][c+i]) == "b" and colour(p) == "w"):
                res.append((r+i, c+i))
                break
            res.append((r+i, c+i))
            
        #check downleft
        for i in range(1,8):
            if c-i > 7 or r+i>7 or r+i < 0 or c-i<0:
                break
            if colour(board[r+i][c-i]) == colour(p):
                break
            if (colour(board[r+i][c-i]) == "w" and colour(p) == "b") or (colour(board[r+i][c-i]) == "b" and colour(p) == "w"):
                res.append((r+i, c-i))
                break
            res.append((r+i, c-i))
            
        #check upleft
        for i in range(1,8):
            if c-i > 7 or r-i>7 or r-i < 0 or c-i<0:
                break
            if colour(board[r-i][c-i]) == colour(p):
                break
            if (colour(board[r-i][c-i]) == "w" and colour(p) == "b") or (colour(board[r-i][c-i]) == "b" and colour(p) == "w"):
                res.append((r-i, c-i))
                break
            res.append((r-i, c-i))
            
        #check upright
        for i in range(1,8):
            if c+i > 7 or r-i>7 or r-i < 0 or c+i<0:
                break
            if colour(board[r-i][c+i]) == colour(p):
                break
            if (colour(board[r-i][c+i]) == "w" and colour(p) == "b") or (colour(board[r-i][c+i]) == "b" and colour(p) == "w"):
                res.append((r-i, c+i))
                break
            res.append((r-i, c+i))
    
    return res
    
def move():
    global selected_row, selected_col, selected_piece, turn, turns, w_king_moved, b_king_moved, w_l_rook_moved, w_r_rook_moved, b_l_rook_moved, b_r_rook_moved, highlighted_board, selected_board
    if clicking:
        clicked_row = int(pygame.mouse.get_pos()[1]//SQUARE_HEIGHT)
        clicked_col = int(pygame.mouse.get_pos()[0]//SQUARE_WIDTH)
        clicked_piece = board[clicked_row][clicked_col]
        
        if selected_piece == "": #select piece
            if clicked_piece != " " and colour(clicked_piece) == turn: #check that there is a piece there and its ur turn
                selected_row = clicked_row
                selected_col = clicked_col
                selected_piece = clicked_piece
                selected_piece = clicked_piece
                selected_board[clicked_row][clicked_col] = 1
                highlighted_board = [[0 for x in range(8)] for _ in range(8)]
                for move in check_legal_moves(selected_row, selected_col):
                    highlighted_board[move[0]][move[1]] = 1

        else: #move/change selection
            if (clicked_row, clicked_col) == (selected_row, selected_col): #deselect piece
                selected_board[selected_row][selected_col] = 0
                highlighted_board = [[0 for x in range(8)] for _ in range(8)]
                selected_row = -1
                selected_col = -1
                selected_piece = ""
            
            elif colour(clicked_piece) == turn and clicked_piece != " ": #change selection
                selected_board[selected_row][selected_col] = 0
                selected_row = clicked_row
                selected_col = clicked_col
                selected_piece = clicked_piece
                selected_board[clicked_row][clicked_col] = 1
                highlighted_board = [[0 for x in range(8)] for _ in range(8)]
                for move in check_legal_moves(selected_row, selected_col):
                    highlighted_board[move[0]][move[1]] = 1
            
            #move
            elif (clicked_row, clicked_col) in check_legal_moves(selected_row, selected_col): #check whether its empty space there or opponent colour
                
                if selected_piece == "K":
                    if w_king_moved == 0 and (clicked_row, clicked_col) == (7, 6):
                        board[7][7] = " "
                        board[7][5] = "R"
                        w_r_rook_moved = 1
                    if w_king_moved == 0 and (clicked_row, clicked_col) == (7, 2):
                        board[7][0] = " "
                        board[7][3] = "R"
                        w_l_rook_moved = 1
                if selected_piece == "k":
                    if b_king_moved == 0 and (clicked_row, clicked_col) == (0, 6):
                        board[0][7] = " "
                        board[0][5] = "r"
                        b_r_rook_moved = 1
                    if b_king_moved == 0 and (clicked_row, clicked_col) == (0, 2):
                        board[0][0] = " "
                        board[0][3] = "r"
                        b_l_rook_moved = 1
                
                board[clicked_row][clicked_col] = selected_piece
                board[selected_row][selected_col] = " "
                selected_board[selected_row][selected_col] = 0
                highlighted_board = [[0 for x in range(8)] for _ in range(8)]
                
                if selected_piece == "k": b_king_moved = 1
                if selected_piece == "K": w_king_moved = 1
                if selected_row == 7 and selected_col == 0: w_l_rook_moved = 1
                if selected_row == 7 and selected_col == 7: w_r_rook_moved = 1
                if selected_row == 0 and selected_col == 0: b_l_rook_moved = 1
                if selected_row == 0 and selected_col == 7: b_r_rook_moved = 1
                
                selected_row = -1
                selected_col = -1
                selected_piece = ""
                turn = "b" if turn=="w" else "w"
                turns += 1
                
                print(f"{w_king_moved = }, {b_king_moved = }, {w_l_rook_moved = }, {w_r_rook_moved = }, {b_l_rook_moved = }, {b_r_rook_moved = }")
        
def draw_selected_overlay(screen: pygame.Surface):
    overlay = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT), pygame.SRCALPHA)
    overlay.fill((169, 123, 49, 191))

    for r, rank in enumerate(selected_board):
        for c, v in enumerate(rank):
            if v:
                screen.blit(overlay, (c*SQUARE_WIDTH, r*SQUARE_HEIGHT))
                
                
def draw_highlighted_overlay(screen: pygame.Surface):
    for r, rank in enumerate(highlighted_board):
        for c, v in enumerate(rank):
            if v:
                if board[r][c] == " ":
                    pygame.draw.circle(screen,(255, 0, 0), (c * SQUARE_WIDTH + SQUARE_WIDTH // 2, r * SQUARE_HEIGHT + SQUARE_HEIGHT // 2), SQUARE_WIDTH/7)
                else:
                    overlay_image = pygame.image.load('overlay/square.png').convert_alpha()
                    overlay_image = pygame.transform.scale(overlay_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
                    screen.blit(overlay_image, (c * SQUARE_WIDTH, r * SQUARE_HEIGHT))