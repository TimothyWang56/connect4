import copy

# dict for colors
player_color = {
    1: "red",
    2: "black"
}


class Player():
    def __init__(self, num, connect4):
        self.num = num
        self.connect4 = connect4

    def choose_move(self, connect4):
        pass

    def check_win(self):
        if self.connect4.check_win(self.connect4.board,
                                   self.connect4.current_num):
            self.connect4.change_header("Player " +
                                        str(self.connect4.current_num) +
                                        " wins!")
            self.connect4.ongoing = False
            self.connect4.canvas.unbind("<Button 1>")
        elif self.connect4.check_tie(self.connect4.board):
            self.connect4.change_header("It's a tie!")
            self.connect4.ongoing = False
            self.connect4.canvas.unbind("<Button 1>")
        else:
            self.connect4.switch_players()
            self.connect4.change_header("It is Player " +
                                        str(self.connect4.current_num) +
                                        "'s turn! (" +
                                        player_color[self.connect4.current_num]
                                        + ")")


class Human_Player(Player):
    def click_move(self, event):
        if (self.connect4.ongoing and
                event.x > 25 and
                event.x < self.connect4.width - 25 and
                event.y > 100 and
                event.y < self.connect4.height - 25):
            column = (event.x - 25)//100 + 1
            if column in self.connect4.get_legal_moves(self.connect4.board):
                self.connect4.play_and_draw_move(column)
                self.connect4.canvas.unbind("<Button 1>")
                self.check_win()
            else:
                self.connect4.change_header("That's not a valid move!" +
                                            "Play again!")
                self.connect4.canvas.unbind("<Button 1>")
                self.connect4.canvas.after(
                    3000,
                    lambda: self.connect4.change_header(
                        "It is Player " +
                        str(self.connect4.current_num) +
                        "'s turn! (" +
                        player_color[self.connect4.current_num] +
                        ")"))
                self.connect4.canvas.bind("<Button 1>", self.click_move)

    def run(self):
        while self.connect4.ongoing:
            if self.connect4.current_num == self.num:
                self.connect4.canvas.bind("<Button 1>", self.click_move)
            else:
                self.connect4.canvas.unbind("<Button 1>")


class AI_Player(Player):

    def minimax_helper(self, board, connect4, depth, current_num):
        legal_moves = connect4.get_legal_moves(board)
        lst = [connect4.play_move(move, copy.deepcopy(board), current_num)
               for move in legal_moves]
        if depth == 1:
            estimate_value_list = [connect4.estimate_value(state)
                                   for state in lst]
            if current_num == 1:
                return (legal_moves, estimate_value_list,
                        max(estimate_value_list))
            else:
                return (legal_moves, estimate_value_list,
                        min(estimate_value_list))
        else:
            if current_num == 1:
                lst2 = [self.minimax_helper(state, connect4, depth - 1, 2)[2]
                        for state in lst]
                return legal_moves, lst2, max(lst2)
            else:
                lst2 = [self.minimax_helper(state, connect4, depth - 1, 1)[2]
                        for state in lst]
                return legal_moves, lst2, min(lst2)

    def minimax(self, connect4):
        board = connect4.board
        moves_values_best = self.minimax_helper(board, connect4, 4,
                                                connect4.current_num)
        return moves_values_best[0][moves_values_best[1]
                                    .index(moves_values_best[2])]

    def choose_move(self):
        move = self.minimax(self.connect4)
        return move

    def run(self):
        while self.connect4.ongoing:
            if self.connect4.current_num == self.num:
                move = self.choose_move()
                self.connect4.play_and_draw_move(move)
                self.check_win()
