import tkinter as tk
import re
from players import Human_Player, AI_Player
import random
import threading

# customizable dimensions
columns = 7
rows = 6

# dict for colors
player_color = {
    1: "red",
    2: "black"
}


class Connect4():
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.ongoing = True
        self.board = [[] for i in range(columns)]
        self.current_num = 1
        self.height = rows * 100 + 125
        self.width = columns * 100 + 50
        self.root = tk.Tk()
        self.root.title("Connect4")
        self.canvas = tk.Canvas(self.root, width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.header_text = self.canvas.create_text(
            self.width/2, 50,
            text=("It is Player 1's turn! (" +
                  player_color[self.current_num] + ")"))

    def change_header(self, text):
        self.canvas.itemconfigure(self.header_text, text=text)

    def get_legal_moves(self, board):
        return [num + 1 for num in range(columns) if len(board[num]) < rows]

    def draw_piece(self, move):
        col_length = len(self.board[move - 1])
        self.canvas.create_oval((move - 1) * 100 + 25,
                                self.height - 25 - (100 * col_length),
                                move * 100 + 25, self.height +
                                75 - (100 * col_length),
                                fill=player_color[self.current_num])
        self.canvas.after(100, self.canvas.update)

    def play_and_draw_move(self, move):
        self.board[move - 1].insert(0, self.current_num)
        self.draw_piece(move)

    def play_move(self, move, board, current_num):
        board[move - 1].insert(0, current_num)
        return board

    def fill_board(self, board):
        filled_board = []
        for column in board:
            if len(column) < rows:
                filled_column = [0 for i in range(rows - len(column))] + column
            else:
                filled_column = column
            filled_board.append(filled_column)
        return filled_board

    def switch_players(self):
        if self.current_num == 1:
            self.current_num = 2
        else:
            self.current_num = 1

    def check_column(self, column, player_num):
        consecutive = 0
        for num in column:
            if num == player_num:
                consecutive += 1
            else:
                consecutive = 0
            if consecutive >= 4:
                return True
        return False

    def check_all_columns(self, board, player_num):
        for column in board:
            if self.check_column(column, player_num):
                return True
        return False

    def transpose_board(self, board, x_dim, y_dim):
        transposed_board = [[board[col][row] for col in range(x_dim)]
                            for row in range(y_dim)]
        return transposed_board

    def check_all_rows(self, board, player_num):
        filled_board = self.fill_board(board)
        transposed_board = self.transpose_board(filled_board, columns, rows)
        return self.check_all_columns(transposed_board, player_num)

    def align_diagonals(self, board):
        aligned_board = [[3 for j in range(i)] + board[i] +
                         [3 for j in range(columns - i)]
                         for i in range(columns)]
        return aligned_board

    def check_diagonals(self, board, player_num):
        filled_board = self.fill_board(board)
        # used for checking forward diagonals
        aligned_board1 = self.align_diagonals(filled_board)
        # used for checking backwards diagonals (other direction)
        filled_board.reverse()
        aligned_board2 = self.align_diagonals(filled_board)
        transposed_board1 = self.transpose_board(aligned_board1, columns,
                                                 columns + rows)
        transposed_board2 = self.transpose_board(aligned_board2, columns,
                                                 columns + rows)
        return (self.check_all_columns(transposed_board1, player_num) or
                self.check_all_columns(transposed_board2, player_num))

    def check_win(self, board=None, player_num=None):
        if not board:
            board = self.board
        if not player_num:
            player_num = self.current_num
        return (self.check_all_columns(board, player_num) or
                self.check_all_rows(board, player_num) or
                self.check_diagonals(board, player_num))

    def check_tie(self, board=None):
        if not board:
            board = self.board
        for column in board:
            if len(column) < rows:
                return False
        return True

    def estimate_value(self, board):
        filled_board = self.fill_board(board)
        col_vals = self.column_values(filled_board)
        if col_vals == float("inf") or col_vals == float("-inf"):
            return col_vals
        row_vals = self.row_values(filled_board)
        if row_vals == float("inf") or row_vals == float("-inf"):
            return row_vals
        diag_vals = self.diagonal_values(filled_board)
        if diag_vals == float("inf") or diag_vals == float("-inf"):
            return diag_vals
        return col_vals + row_vals + diag_vals

    def column_values(self, board):
        value = 0
        for column in board:
            column_string = "".join([str(num) for num in column])
            win_regex_p1 = r'1111'
            threes_regex_p1 = r'0111|1110'
            twos_regex_p1 = r'0011|1100|0110'
            ones_regex_p1 = r'0001|1000|0100|0010'
            win_regex_p2 = r'2222'
            threes_regex_p2 = r'0222|2220'
            twos_regex_p2 = r'0022|2200|0220'
            ones_regex_p2 = r'0002|2000|0200|0020'
            if re.search(win_regex_p1, column_string):
                value = float("inf")
                break
            elif re.search(threes_regex_p1, column_string):
                value += 30
            elif re.search(twos_regex_p1, column_string):
                value += 15
            elif re.search(ones_regex_p1, column_string):
                value += 5
            if re.search(win_regex_p2, column_string):
                value = float("-inf")
                break
            elif re.search(threes_regex_p2, column_string):
                value -= 30
            elif re.search(twos_regex_p2, column_string):
                value -= 15
            elif re.search(ones_regex_p2, column_string):
                value -= 5
        return value

    def row_values(self, board):
        transposed_board = self.transpose_board(board,  columns, rows)
        return self.column_values(transposed_board)

    def diagonal_values(self, board):
        # used for checking forward diagonals
        aligned_board1 = self.align_diagonals(board)
        # used for checking backwards diagonals (other direction)
        board.reverse()
        aligned_board2 = self.align_diagonals(board)
        transposed_board1 = self.transpose_board(aligned_board1, columns,
                                                 columns + rows)
        transposed_board2 = self.transpose_board(aligned_board2, columns,
                                                 columns + rows)
        return (self.column_values(transposed_board1) +
                self.column_values(transposed_board2))

    def draw_grid(self):
        for col in range(columns + 1):
            self.canvas.create_line(col * 100 + 25, 100, col * 100 + 25,
                                    self.height - 25)
        for row in range(rows + 1):
            self.canvas.create_line(25, row * 100 + 100, self.width - 25,
                                    row * 100 + 100)

    def run_game(self):
        self.draw_grid()
        # randomize who goes first
        self.ai_first = random.choice([True, False])
        if self.ai_first:
            self.player1, self.player2 = (AI_Player(1, self),
                                          Human_Player(2, self))
        else:
            self.player1, self.player2 = (Human_Player(1, self),
                                          AI_Player(2, self))
        thread1 = threading.Thread(target=self.player1.run)
        thread2 = threading.Thread(target=self.player2.run)
        thread1.daemon = True
        thread2.daemon = True
        thread1.start()
        thread2.start()
        self.root.mainloop()
