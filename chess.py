import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((850,620))
pygame.display.set_caption('Basic 1v1 Chess')
clock = pygame.time.Clock()
font = pygame.font.SysFont ("Consolas", 26)
w_font = pygame.font.SysFont("Consolas", 20)
b_font = pygame.font.SysFont("Consolas", 20)
text_surface = font.render('Chess.OS', True, 'White' )
w_surface = w_font.render("White Plays", True, 'White')
b_surface = b_font.render("Black Plays", True, 'Black')
check = pygame.font.SysFont("Consolas", 23)
check_surface = check.render("Check", True, (230, 160, 60))
big_font = pygame.font.SysFont("Consolas", 40, bold=True)
mate_surface = big_font.render("Checkmate", True, (230, 70, 50))
stalemate_surface = big_font.render("Draw!", True, (212, 175, 55))
horline_1 = pygame.Surface((600,10))
horline_2 = pygame.Surface((600,10))
verline_1 = pygame.Surface((10,600))
verline_2 = pygame.Surface((10,600))
verline_1.fill((101, 67, 33))
verline_2.fill((101, 67, 33))
horline_2.fill((101, 67, 33))
horline_1.fill((101, 67, 33))
Tile = 75 
board = [
["b_rook","b_knight","b_bish","b_queen","b_king","b_bish1","b_knight1","b_rook1"],
["b_pawn0","b_pawn1","b_pawn2","b_pawn3",
 "b_pawn4","b_pawn5","b_pawn6","b_pawn7"],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["","","","","","","",""],
["w_pawn0","w_pawn1","w_pawn2","w_pawn3",
 "w_pawn4","w_pawn5","w_pawn6","w_pawn7"],
["w_rook","w_knight","w_bish","w_queen",
 "w_king","w_bish1","w_knight1","w_rook1"]
]
pieces = {
"b_rook" : pygame.image.load('B_Rook.png').convert_alpha(),
"b_knight" : pygame.image.load ('B_Knight.png').convert_alpha(),
"b_bish"  : pygame.image.load('B_Bishop.png').convert_alpha(),
"b_rook1" : pygame.image.load('B_Rook.png').convert_alpha(),
"b_knight1" : pygame.image.load ('B_Knight.png').convert_alpha(),
"b_bish1"  : pygame.image.load('B_Bishop.png').convert_alpha(),
"b_queen" : pygame.image.load('B_Queen.png').convert_alpha(),
"b_king"  :  pygame.image.load('B_King.png').convert_alpha(),
"b_pawn0" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn1" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn2" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn3" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn4" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn5" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn6" : pygame.image.load('B_Pawn.png').convert_alpha(),
"b_pawn7" : pygame.image.load('B_Pawn.png').convert_alpha(),
"w_rook" : pygame.image.load('W_Rook.png').convert_alpha(),
"w_knight"  :  pygame.image.load ('W_Knight.png').convert_alpha(),
"w_bish" : pygame.image.load('W_Bishop.png').convert_alpha(),
"w_rook1" : pygame.image.load('W_Rook.png').convert_alpha(),
"w_knight1" : pygame.image.load ('W_Knight.png').convert_alpha(),
"w_bish1" : pygame.image.load('W_Bishop.png').convert_alpha(),
"w_queen" : pygame.image.load('W_Queen.png').convert_alpha(),
"w_king" : pygame.image.load('W_King.png').convert_alpha(),
"w_pawn0" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn1" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn2" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn3" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn4" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn5" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn6" : pygame.image.load('W_Pawn.png').convert_alpha(),
"w_pawn7" : pygame.image.load('W_Pawn.png').convert_alpha(),
}
for bk in pieces:
    pieces[bk] = pygame.transform.scale(pieces[bk],(75,75)) 
turn = 1 
selected  = None
first = "w"
movement_db = {}
last_move = None
check_status = False
mate_status = False
stalemate_status = False
game_over = False
winner_text = ""

def movement_store(m1, m2 ,b):
    if b not in movement_db:
        movement_db[b] = [(m1, m2)]
    if not movement_db[b] or movement_db[b][-1] != (m1, m2):
        movement_db[b].append((m1,m2))
    return movement_db

def promo():
    wr = 0
    br = 7
    for c in range(8):
        if board[wr][c].startswith("w_pawn"):
            return True,wr,c
        if board[br][c].startswith('b_pawn'):
            return True,br,c
    return False,wr,br

def valid_movement (curr_row ,curr_col ,prior_row ,prior_col , piece ,moves):
    if curr_row == prior_row and curr_col == prior_col:
        return False
    if piece.startswith("w_pawn"):
        if len(moves.get(piece, [])) == 0:
            if prior_row - curr_row == 1 and abs (curr_col - prior_col) == 1:
                if board[curr_row][curr_col].startswith('b'):
                    return True
            if (prior_row - 1 == curr_row  or prior_row - 2 == curr_row) and prior_col == curr_col:
                if board[curr_row][curr_col] == "":
                    if prior_row - curr_row == 2 and board[curr_row+1][curr_col] == "":
                        return True
                    if prior_row - curr_row == 1:
                        return True
        if last_move is not None:
            lm_piece, lm_or, lm_oc, lm_r, lm_c = last_move
            if lm_piece.startswith("b_pawn") and lm_or == 1 and lm_r == 3:
                if prior_row == 3 and curr_row == 2 and curr_col == lm_c and abs(curr_col - prior_col) == 1:
                    if board[curr_row][curr_col] == "":
                        return True
        if len(moves.get(piece, [])) > 0:
            if prior_row - 1 == curr_row and prior_col == curr_col:
                if board[curr_row][curr_col] == "":
                    return True
            if prior_row - curr_row == 1 and abs (curr_col - prior_col) == 1:
                if board[curr_row][curr_col].startswith('b'):
                    return True
    if piece.startswith("b_pawn"):
        if len(moves.get(piece, [])) == 0:
            if curr_row - prior_row == 1 and abs (prior_col - curr_col) == 1:
                if board[curr_row][curr_col].startswith('w'):
                    return True
            if (prior_row + 1 == curr_row or prior_row + 2 == curr_row) and prior_col == curr_col:
                if board[curr_row][curr_col] == "":

                    if curr_row - prior_row == 2 and board[curr_row-1][curr_col] == "":
                        return True
                    if curr_row - prior_row == 1:
                        return True
        if len(moves.get(piece, [])) > 0:
            if prior_row + 1 == curr_row and prior_col == curr_col:
                if board[curr_row][curr_col] == "":
                    return True
            if curr_row - prior_row == 1 and abs (prior_col - curr_col) == 1:
                if board[curr_row][curr_col].startswith('w'):
                    return True
        if last_move is not None:
            lm_piece, lm_or, lm_oc, lm_r, lm_c = last_move
            if lm_piece.startswith("w_pawn") and lm_or == 6 and lm_r == 4:
                if prior_row == 4 and curr_row == 5 and curr_col == lm_c and abs(curr_col - prior_col) == 1:
                    if board[curr_row][curr_col] == "":
                        return True
    if piece.startswith("w_rook"):
        if prior_row == curr_row or prior_col == curr_col:
            if prior_row != curr_row:
                if prior_row > curr_row:
                    for i in range(prior_row - curr_row - 1):
                        if board[prior_row - 1 - i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
                if curr_row > prior_row:
                    for i in range(curr_row - prior_row - 1):
                        if board[prior_row + 1 + i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
            if prior_col != curr_col:
                if prior_col > curr_col:
                    for i in range(prior_col - curr_col - 1):
                        if board[curr_row][prior_col - 1 - i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
                if curr_col > prior_col:
                    for i in range(curr_col - prior_col - 1):
                        if board[curr_row][prior_col + 1 + i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True                        
    if piece.startswith("b_rook"):
        if prior_row == curr_row or prior_col == curr_col:
            if prior_row != curr_row:
                if prior_row > curr_row:
                    for i in range(prior_row - curr_row - 1):
                        if board[prior_row - 1 - i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
                if curr_row > prior_row:
                    for i in range(curr_row - prior_row - 1):
                        if board[prior_row + 1 + i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
            if prior_col != curr_col:
                if prior_col > curr_col:
                    for i in range(prior_col - curr_col - 1):
                        if board[curr_row][prior_col - 1 - i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
                if curr_col > prior_col:
                    for i in range(curr_col - prior_col - 1):
                        if board[curr_row][prior_col + 1 + i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True                    
    if piece.startswith("w_bish"):
        if abs(curr_row - prior_row) == abs(curr_col - prior_col):
            for i in range(1,abs(curr_row - prior_row)):
                if curr_row > prior_row and  curr_col > prior_col:
                    if board[curr_row - i][curr_col - i] != "": 
                        return False
                if curr_row > prior_row and  curr_col < prior_col:
                    if board[curr_row - i][curr_col + i] != "": 
                        return False
                if curr_row < prior_row and  curr_col > prior_col:
                    if board[curr_row + i][curr_col - i] != "": 
                        return False
                if curr_row < prior_row and  curr_col < prior_col:
                    if board[curr_row + i][curr_col + i] != "": 
                        return False  
            if (board[curr_row][curr_col].startswith('b') or board[curr_row][curr_col] == ""):
                return True         
    if piece.startswith("b_bish"):
        if abs(curr_row - prior_row) == abs(curr_col - prior_col):
            for i in range(1,abs(curr_row - prior_row)):
                if curr_row > prior_row and  curr_col > prior_col:
                    if board[curr_row - i][curr_col - i] != "": 
                        return False
                if curr_row > prior_row and  curr_col < prior_col:
                    if board[curr_row - i][curr_col + i] != "": 
                        return False
                if curr_row < prior_row and  curr_col > prior_col:
                    if board[curr_row + i][curr_col - i] != "": 
                        return False
                if curr_row < prior_row and  curr_col < prior_col:
                    if board[curr_row + i][curr_col + i] != "": 
                        return False  
            if (board[curr_row][curr_col].startswith('w') or board[curr_row][curr_col] == ""):
                return True 
    if piece.startswith("w_queen"):
        if prior_row == curr_row or prior_col == curr_col:
            if prior_row != curr_row:
                if prior_row > curr_row:
                    for i in range(prior_row - curr_row - 1):
                        if board[prior_row - 1 - i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
                if curr_row > prior_row:
                    for i in range(curr_row - prior_row - 1):
                        if board[prior_row + 1 + i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
            if prior_col != curr_col:
                if prior_col > curr_col:
                    for i in range(prior_col - curr_col - 1):
                        if board[curr_row][prior_col - 1 - i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
                if curr_col > prior_col:
                    for i in range(curr_col - prior_col - 1):
                        if board[curr_row][prior_col + 1 + i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('w'):
                        return False
                    return True
        if abs(curr_row - prior_row) == abs(curr_col - prior_col):
            for i in range(1,abs(curr_row - prior_row)):
                if curr_row > prior_row and  curr_col > prior_col:
                    if board[curr_row - i][curr_col - i] != "": 
                        return False
                if curr_row > prior_row and  curr_col < prior_col:
                    if board[curr_row - i][curr_col + i] != "": 
                        return False
                if curr_row < prior_row and  curr_col > prior_col:
                    if board[curr_row + i][curr_col - i] != "": 
                        return False
                if curr_row < prior_row and  curr_col < prior_col:
                    if board[curr_row + i][curr_col + i] != "": 
                        return False  
            if (board[curr_row][curr_col].startswith('b') or board[curr_row][curr_col] == ""):
                return True 
    if piece.startswith("b_queen"):
        if prior_row == curr_row or prior_col == curr_col:
            if prior_row != curr_row:
                if prior_row > curr_row:
                    for i in range(prior_row - curr_row - 1):
                        if board[prior_row - 1 - i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
                if curr_row > prior_row:
                    for i in range(curr_row - prior_row - 1):
                        if board[prior_row + 1 + i][curr_col] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
            if prior_col != curr_col:
                if prior_col > curr_col:
                    for i in range(prior_col - curr_col - 1):
                        if board[curr_row][prior_col - 1 - i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
                if curr_col > prior_col:
                    for i in range(curr_col - prior_col - 1):
                        if board[curr_row][prior_col + 1 + i] != "":
                            return False
                    if board[curr_row][curr_col].startswith('b'):
                        return False
                    return True
        if abs(curr_row - prior_row) == abs(curr_col - prior_col):
            for i in range(1,abs(curr_row - prior_row)):
                if curr_row > prior_row and  curr_col > prior_col:
                    if board[curr_row - i][curr_col - i] != "": 
                        return False
                if curr_row > prior_row and  curr_col < prior_col:
                    if board[curr_row - i][curr_col + i] != "": 
                        return False
                if curr_row < prior_row and  curr_col > prior_col:
                    if board[curr_row + i][curr_col - i] != "": 
                        return False
                if curr_row < prior_row and  curr_col < prior_col:
                    if board[curr_row + i][curr_col + i] != "": 
                        return False  
            if (board[curr_row][curr_col].startswith('w') or board[curr_row][curr_col] == ""):
                return True 
            
    if piece.startswith("w_king"):
        if abs(curr_row - prior_row) <= 1 and abs(curr_col - prior_col) <= 1 and not board[curr_row][curr_col].startswith('w'):
            return True
        if len(moves.get(piece, [])) == 0:
            if abs(curr_col - prior_col) == 2 and curr_row == prior_row:
                if curr_col > prior_col:
                    if board[curr_row][7] != 'w_rook1' or len(moves.get('w_rook1', [])) > 0:
                        return False
                    for i in range(curr_col - prior_col):
                        if board[curr_row][curr_col-i] != '':
                            return False
                    return True
                else:
                    if board[curr_row][0] != 'w_rook' or len(moves.get('w_rook', [])) > 0:
                        return False
                    for i in range(1, 4):
                        if board[curr_row][i] != '':
                            return False
                    return True
    if piece.startswith("b_king"):
        if abs(curr_row - prior_row) <= 1 and abs(curr_col - prior_col) <= 1 and not board[curr_row][curr_col].startswith('b'):
            return True
        if len(moves.get(piece, [])) == 0:
            if abs(curr_col - prior_col) == 2 and curr_row == prior_row:
                if curr_col > prior_col:
                    if board[curr_row][7] != 'b_rook1' or len(moves.get('b_rook1', [])) > 0:
                        return False
                    for i in range(curr_col - prior_col):
                        if board[curr_row][curr_col-i] != '':
                            return False
                    return True
                else:
                    if board[curr_row][0] != 'b_rook' or len(moves.get('b_rook', [])) > 0:
                        return False
                    for i in range(1, 4):
                        if board[curr_row][i] != '':
                            return False
                    return True
                
    if piece.startswith("w_knight"):
        if (abs(curr_col-prior_col) == 2 and abs(curr_row-prior_row) == 1 or abs(curr_col-prior_col) == 1 and abs(curr_row-prior_row) == 2) and not board[curr_row][curr_col].startswith('w'):
            return True
    if piece.startswith("b_knight"):
        if (abs(curr_col-prior_col) == 2 and abs(curr_row-prior_row) == 1 or abs(curr_col-prior_col) == 1 and abs(curr_row-prior_row) == 2) and not board[curr_row][curr_col].startswith('b'):
            return True 
    return False

def is_in_check(color):
    king_name = color + "_king"
    king_r, king_c = -1, -1
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_name:
                king_r, king_c = r, c
                break
        if king_r != -1:
            break
    if king_r == -1:
        return False     
    enemy_color = "b" if color == "w" else "w"
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece.startswith(enemy_color):
                if valid_movement(king_r, king_c, r, c, piece, movement_db):
                    return True
    return False

def is_mate(color):
    if not is_in_check(color):
        return False
    for start_r in range(8):
        for start_c in range(8):
            piece = board[start_r][start_c]
            if piece.startswith(color):
                for end_r in range(8):
                    for end_c in range(8):
                        if valid_movement(end_r, end_c, start_r, start_c, piece, movement_db):
                            target_piece = board[end_r][end_c]
                            board[end_r][end_c] = piece
                            board[start_r][start_c] = ""
                            still_in_check = is_in_check(color)                            
                            board[start_r][start_c] = piece
                            board[end_r][end_c] = target_piece
                            if not still_in_check:
                                return False                             
    return True

def is_stalemate(color):
    if is_in_check(color):
        return False
    for start_r in range(8):
        for start_c in range(8):
            piece = board[start_r][start_c]
            if piece.startswith(color):
                for end_r in range(8):
                    for end_c in range(8):
                        if valid_movement(end_r, end_c, start_r, start_c, piece, movement_db):
                            target_piece = board[end_r][end_c]
                            board[end_r][end_c] = piece
                            board[start_r][start_c] = ""
                            still_in_check = is_in_check(color)                            
                            board[start_r][start_c] = piece
                            board[end_r][end_c] = target_piece
                            if not still_in_check:
                                return False 
    return True


while True:
    screen.fill((60, 50, 40))
    pawn_promo_status, pr, pc = promo()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = (mouse_x-150)//75
            row = (mouse_y-10)//75
            if pawn_promo_status:
                old_name = board[pr][pc]
                promoted = False
                if board[pr][pc].startswith('w'):
                    if 30 <= mouse_x < 105 and 100 <= mouse_y < 175:
                        new_name = 'w_queen_'+ old_name[-1]
                        pieces[new_name] = pieces['w_queen']
                        board[pr][pc] =  new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 175 <= mouse_y < 250:
                        new_name = 'w_rook_'+old_name[-1]
                        pieces[new_name] = pieces['w_rook']
                        board[pr][pc] = new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 250 <= mouse_y < 325:
                        new_name = 'w_bish_'+old_name[-1]
                        pieces[new_name] = pieces["w_bish"]
                        board[pr][pc] =  new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 325 <= mouse_y < 400:
                        new_name = 'w_knight_'+old_name[-1]
                        pieces[new_name] = pieces['w_knight']
                        board[pr][pc] =  new_name
                        promoted = True
                if board[pr][pc].startswith('b'):
                    if 30 <= mouse_x < 105 and 100 <= mouse_y < 175:
                        new_name = 'b_queen_'+ old_name[-1]
                        pieces[new_name] = pieces['b_queen']
                        board[pr][pc] =  new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 175 <= mouse_y < 250:
                        new_name = 'b_rook_'+old_name[-1]
                        pieces[new_name] = pieces['b_rook']
                        board[pr][pc] = new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 250 <= mouse_y < 325:
                        new_name = 'b_bish_'+old_name[-1]
                        pieces[new_name] = pieces["b_bish"]
                        board[pr][pc] =  new_name
                        promoted = True
                    if 30 <= mouse_x < 105 and 325 <= mouse_y < 400:
                        new_name = 'b_knight_'+old_name[-1]
                        pieces[new_name] = pieces['b_knight']
                        board[pr][pc] =  new_name
                        promoted = True
                if promoted:
                    check_status = is_in_check(first)
                    mate_status = is_mate(first)
                    stalemate_status = is_stalemate(first)
                    if mate_status or stalemate_status:
                        game_over = True
                        if mate_status:
                            winner_text = "Black Wins!" if first == "w" else "White Wins!"

            elif 0 <= row < 8 and 0 <= col <8:
                    if selected is None:
                        if board[row][col] != "" and board[row][col].startswith(first):
                            selected = (row, col)
                    else:
                        oldrow, oldcol = selected
                        if oldrow == row and oldcol == col:
                            selected = None
                        else:
                            if board[oldrow][oldcol] not in movement_db:
                                movement_db[board[oldrow][oldcol]] = []
                            piece_name = board[oldrow][oldcol]
                            if piece_name.endswith("king") and abs(col - oldcol) == 2 and row == oldrow:
                                castle_color = "w" if piece_name.startswith("w") else "b"
                                if is_in_check(castle_color):
                                    selected = None
                                    continue
                                transit_col = 5 if col > oldcol else 3
                                if board[oldrow][transit_col] == "":
                                    board[oldrow][transit_col] = piece_name
                                    board[oldrow][oldcol] = ""
                                    transit_attacked = is_in_check(castle_color)
                                    board[oldrow][oldcol] = piece_name
                                    board[oldrow][transit_col] = ""
                                    if transit_attacked:
                                        selected = None
                                        continue
                            if valid_movement(row, col, oldrow, oldcol, piece_name, movement_db):
                                is_ep = (piece_name.startswith("w_pawn") or piece_name.startswith("b_pawn")) \
                                    and abs(col - oldcol) == 1 and board[row][col] == ""
                                target_piece = board[row][col]
                                board[row][col] = piece_name
                                board[oldrow][oldcol] = ""
                                if piece_name.startswith("w_king") or piece_name.startswith("b_king"):
                                    if abs(col - oldcol) == 2:
                                        if col > oldcol:
                                            rook_name = board[row][7]
                                            board[row][5] = rook_name
                                            board[row][7] = ""
                                            movement_store(row, 5, rook_name)
                                        else:
                                            rook_name = board[row][0]
                                            board[row][3] = rook_name
                                            board[row][0] = ""
                                            movement_store(row, 3, rook_name)
                                own_color = "w" if piece_name.startswith("w") else "b"
                                if is_in_check(own_color):
                                    board[oldrow][oldcol] = piece_name
                                    board[row][col] = target_piece
                                else:
                                    if is_ep:
                                        board[oldrow][col] = ""
                                    movement_store(row, col, piece_name)
                                    selected = None 
                                    if board[row][col].startswith("w"):
                                        turn -=1 
                                        first = "b"
                                    else:
                                        turn += 1
                                        first = "w"
                                    last_move = (piece_name, oldrow, oldcol, row, col)  
                                    enemy_color = first                                   
                                    check_status = is_in_check(enemy_color)
                                    mate_status = is_mate(enemy_color)
                                    stalemate_status = is_stalemate(enemy_color)
                                    if mate_status or stalemate_status:
                                        game_over = True
                                        if mate_status:
                                            winner_text = "White Wins!" if own_color == "w" else "Black Wins!"

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(horline_1,(150,0))
    screen.blit(horline_2,(150,610))
    screen.blit(verline_1,(140,10))
    screen.blit(verline_2,(750,10))
    x = 150
    y = 10
    for x1 in range(4):
        for y1 in range(4):
            pygame.draw.rect(screen,(240, 217, 181), (x, y, Tile, Tile))
            x  += 150  
            if y1 ==  3:
                x  = 150
                y += 150
    a = 225
    b = 85           
    for x1 in range(4):
        for y1 in range(4):
            pygame.draw.rect(screen,(240, 217, 181), (a, b, Tile, Tile))
            a  += 150  
            if y1 ==  3:
                a  = 225
                b += 150
    x = 150
    b = 85
    for x1 in range(4):
        for y1 in range(4):
            pygame.draw.rect(screen,(181, 136, 99), (x, b, Tile, Tile))
            x  += 150  
            if y1 ==  3:
                x  = 150
                b += 150
    a = 225
    y = 10
    for x1 in range(4):
        for y1 in range(4):
            pygame.draw.rect(screen,(181, 136, 99), (a, y, Tile, Tile))
            a  += 150  
            if y1 ==  3:
                a  = 225
                y += 150
                
    position_x = 150
    position_y = 10
    for row, i in enumerate(board):
        for col, j in enumerate(i):
            position_x = 150 + col * 75
            position_y = 10 + row * 75
            if j != "":
                screen.blit(
                    pieces[j],
                    (position_x, position_y)
                )
            position_x += 75
        position_x = 150
        position_y += 75 
    if selected is not None:
        row, col = selected
        pygame.draw.rect(screen, "Red" , (150 + col * 75 , 10 + row * 75, 75, 75), 4 )
    if turn == 1:
        screen.blit(w_surface,(9 ,500 ))
    if turn == 0:
        screen.blit(b_surface,(9, 500 ))
    screen.blit(text_surface,(10,20))
    if pawn_promo_status:
        if board[pr][pc].startswith('b'):
            screen.blit(pieces["b_queen"],(30, 100))
            screen.blit(pieces["b_rook"],(30, 175))
            screen.blit(pieces["b_bish"],(30, 250))
            screen.blit(pieces["b_knight"],(30, 325))
        else:
            screen.blit(pieces["w_queen"],(30, 100))
            screen.blit(pieces["w_rook"],(30, 175))
            screen.blit(pieces["w_bish"],(30, 250))
            screen.blit(pieces["w_knight"],(30, 325))

    if mate_status or stalemate_status:
        overlay = pygame.Surface((850, 620))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        if mate_status:
            msg_surface = big_font.render("Checkmate", True, (230, 70, 50))
        else:
            msg_surface = big_font.render("Draw!", True, (212, 175, 55))

        text_rect = msg_surface.get_rect(center=(425, 310))     
        box_rect = text_rect.inflate(60, 40)                    
        pygame.draw.rect(screen, (30, 25, 20), box_rect)      
        pygame.draw.rect(screen, (212, 175, 55), box_rect, 3)    
        screen.blit(msg_surface, text_rect)
        if mate_status and winner_text != "":
            win_surface = w_font.render(winner_text, True, (230, 220, 200))
            win_rect = win_surface.get_rect(center=(425, 570))
            screen.blit(win_surface, win_rect)
    elif check_status:
        screen.blit(check_surface, (30,280))
    pygame.display.update()
    clock.tick(60)