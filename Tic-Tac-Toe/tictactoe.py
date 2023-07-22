import random as rd
import pygame as pg
import numpy as np
import copy
import sys

from constants import *

# Starter pygame
pg.init()
brett = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")
brett.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empyt_sqrs = self.squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        """
        Returnerer 0 hvis ingen har vunnet enda
        Returnerer 1 hvis spiller 1 vinner
        Returnerer 2 hvis spiler 2 vinner
        """

        # Vertikal seier
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRQ_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pg.draw.line(brett, color, iPos, fPos, LINE_WIN_WIDTH)
                return self.squares[0][col] # Returnerer 1
            
        # Horizontal seier
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRQ_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pg.draw.line(brett, color, iPos, fPos, LINE_WIN_WIDTH)    
                return self.squares[row][0]
        
        # Synkende diagonal seier
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRQ_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pg.draw.line(brett, color, iPos, fPos, LINE_WIN_WIDTH)
            return self.squares[1][1]

        # Stigende diagonal seier
        if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] != 0:
            if show:
                color = CIRQ_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pg.draw.line(brett, color, iPos, fPos, LINE_WIN_WIDTH)
            return self.squares[1][1]

        # Ingen seier enda
        return 0
    
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs        
    
    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = rd.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)
    
    def minimax(self, board, maximizing):
        # Terminal case
        case = board.final_state()

        # Player 1 wins
        if case == 1:
            return 1, None # eval, move
        # Player 2 wins
        if case == 2:
            return -1, None
        # Draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
        
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
    
    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # Minimax algo choice
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1=kyrss, 2=sirkel, bestemmer hvem som starter
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()


    def show_lines(self):
        brett.fill(BG_COLOR)
        # Tegner linjene til brettet

        # Loddrette linjer
        pg.draw.line(brett, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pg.draw.line(brett, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        
        # Vannrette linjer
        pg.draw.line(brett, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pg.draw.line(brett, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        # Tegner figurene
        if self.player == 1:
            # Tegner kryss

            # Synkende linje
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pg.draw.line(brett, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # Stigende loinje
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pg.draw.line(brett, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # Tegn sirkel
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pg.draw.circle(brett, CIRQ_COLOR, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1
    
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
    
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    game = Game()
    board = game.board
    ai = game.ai

    print(f"Gamemode: {game.gamemode}")
    print(f"AI modus: {ai.level}")

    # Main loop
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                # Trykk g for å endre gamemode
                if event.key == pg.K_g:
                    game.change_gamemode()
                    print(f"Gamemode: {game.gamemode}")
                
                # r-restart
                if event.key == pg.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                    print(f"Spillet ble resatt")

                # 0-random AI
                if event.key == pg.K_0:
                    ai.level = 0
                    print(f"AI modus: {ai.level}")

                # 1-minimax AI
                if event.key == pg.K_1:
                    ai.level = 1
                    print(f"AI modus: {ai.level}")

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
                if board.empty_sqr(row, col):
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False
            
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pg.display.update()

            # AI methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
                            
        pg.display.update()

main()