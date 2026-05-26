import pygame
import copy
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD, resource_path

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
mate = ""

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
                    piece_image = pygame.image.load(resource_path(f'whitepiece/{piece}.png')).convert_alpha()
                    piece_image = pygame.transform.scale(piece_image, piece_size)
                    screen.blit(piece_image, (col*piece_width, row*piece_height))
                else:
                    piece_image = pygame.image.load(resource_path(f'blackpiece/{piece}.png')).convert_alpha()
                    piece_image = pygame.transform.scale(piece_image, piece_size)
                    screen.blit(piece_image, (col*piece_width, row*piece_height))
                    
                    
def colour(piece: str):
    if piece == " ":
        return ""
    return "w" if piece.isupper() else "b"


def check_black_check(board):
    br, bc = 0, 0
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if p == "k":
                br, bc = r, c
    #BLACK
    if bc+1 < 8 and br+1<8:
        if board[br+1][bc+1] == "P":
            return "b"
    if bc-1 >= 0 and br+1<8:
        if board[br+1][bc-1] == "P":
            return "b"
        
    #DOWNRIGHT
    for i in range(1,8):
        if bc+i > 7 or br+i>7 or br+i < 0 or bc+i<0:
            break
        if colour(board[br+i][bc+i]) == "b":
            break
        if board[br+i][bc+i] == "B" or board[br+i][bc+i] == "Q":
            return "b"
    #DOWNLEFT
    for i in range(1,8):
        if bc-i > 7 or br+i>7 or br+i < 0 or bc-i<0:
            break
        if colour(board[br+i][bc-i]) == "b":
            break
        if board[br+i][bc-i] == "B" or board[br+i][bc-i] == "Q":
            return "b"
    #UPLEFT
    for i in range(1,8):
        if bc-i > 7 or br-i>7 or br-i < 0 or bc-i<0:
            break
        if colour(board[br-i][bc-i]) == "b":
            break
        if board[br-i][bc-i] == "B" or board[br-i][bc-i] == "Q":
            return "b"
        
    #UPRIGHT
    for i in range(1,8):
        if bc+i > 7 or br-i>7 or br-i < 0 or bc+i<0:
            break
        if colour(board[br-i][bc+i]) == "b":
            break
        if board[br-i][bc+i] == "B" or board[br-i][bc+i] == "Q":
            return "b"
    #RIGHT
    for i in range(1,8):
        if bc+i > 7:
            break
        if colour(board[br][bc+i]) == "b":
            break
        if board[br][bc+i] == "R" or board[br][bc+i] == "Q":
            return "b"
        
    #LEFT
    for i in range(1,8):
        if bc-i < 0:
            break
        if colour(board[br][bc-i]) == "b":
            break
        if board[br][bc-i] == "R" or board[br][bc-i] == "Q":
            return "b"
        
    #DOWN
    for i in range(1,8):
        if br+i > 7:
            break
        if colour(board[br+i][bc]) == "b":
            break
        if board[br+i][bc] == "R" or board[br+i][bc] == "Q":
            return "b"
    
    #UP
    for i in range(1,8):
        if br-i < 0:
            break
        if colour(board[br-i][bc]) == "b":
            break
        if board[br-i][bc] == "R" or board[br-i][bc] == "Q":
            return "b"
    
    #check all the Ls
    wtemp = []
    wtemp.append((br+1, bc+2))
    wtemp.append((br+1, bc-2))
    wtemp.append((br-1, bc+2))
    wtemp.append((br-1, bc-2))
    wtemp.append((br+2, bc+1))
    wtemp.append((br+2, bc-1))
    wtemp.append((br-2, bc+1))
    wtemp.append((br-2, bc-1))
    for move in wtemp:
        if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
            continue
        if board[move[0]][move[1]] == "N":
            return "b"
        
    #check surrounding 8
    wtemp = []
    wtemp.append((br-1, bc-1))
    wtemp.append((br-1, bc))
    wtemp.append((br-1, bc+1))
    wtemp.append((br, bc-1))
    wtemp.append((br, bc+1))
    wtemp.append((br+1, bc-1))
    wtemp.append((br+1, bc))
    wtemp.append((br+1, bc+1))
    
    for move in wtemp:
        if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
            continue
        if board[move[0]][move[1]] == "K":
            return "b"
    
    return ""

def check_white_check(board):
    wr, wc = 0, 0
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if p == "K":
                wr, wc = r, c
                
    #reverse check
    
    #WHITE
    if wc+1 < 8 and wr-1>=0:
        if board[wr-1][wc+1] == "p":
            return "w"
    if wc-1 >= 0 and wr-1>=0:
        if board[wr-1][wc-1] == "p":
            return "w"
        
    #DOWNRIGHT
    for i in range(1,8):
        if wc+i > 7 or wr+i>7 or wr+i < 0 or wc+i<0:
            break
        if colour(board[wr+i][wc+i]) == "w":
            break
        if board[wr+i][wc+i] == "b" or board[wr+i][wc+i] == "q":
            return "w"
    #DOWNLEFT
    for i in range(1,8):
        if wc-i > 7 or wr+i>7 or wr+i < 0 or wc-i<0:
            break
        if colour(board[wr+i][wc-i]) == "w":
            break
        if board[wr+i][wc-i] == "b" or board[wr+i][wc-i] == "q":
            return "w"
    #UPLEFT
    for i in range(1,8):
        if wc-i > 7 or wr-i>7 or wr-i < 0 or wc-i<0:
            break
        if colour(board[wr-i][wc-i]) == "w":
            break
        if board[wr-i][wc-i] == "b" or board[wr-i][wc-i] == "q":
            return "w"
        
    #UPRIGHT
    for i in range(1,8):
        if wc+i > 7 or wr-i>7 or wr-i < 0 or wc+i<0:
            break
        if colour(board[wr-i][wc+i]) == "w":
            break
        if board[wr-i][wc+i] == "b" or board[wr-i][wc+i] == "q":
            return "w"
    #RIGHT
    for i in range(1,8):
        if wc+i > 7:
            break
        if colour(board[wr][wc+i]) == "w":
            break
        if board[wr][wc+i] == "r" or board[wr][wc+i] == "q":
            return "w"
        
    #LEFT
    for i in range(1,8):
        if wc-i > 7:
            break
        if colour(board[wr][wc-i]) == "w":
            break
        if board[wr][wc-i] == "r" or board[wr][wc-i] == "q":
            return "w"
        
    #DOWN
    for i in range(1,8):
        if wr+i > 7:
            break
        if colour(board[wr+i][wc]) == "w":
            break
        if board[wr+i][wc] == "r" or board[wr+i][wc] == "q":
            return "w"
    
    #UP
    for i in range(1,8):
        if wr-i > 7:
            break
        if colour(board[wr-i][wc]) == "w":
            break
        if board[wr-i][wc] == "r" or board[wr-i][wc] == "q":
            return "w"
    
    #check all the Ls
    wtemp = []
    wtemp.append((wr+1, wc+2))
    wtemp.append((wr+1, wc-2))
    wtemp.append((wr-1, wc+2))
    wtemp.append((wr-1, wc-2))
    wtemp.append((wr+2, wc+1))
    wtemp.append((wr+2, wc-1))
    wtemp.append((wr-2, wc+1))
    wtemp.append((wr-2, wc-1))
    for move in wtemp:
        if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
            continue
        if board[move[0]][move[1]] == "n":
            return "w"
        
    #check surrounding 8
    wtemp = []
    wtemp.append((wr-1, wc-1))
    wtemp.append((wr-1, wc))
    wtemp.append((wr-1, wc+1))
    wtemp.append((wr, wc-1))
    wtemp.append((wr, wc+1))
    wtemp.append((wr+1, wc-1))
    wtemp.append((wr+1, wc))
    wtemp.append((wr+1, wc+1))
    
    for move in wtemp:
        if move[0] < 0 or move[0] > 7  or move[1] < 0 or move[1] > 7:
            continue
        if board[move[0]][move[1]] == "k":
            return "w"
        
    return ""

def check_legal_moves(r: int, c: int):
    res = []
    p = board[r][c]
    #PAWN - TODO: En Passant
    if p.lower() == "p": #checks if it is A pawn
        temp = []
        if colour(p) == "w":  #checks for white pawn
            if r-1 >= 0: #checks that there is a spot above
                #move conditons
                if board[r-1][c] == " ": #checks that the spot is empty
                    temp.append((r-1, c)) #add the spot above
                    
                    if r == 6 and board[r-2][c] == " ": #if unmoved, allow for 2 move
                       temp.append((r-2, c))
                
                #take conditions
                if c+1 <= 7 and colour(board[r-1][c+1]) == "b":
                    temp.append((r-1, c+1))
                if c-1 >=0 and colour(board[r-1][c-1]) == "b":
                    temp.append((r-1, c-1))
        if colour(p) == "b":  #checks for white pawn
            if r+1 <= 7: #checks that there is a spot above
                #move conditons
                if board[r+1][c] == " ": #checks that the spot is empty
                    temp.append((r+1, c)) #add the spot above
                    
                    if r == 1 and board[r+2][c] == " ": #if unmoved, allow for 2 move
                       temp.append((r+2, c))
                
                #take conditions
                if c+1 <= 7 and colour(board[r+1][c+1]) == "w":
                    temp.append((r+1, c+1))
                if c-1 >=0 and colour(board[r+1][c-1]) == "w":
                    temp.append((r+1, c-1))
        for move in temp:
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)        
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
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
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
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)
        
        castle_moves = []
        if colour(p) == "w":
            if w_king_moved == 0 and check_white_check(board) == "":
                if w_r_rook_moved == 0 and (7,5) in res and board[7][6] == " ":
                    castle_moves.append((7,6))
                if w_l_rook_moved == 0 and (7,3) in res and board[7][2] == " " and board[7][1] == " ":
                    castle_moves.append((7, 2))
                    
        if colour(p) == "b":
            if b_king_moved == 0 and check_black_check(board) == "":
                if b_r_rook_moved == 0 and (0, 5) in res and board[0][6] == " ":
                    castle_moves.append((0, 6))
                if b_l_rook_moved == 0 and (0, 3) in res and board[0][2] == " " and board[0][1] == " ":
                    castle_moves.append((0, 2))
                    
        for move in castle_moves:
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)
    #rook
    if p.lower() == "r":
        temp = []
        #check right
        for i in range(1,8):
            if c+i > 7:
                break
            if colour(board[r][c+i]) == colour(p):
                break
            if (colour(board[r][c+i]) == "w" and colour(p) == "b") or (colour(board[r][c+i]) == "b" and colour(p) == "w"):
                temp.append((r, c+i))
                break
            temp.append((r, c+i))
        
        #check left
        for i in range(1,8):
            if c-i < 0:
                break
            if colour(board[r][c-i]) == colour(p):
                break
            if (colour(board[r][c-i]) == "w" and colour(p) == "b") or (colour(board[r][c-i]) == "b" and colour(p) == "w"):
                temp.append((r, c-i))
                break
            temp.append((r, c-i))
            
        #check down
        for i in range(1,8):
            if r+i > 7:
                break
            if colour(board[r+i][c]) == colour(p):
                break
            if (colour(board[r+i][c]) == "w" and colour(p) == "b") or (colour(board[r+i][c]) == "b" and colour(p) == "w"):
                temp.append((r+i, c))
                break
            temp.append((r+i, c))
            
        #check up
        for i in range(1,8):
            if r-i < 0:
                break
            if colour(board[r-i][c]) == colour(p):
                break
            if (colour(board[r-i][c]) == "w" and colour(p) == "b") or (colour(board[r-i][c]) == "b" and colour(p) == "w"):
                temp.append((r-i, c))
                break
            temp.append((r-i, c))
            
        for move in temp:
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)
            
    #bishop
    if p.lower() == "b":
        temp = []
        #check downright
        for i in range(1,8):
            if c+i > 7 or r+i>7 or r+i < 0 or c+i<0:
                break
            if colour(board[r+i][c+i]) == colour(p):
                break
            if (colour(board[r+i][c+i]) == "w" and colour(p) == "b") or (colour(board[r+i][c+i]) == "b" and colour(p) == "w"):
                temp.append((r+i, c+i))
                break
            temp.append((r+i, c+i))
            
        #check downleft
        for i in range(1,8):
            if c-i > 7 or r+i>7 or r+i < 0 or c-i<0:
                break
            if colour(board[r+i][c-i]) == colour(p):
                break
            if (colour(board[r+i][c-i]) == "w" and colour(p) == "b") or (colour(board[r+i][c-i]) == "b" and colour(p) == "w"):
                temp.append((r+i, c-i))
                break
            temp.append((r+i, c-i))
            
        #check upleft
        for i in range(1,8):
            if c-i > 7 or r-i>7 or r-i < 0 or c-i<0:
                break
            if colour(board[r-i][c-i]) == colour(p):
                break
            if (colour(board[r-i][c-i]) == "w" and colour(p) == "b") or (colour(board[r-i][c-i]) == "b" and colour(p) == "w"):
                temp.append((r-i, c-i))
                break
            temp.append((r-i, c-i))
            
        #check upright
        for i in range(1,8):
            if c+i > 7 or r-i>7 or r-i < 0 or c+i<0:
                break
            if colour(board[r-i][c+i]) == colour(p):
                break
            if (colour(board[r-i][c+i]) == "w" and colour(p) == "b") or (colour(board[r-i][c+i]) == "b" and colour(p) == "w"):
                temp.append((r-i, c+i))
                break
            temp.append((r-i, c+i))
            
        for move in temp:
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)
    
    #queen
    if p.lower() == "q":
        temp = []
        #check right
        for i in range(1,8):
            if c+i > 7:
                break
            if colour(board[r][c+i]) == colour(p):
                break
            if (colour(board[r][c+i]) == "w" and colour(p) == "b") or (colour(board[r][c+i]) == "b" and colour(p) == "w"):
                temp.append((r, c+i))
                break
            temp.append((r, c+i))
        
        #check left
        for i in range(1,8):
            if c-i < 0:
                break
            if colour(board[r][c-i]) == colour(p):
                break
            if (colour(board[r][c-i]) == "w" and colour(p) == "b") or (colour(board[r][c-i]) == "b" and colour(p) == "w"):
                temp.append((r, c-i))
                break
            temp.append((r, c-i))
            
        #check down
        for i in range(1,8):
            if r+i > 7:
                break
            if colour(board[r+i][c]) == colour(p):
                break
            if (colour(board[r+i][c]) == "w" and colour(p) == "b") or (colour(board[r+i][c]) == "b" and colour(p) == "w"):
                temp.append((r+i, c))
                break
            temp.append((r+i, c))
            
        #check up
        for i in range(1,8):
            if r-i < 0:
                break
            if colour(board[r-i][c]) == colour(p):
                break
            if (colour(board[r-i][c]) == "w" and colour(p) == "b") or (colour(board[r-i][c]) == "b" and colour(p) == "w"):
                temp.append((r-i, c))
                break
            temp.append((r-i, c))
            
        #check downright
        for i in range(1,8):
            if c+i > 7 or r+i>7 or r+i < 0 or c+i<0:
                break
            if colour(board[r+i][c+i]) == colour(p):
                break
            if (colour(board[r+i][c+i]) == "w" and colour(p) == "b") or (colour(board[r+i][c+i]) == "b" and colour(p) == "w"):
                temp.append((r+i, c+i))
                break
            temp.append((r+i, c+i))
            
        #check downleft
        for i in range(1,8):
            if c-i > 7 or r+i>7 or r+i < 0 or c-i<0:
                break
            if colour(board[r+i][c-i]) == colour(p):
                break
            if (colour(board[r+i][c-i]) == "w" and colour(p) == "b") or (colour(board[r+i][c-i]) == "b" and colour(p) == "w"):
                temp.append((r+i, c-i))
                break
            temp.append((r+i, c-i))
            
        #check upleft
        for i in range(1,8):
            if c-i > 7 or r-i>7 or r-i < 0 or c-i<0:
                break
            if colour(board[r-i][c-i]) == colour(p):
                break
            if (colour(board[r-i][c-i]) == "w" and colour(p) == "b") or (colour(board[r-i][c-i]) == "b" and colour(p) == "w"):
                temp.append((r-i, c-i))
                break
            temp.append((r-i, c-i))
            
        #check upright
        for i in range(1,8):
            if c+i > 7 or r-i>7 or r-i < 0 or c+i<0:
                break
            if colour(board[r-i][c+i]) == colour(p):
                break
            if (colour(board[r-i][c+i]) == "w" and colour(p) == "b") or (colour(board[r-i][c+i]) == "b" and colour(p) == "w"):
                temp.append((r-i, c+i))
                break
            temp.append((r-i, c+i))
            
        for move in temp:
            test_board = copy.deepcopy(board)
            test_board[r][c] = " "
            test_board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_board) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_board) == "":
                    res.append(move)
    return res

def check_white_moves():
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if colour(p) == "w":
                if len(check_legal_moves(r, c)) != 0:
                    return True
    return False

def check_black_moves():
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if colour(p) == "b":
                if len(check_legal_moves(r, c)) != 0:
                    return True
    return False

def check_checkmate():
    if not(check_white_moves()) and check_white_check(board) == "w":
        return "w"
    if not(check_black_moves()) and check_black_check(board) == "b":
        return "b"
    if turn == "w" and not check_white_moves():
        return "d"
    if turn == "b" and not check_black_moves():
        return "d"
    return ""
 
def move():
    global selected_row, selected_col, selected_piece, turn, turns, w_king_moved, b_king_moved, w_l_rook_moved, w_r_rook_moved, b_l_rook_moved, b_r_rook_moved, highlighted_board, selected_board, mate
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
                if selected_piece == "P":
                    if clicked_row == 0:
                        promo_options = ['q', 'n', 'r', 'b']
                        print("q: queen\nn: knight\nr: rook\nb: bishop")
                        inp = ''
                        while inp.lower() not in promo_options:
                            inp = input("Please select your choice: ")
                        board[clicked_row][clicked_col] = inp.upper()
                if selected_piece == "p":
                    if clicked_row == 7:
                        promo_options = ['q', 'n', 'r', 'b']
                        print("q: queen\nn: knight\nr: rook\nb: bishop")
                        inp = ''
                        while inp.lower() not in promo_options:
                            inp = input("Please select your choice: ")
                        board[clicked_row][clicked_col] = inp.lower()
                        
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
                mate = check_checkmate()
                

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
                    overlay_image = pygame.image.load(resource_path('overlay/square.png')).convert_alpha()
                    overlay_image = pygame.transform.scale(overlay_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
                    screen.blit(overlay_image, (c * SQUARE_WIDTH, r * SQUARE_HEIGHT))

def get_mate():
    global mate
    return mate