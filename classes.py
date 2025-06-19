import sys
import pygame
import numpy as np
import random
import tkinter as tk

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols))
        self.SQUARESIZE = 30
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.width = cols * self.SQUARESIZE
        self.height = rows * self.SQUARESIZE

    def create(self):
        self.board = np.zeros((self.rows, self.cols))

    def is_available(self, row, col):
        return self.board[row][col] == 0

    def drop_piece(self, row, col, piece):
        if self.is_available(row, col):
            self.board[row][col] = piece

    def winning_move(self, piece):
        for c in range(self.cols - 5):
            for r in range(self.rows):
                if all(self.board[r][c + i] == piece for i in range(6)):
                    return True

        for c in range(self.cols):
            for r in range(self.rows - 5):
                if all(self.board[r + i][c] == piece for i in range(6)):
                    return True

        for c in range(self.cols - 5):
            for r in range(self.rows - 5):
                if all(self.board[r + i][c + i] == piece for i in range(6)):
                    return True

        for c in range(self.cols - 5):
            for r in range(5, self.rows):
                if all(self.board[r - i][c + i] == piece for i in range(6)):
                    return True

        return False

    def draw(self, screen, player_piece, ai_piece):
        for c in range(self.cols):
            for r in range(self.rows):
                pygame.draw.rect(
                    screen, (0, 0, 0),
                    (c * self.SQUARESIZE, r * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                )
                pygame.draw.rect(
                    screen, (225, 255, 0),
                    (c * self.SQUARESIZE + 1, r * self.SQUARESIZE + 1, self.SQUARESIZE - 1, self.SQUARESIZE - 1)
                )
        for c in range(self.cols):
            for r in range(self.rows):
                if self.board[r][c] == player_piece:
                    pygame.draw.circle(
                        screen, (255, 255, 255),
                        (c * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE // 2),
                        self.RADIUS
                    )
                elif self.board[r][c] == ai_piece:
                    pygame.draw.circle(
                        screen, (0, 0, 0),
                        (c * self.SQUARESIZE + self.SQUARESIZE // 2, r * self.SQUARESIZE + self.SQUARESIZE // 2),
                        self.RADIUS
                    )
        pygame.display.update()


class AI:
    def __init__(self, depth, board, ai_piece, player_piece):
        self.depth = depth
        self.board = board
        self.ai_piece = ai_piece
        self.player_piece = player_piece

    def heuristic(self, piece):
        # Add heuristic logic here
        return 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        # Add minimax logic here
        return (None, None, 0)

    def get_move(self):
        row, col, _ = self.minimax(self.board.board, self.depth, -float('inf'), float('inf'), True)
        return row, col


class Game:
    def __init__(self):
        self.board = None
        self.ai = None
        self.turn = random.randint(0, 1)
        self.game_over = False
        self.current_turn_moves = 0
        self.first_move = True
        self.player_piece = 1
        self.ai_piece = 2

    def start(self):
        def get_size():
            size = int(entry.get())
            if size >= 6:
                rows = cols = size
                self.board = Board(rows, cols)
                self.board.create()
                global screen
                screen = pygame.display.set_mode((self.board.width, self.board.height))
                self.ai = AI(1, self.board, self.ai_piece, self.player_piece)
                self.board.draw(screen, self.player_piece, self.ai_piece)
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

        button = tk.Button(root, text="Enter", width=15, command=get_size)
        button.pack(pady=10)

        root.mainloop()

    def run(self):
        pygame.init()
        pygame.display.set_caption("Connect 6")

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.turn == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0] // self.board.SQUARESIZE
                    mouseY = event.pos[1] // self.board.SQUARESIZE
                    if self.board.is_available(mouseY, mouseX):
                        self.board.drop_piece(mouseY, mouseX, self.player_piece)
                        self.current_turn_moves += 1
                        self.board.draw(screen, self.player_piece, self.ai_piece)
                        if self.board.winning_move(self.player_piece):
                            font = pygame.font.Font(None, 74)
                            text = font.render("Player Wins!", True, (255, 255, 255))
                            screen.blit(text, (self.board.width // 4, self.board.height // 2))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            self.game_over = True

                        if self.first_move or self.current_turn_moves == 2:
                            self.turn = (self.turn + 1) % 2
                            self.current_turn_moves = 0
                            self.first_move = False

            if self.turn == 1 and not self.game_over:
                row, col = self.ai.get_move()
                if row is not None and col is not None:
                    self.board.drop_piece(row, col, self.ai_piece)
                self.current_turn_moves += 1
                self.board.draw(screen, self.player_piece, self.ai_piece)
                if self.board.winning_move(self.ai_piece):
                    font = pygame.font.Font(None, 74)
                    text = font.render("AI Wins!", True, (0, 0, 0))
                    screen.blit(text, (self.board.width // 4, self.board.height // 2))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    self.game_over = True

                if self.current_turn_moves == 2 or self.first_move:
                    self.first_move = False
                    self.turn = (self.turn + 1) % 2
                    self.current_turn_moves = 0


if __name__ == "__main__":
    game = Game()
    game.start()
    game.run()
