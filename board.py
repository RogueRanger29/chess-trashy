import pygame
import copy
from helper import SQUARE_WIDTH, SQUARE_HEIGHT, LIGHT, DARK, DEFAULT_BOARD, resource_path

class GameState:
    def __init__(self):
        self.board = copy.deepcopy(DEFAULT_BOARD)
        #stats for castle
        self.w_king_moved = 0
        self.w_l_rook_moved = 0
        self.w_r_rook_moved = 0

        self.b_king_moved = 0
        self.b_l_rook_moved = 0
        self.b_r_rook_moved = 0

        self.turn = "w"
        self.turns = 0
        self.mate = ""

        self.w_en_passant = None
        self.b_en_passant = None

        self.promotion = None

class UIState:
    def __init__(self):
        self.selected_board = [[0 for x in range(8)] for _ in range(8)]
        self.highlighted_board = [[0 for x in range(8)] for _ in range(8)]

        self.selected_row = -1
        self.selected_col = -1
        self.selected_piece = ""

    def clear(self):
        self.selected_board = [[0 for _ in range(8)] for _ in range(8)]
        self.highlighted_board = [[0 for _ in range(8)] for _ in range(8)]

        self.selected_row = -1
        self.selected_col = -1
        self.selected_piece = ""

    def deselect(self):
        if self.selected_row != -1:
            self.selected_board[self.selected_row][self.selected_col] = 0

        self.highlighted_board = [[0 for _ in range(8)] for _ in range(8)]
        self.selected_row = -1
        self.selected_col = -1
        self.selected_piece = ""
def get_event(event: pygame.event.Event, gamestate: GameState, uistate: UIState):
    if gamestate.promotion != None:
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_q:
                handle_promotion("q", gamestate)
            if key == pygame.K_n:
                handle_promotion("n", gamestate)
            if key == pygame.K_r:
                handle_promotion("r", gamestate)
            if key == pygame.K_b:
                handle_promotion("b", gamestate)
        return
    if event.type == pygame.MOUSEBUTTONDOWN:
        clicked_row = int(pygame.mouse.get_pos()[1]//SQUARE_HEIGHT)
        clicked_col = int(pygame.mouse.get_pos()[0]//SQUARE_WIDTH)
        handle_selection(clicked_row, clicked_col, gamestate, uistate)
    else:
        return
def handle_selection(r, c, gamestate: GameState, uistate: UIState):
    clicked_piece = gamestate.board[r][c]
    if uistate.selected_piece == "": #select piece if none selected
        if clicked_piece != " " and colour(clicked_piece) == gamestate.turn: #check that there is a piece there and its ur turn
            uistate.selected_row = r
            uistate.selected_col = c
            uistate.selected_piece = clicked_piece
            uistate.selected_board[r][c] = 1 
            uistate.highlighted_board = [[0 for x in range(8)] for _ in range(8)]
            for move in check_legal_moves(uistate.selected_row, uistate.selected_col, gamestate):
                uistate.highlighted_board[move[0]][move[1]] = 1
        return
    
    if (r, c) == (uistate.selected_row, uistate.selected_col): #deselect piece
        uistate.deselect()
        return
            
    if colour(clicked_piece) == gamestate.turn and clicked_piece != " ": #change selection
        uistate.selected_board[uistate.selected_row][uistate.selected_col] = 0
        uistate.selected_row = r
        uistate.selected_col = c
        uistate.selected_piece = clicked_piece
        uistate.selected_board[r][c] = 1
        uistate.highlighted_board = [[0 for x in range(8)] for _ in range(8)]
        for move in check_legal_moves(uistate.selected_row, uistate.selected_col, gamestate):
            uistate.highlighted_board[move[0]][move[1]] = 1
        return
    
    try_move(uistate.selected_row, uistate.selected_col, r, c, gamestate, uistate)
            
def handle_promotion(choice: str, gamestate: GameState):
    if gamestate.promotion == None:
        return
    p, r, c = gamestate.promotion
    if colour(p) == "w":
        gamestate.board[r][c] = choice.upper()
    else:
        gamestate.board[r][c] = choice.lower()
        
    gamestate.promotion = None
    
    if gamestate.turn == "w" and gamestate.promotion == None:
        gamestate.b_en_passant = None
        gamestate.turn = "b"
    elif gamestate.turn == "b" and gamestate.promotion == None:
        gamestate.w_en_passant = None
        gamestate.turn = "w"
    gamestate.turns += 1
    gamestate.mate = check_checkmate(gamestate)
    
def draw_board(screen: pygame.Surface):    
    for row in range(8):
        for col in range(8):
            square = pygame.Rect(col*SQUARE_WIDTH, row*SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT)
            if (row+col)%2:
                color = DARK
            else:
                color = LIGHT
            
            pygame.draw.rect(screen, color, square)
            
def draw_pieces(screen: pygame.Surface, gamestate: GameState):
    piece_width = SQUARE_WIDTH
    piece_height = SQUARE_HEIGHT
    piece_size = (piece_width, piece_height)
    for row, rank in enumerate(gamestate.board):
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


def check_black_check(gamestate: GameState):
    board = gamestate.board
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

def check_white_check(gamestate: GameState):
    board = gamestate.board
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

def check_legal_moves(r: int, c: int, gamestate: GameState):
    board = gamestate.board
    w_en_passant = gamestate.w_en_passant
    b_en_passant  = gamestate.b_en_passant
    
    w_king_moved = gamestate.w_king_moved
    w_l_rook_moved = gamestate.w_l_rook_moved
    w_r_rook_moved = gamestate.w_r_rook_moved
    
    b_king_moved = gamestate.b_king_moved
    b_l_rook_moved = gamestate.b_l_rook_moved
    b_r_rook_moved = gamestate.b_r_rook_moved
    
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
                    
            if b_en_passant != None and r == 3 and abs(c-b_en_passant[1]) == 1:
                temp.append(b_en_passant)
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
                    
            if w_en_passant != None and r == 4 and abs(c-w_en_passant[1]) == 1:
                temp.append(w_en_passant)
        for move in temp:
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
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
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
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
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
                    res.append(move)
        
        castle_moves = []
        if colour(p) == "w":
            if w_king_moved == 0 and check_white_check(gamestate) == "":
                if w_r_rook_moved == 0 and board[7][7] == "R" and (7,5) in res and board[7][6] == " ":
                    castle_moves.append((7,6))
                if w_l_rook_moved == 0 and board[7][0] == "R" and (7,3) in res and board[7][2] == " " and board[7][1] == " ":
                    castle_moves.append((7, 2))
                    
        if colour(p) == "b":
            if b_king_moved == 0 and check_black_check(gamestate) == "":
                if b_r_rook_moved == 0 and board[0][7] == "r" and (0, 5) in res and board[0][6] == " ":
                    castle_moves.append((0, 6))
                if b_l_rook_moved == 0 and board [0][0] == "r" and (0, 3) in res and board[0][2] == " " and board[0][1] == " ":
                    castle_moves.append((0, 2))
                    
        for move in castle_moves:
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
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
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
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
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
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
            test_state = copy.deepcopy(gamestate)
            test_state.board[r][c] = " "
            test_state.board[move[0]][move[1]] = p
            if colour(p) == "w":
                if check_white_check(test_state) == "":
                    res.append(move)
            if colour(p) == "b":
                if check_black_check(test_state) == "":
                    res.append(move)
    return res

def check_white_moves(gamestate: GameState):
    board = gamestate.board
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if colour(p) == "w":
                if len(check_legal_moves(r, c, gamestate)) != 0:
                    return True
    return False

def check_black_moves(gamestate: GameState):
    board = gamestate.board
    for r, rank in enumerate(board):
        for c, p in enumerate(rank):
            if colour(p) == "b":
                if len(check_legal_moves(r, c, gamestate)) != 0:
                    return True
    return False

def check_checkmate(gamestate: GameState):
    if not(check_white_moves(gamestate)) and check_white_check(gamestate) == "w":
        return "w"
    if not(check_black_moves(gamestate)) and check_black_check(gamestate) == "b":
        return "b"
    if gamestate.turn == "w" and not check_white_moves(gamestate):
        return "d"
    if gamestate.turn == "b" and not check_black_moves(gamestate):
        return "d"
    return ""
 
def try_move(fr, fc, tr, tc, gamestate: GameState, uistate: UIState): 
    #move
    piece = gamestate.board[fr][fc]
    if (tr, tc) in check_legal_moves(fr, fc, gamestate):
        #Promotion Logic
        if (piece == "P" and tr == 0) or (piece == "p" and tr == 7):
            gamestate.promotion = (piece, tr, tc)
            gamestate.board[tr][tc] = piece
            gamestate.board[fr][fc] = " "

            uistate.clear()
            return
        if piece == "P":
            if fr - tr == 2:
                gamestate.w_en_passant = (tr + 1, tc)
            if (tr, tc) == gamestate.b_en_passant:
                gamestate.board[gamestate.b_en_passant[0]+1][gamestate.b_en_passant[1]] = " "
        if piece == "p":
            if fr - tr == -2:
                gamestate.b_en_passant = (tr - 1, tc)
            if (tr, tc) == gamestate.w_en_passant:
                gamestate.board[gamestate.w_en_passant[0]-1][gamestate.w_en_passant[1]] = " "
        
        
        if piece == "K":
            if gamestate.w_king_moved == 0 and (tr, tc) == (7, 6):
                gamestate.board[7][7] = " "
                gamestate.board[7][5] = "R"
                gamestate.w_r_rook_moved = 1
            if gamestate.w_king_moved == 0 and (tr, tc) == (7, 2):
                gamestate.board[7][0] = " "
                gamestate.board[7][3] = "R"
                gamestate.w_l_rook_moved = 1
        if piece == "k":
            if gamestate.b_king_moved == 0 and (tr, tc) == (0, 6):
                gamestate.board[0][7] = " "
                gamestate.board[0][5] = "r"
                gamestate.b_r_rook_moved = 1
            if gamestate.b_king_moved == 0 and (tr, tc) == (0, 2):
                gamestate.board[0][0] = " "
                gamestate.board[0][3] = "r"
                gamestate.b_l_rook_moved = 1
        
        gamestate.board[tr][tc] = piece
        gamestate.board[fr][fc] = " "
        
        if piece == "k": gamestate.b_king_moved = 1
        if piece == "K": gamestate.w_king_moved = 1
        if fr == 7 and fc == 0: gamestate.w_l_rook_moved = 1
        if fr == 7 and fc == 7: gamestate.w_r_rook_moved = 1
        if fr == 0 and fc == 0: gamestate.b_l_rook_moved = 1
        if fr == 0 and fc == 7: gamestate.b_r_rook_moved = 1
        
        uistate.clear()
        if gamestate.turn == "w" and gamestate.promotion == None:
            gamestate.b_en_passant = None
            gamestate.turn = "b"
        elif gamestate.turn == "b" and gamestate.promotion == None:
            gamestate.w_en_passant = None
            gamestate.turn = "w"
        gamestate.turns += 1
        gamestate.mate = check_checkmate(gamestate)
        return True
    return False
                
def draw_selected_overlay(screen: pygame.Surface, uistate: UIState):
    overlay = pygame.Surface((SQUARE_WIDTH, SQUARE_HEIGHT), pygame.SRCALPHA)
    overlay.fill((169, 123, 49, 191))

    for r, rank in enumerate(uistate.selected_board):
        for c, v in enumerate(rank):
            if v:
                screen.blit(overlay, (c*SQUARE_WIDTH, r*SQUARE_HEIGHT))
def draw_highlighted_overlay(screen: pygame.Surface, gamestate: GameState, uistate: UIState):
    for r, rank in enumerate(uistate.highlighted_board):
        for c, v in enumerate(rank):
            if v:
                if gamestate.board[r][c] == " ":
                    pygame.draw.circle(screen,(255, 0, 0), (c * SQUARE_WIDTH + SQUARE_WIDTH // 2, r * SQUARE_HEIGHT + SQUARE_HEIGHT // 2), SQUARE_WIDTH/7)
                else:
                    overlay_image = pygame.image.load(resource_path('overlay/square.png')).convert_alpha()
                    overlay_image = pygame.transform.scale(overlay_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
                    screen.blit(overlay_image, (c * SQUARE_WIDTH, r * SQUARE_HEIGHT))

def draw_promo_overlay(screen: pygame.Surface, gamestate: GameState):
    if gamestate.promotion != None:
        overlay_image = pygame.image.load(resource_path('overlay/promooverlay.png')).convert_alpha()
        overlay_image = pygame.transform.scale(overlay_image, (SQUARE_WIDTH*8, SQUARE_HEIGHT*8))
        screen.blit(overlay_image, (0,0))
def get_mate(gamestate: GameState):
    return gamestate.mate