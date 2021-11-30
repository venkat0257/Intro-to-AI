try:
    from random import randint
    from math import inf

    import game_board as gb
except ImportError as E:
    print(f'alpha_beta.py => {E}')


class AlphaBeta:
    def __init__(self):
        self.INFINITY     = inf
        self.NEG_INFINITY = self.INFINITY * -1

    # Returns columns from game board that are NOT full.
    def get_valid_columns(self, board_slots: dict):
        valid_columns = []

        for i in range(gb.GAME_BOARD_COLS):
            if board_slots.get((0, i)) == None:
                valid_columns.append(i)

        return valid_columns

    def window_counter(self, window: list, player: int):
        window_score = 0
        piece_color = gb.player_colors[player]
        opponent    = gb.player_colors[not bool(player)]

        if window.count(piece_color) == 4:
            window_score += 100
        elif window.count(piece_color) == 3 and window.count(None) == 1:
            window_score += 5
        elif window.count(piece_color) == 2 and window.count(None) == 2:
            window_score += 2

        if window.count(opponent) == 3 and window.count(None) == 1:
            window_score -= 4

        return window_score
    
    def validate_board_scores(self, board: list, player: int):
        board_score = 0

        # Dimensions for sliding window and board traversal.
        SLIDING_WINDOW_DIM = 4
        WINDOW_TRAVERSE_H  = gb.GAME_BOARD_ROWS - SLIDING_WINDOW_DIM + 1
        WINDOW_TRAVERSE_W  = gb.GAME_BOARD_COLS - SLIDING_WINDOW_DIM + 1

        # Validate board score - CENTER
        center_array = [i for i in list(board[:gb.GAME_BOARD_COLS//2])]
        center_count = center_array.count(gb.player_colors[player])
        board_score += center_count * 3

        # Validate board score - HORIZONTAL
        for r in range(gb.GAME_BOARD_ROWS):
            row_arr = [i for i in list(board[r:])]
            
            for c in range(WINDOW_TRAVERSE_W):
                window      = row_arr[c:c+SLIDING_WINDOW_DIM]
                board_score += self.window_counter(window, player)

        # Validate board score - VERTICAL
        for c in range(gb.GAME_BOARD_COLS):
            col_arr = [i for i in list(board[:c])]

            for r in range(WINDOW_TRAVERSE_H):
                window      = col_arr[r:r+SLIDING_WINDOW_DIM]
                board_score += self.window_counter(window, player)

        # Validate board score - DIAGONAL
        for r in range(WINDOW_TRAVERSE_H):
            for c in range(WINDOW_TRAVERSE_W):
                window      = [board[r+i][c+i] for i in range(SLIDING_WINDOW_DIM)]
                board_score += self.window_counter(window, player)
        for r in range(WINDOW_TRAVERSE_H):
            for c in range(WINDOW_TRAVERSE_W):
                window      = [board[r+3-i][c+i] for i in range(SLIDING_WINDOW_DIM)]
                board_score += self.window_counter(window, player)

        return board_score

    def validate_winning_move(self, board: dict) -> bool:
        pass

    def is_terminal(self, board: dict):
        pass

    def minimax(self, board: dict, depth: int, alpha: int, beta: int,
            maximizingPlayer: bool) -> tuple:
        pass

    def ai_move(self, board: dict):
        print(self.validate_board_scores(board, gb.P2_AI))
        # valid_columns = self.get_valid_columns(board)
        # selected_column = valid_columns[randint(0, len(valid_columns)-1)]
        # gb.validate_winner(gb.P2_AI, selected_column)
