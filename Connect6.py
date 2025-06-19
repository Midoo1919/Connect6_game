import sys
import pygame
import numpy as np
import random
import tkinter as tk


row = 6
col = 6


SQUARESIZE = 30
width = col * SQUARESIZE
height = row * SQUARESIZE
RADIUS = int(SQUARESIZE / 2 - 5)
 

PLAYER_PIECE = 1
AI_PIECE = 2


DEPTH = 1

def create_board():
    return np.zeros((row, col)) 


def is_available_place(board, row, col):
    return board[row][col] == 0

def drop_piece(board, row, col, piece):
    if (is_available_place (board , row , col)):
        board[row, col] = piece

def winning_move(board, piece):
   
    for c in range(col - 5):
        for r in range(row):
            if all(board[r][c + i] == piece for i in range(6)):
                return True
    
    for c in range(col):
        for r in range(row - 5):
            if all(board[r + i][c] == piece for i in range(6)):
                return True
    
    for c in range(col - 5):
        for r in range(row - 5):
            if all(board[r + i][c + i] == piece for i in range(6)):
                return True
    
    for c in range(col - 5):
        for r in range(5, row):
            if all(board[r - i][c + i] == piece for i in range(6)):
                return True
    return False

def draw_board(board):
    for c in range(col):
        for r in range(row):
            pygame.draw.rect(screen, (0, 0, 0), (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.rect(screen, (225, 255, 0), (int(c * SQUARESIZE + 1), int(r * SQUARESIZE + 1), SQUARESIZE - 1, SQUARESIZE - 1))
    for c in range(col):
        for r in range(row):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, (255, 255, 255), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, (0, 0, 0), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()
    

def heuristic(board, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    center_x, center_y = col // 2, row // 2
    if board[center_y][center_x] == piece:
        score += 25  
    for r in range(max(0, center_y - 1), min(row, center_y + 2)):
        for c in range(max(0, center_x - 1), min(col, center_x + 2)):
            if board[r][c] == piece:
                score += 10  

    
    for r in range(row):
        for c in range(col):
            if board[r][c] == piece:
                score += 5  

            if board[r][c] == opp_piece:
                score -= 10  

   
    corners = [(0, 0), (0, col - 1), (row - 1, 0), (row - 1, col - 1)]
    for r, c in corners:
        if board[r][c] == piece:
            score += 3  

    return score


def score_position(board, piece):
    score = 0

    for r in range(row):
        row_array = [i for i in list(board[r, :])]
        for c in range(col - 5):
            window = row_array[c:c + 6]
            score += evaluate_window(window, piece)

    for c in range(col):
        col_array = [int(board[r][c]) for r in range(row)]
        for r in range(row - 5):
            window = col_array[r:r + 6]
            score += evaluate_window(window, piece)

    for r in range(row - 5):
        for c in range(col - 5):
            window = [board[r + i][c + i] for i in range(6)]
            score += evaluate_window(window, piece)

    for r in range(5, row):
        for c in range(col - 5):
            window = [board[r - i][c + i] for i in range(6)]
            score += evaluate_window(window, piece)
    score += heuristic(board, piece)
    return score

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    if window.count(piece) == 6:
        score += 100
    elif window.count(piece) == 5 and window.count(0) == 1:
        score += 90
    elif window.count(piece) == 4 and window.count(0) == 2:
        score += 30
    elif window.count(piece) == 3 and window.count(0) == 3:
        score += 5
    if window.count(opp_piece) == 5 and window.count(0) == 1:
        score -= 90
    elif window.count(opp_piece) == 4 and window.count(0) == 2 :
        score -= 90
    elif window.count(opp_piece) == 3 and window.count(0) == 3 :
        score -= 5

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or not np.any(board == 0)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = [(r, c) for r in range(row) for c in range(col) if is_available_place(board, r, c)]
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, None, float('inf'))
            elif winning_move(board, PLAYER_PIECE):
                return (None, None, -float('inf'))
            else:  
                return (None, None, 0)
        else: 
            return (None, None, score_position(board, AI_PIECE))
    
    if maximizingPlayer:  
        value = -float('inf')
        best_move = None
        for r, c in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, r, c, AI_PIECE)  
            _, _, new_score = minimax(temp_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_move = (r, c)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        if best_move is None:
            return (None, None, value)
        else:
            return (best_move[0], best_move[1], value)
    else:  
        value = float('inf')
        best_move = None
        for r, c in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, r, c, PLAYER_PIECE) 
            _, _, new_score = minimax(temp_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_move = (r, c)
            beta = min(beta, value)
            if alpha >= beta:
                break
        if best_move is None:
            return (None, None, value)
        else:
            return (best_move[0], best_move[1], value)


def ai_turn(board):

    rowAI, colAI, _ = minimax(board, DEPTH, -float('inf'), float('inf'), True)

    if rowAI is not None and colAI is not None:  
        drop_piece(board, rowAI, colAI, AI_PIECE)  
    return rowAI, colAI


def start():
    def get_size():
        size = int(entry.get())
        if size >= 6:
            global row, col, width, height, board, screen
            row = col = size
            width = col * SQUARESIZE
            height = row * SQUARESIZE
            board = create_board()
            screen = pygame.display.set_mode((width, height))
            draw_board(board)
            root.destroy()
        else:
            label_error["text"] = "Please enter a size >= 6"

    root = tk.Tk()
    root.geometry("300x200")
    root.title("Board Size")

    label = tk.Label(root, text="Enter board size (min 6):")
    label.pack(pady=10)

    entry = tk.Entry(root, width=7, font=("Arial", 20))
    entry.pack(pady=10)

    label_error = tk.Label(root, text="", fg="red")
    label_error.pack()

    button = tk.Button(root, text="Enter",width=15, command=get_size)
    button.pack(pady=10)

    root.mainloop()

start()
pygame.init()
pygame.display.set_caption("Connect 6")
game_over = False
turn = random.randint(0,1) 
first_move = True
current_turn_moves = 0

draw_board(board)
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if turn == 0 and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0] // SQUARESIZE
            mouseY = event.pos[1] // SQUARESIZE
            if is_available_place(board, mouseY, mouseX):
                drop_piece(board, mouseY, mouseX, PLAYER_PIECE)
                current_turn_moves += 1
                draw_board(board)
                if winning_move(board, PLAYER_PIECE):
                    font = pygame.font.Font(None, 74)
                    text = font.render("Player Wins!", True, (255, 255, 255))
                    screen.blit(text, (width // 4, height // 2))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    game_over = True

                if first_move or current_turn_moves == 2:
                    turn = (turn + 1) % 2
                    current_turn_moves = 0
                    first_move = False

    if turn == 1 and not game_over:
        # pygame.time.wait(500)  
        rowAI, colAI = ai_turn(board)
        drop_piece(board, rowAI, colAI, AI_PIECE)
        current_turn_moves += 1
        draw_board(board)
        if winning_move(board, AI_PIECE):
            font = pygame.font.Font(None, 74)
            text = font.render("AI Wins!", True, (0, 0, 0))
            screen.blit(text, (width // 4, height // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            game_over = True


        if current_turn_moves == 2 or first_move:
            first_move = False
            turn = (turn + 1) % 2
            current_turn_moves = 0
