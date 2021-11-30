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

    def validate_winning_move(self, board: dict) -> bool:
        pass

    def is_terminal(self, board: dict):
        pass

    def minimax(self, board: dict, depth: int, alpha: int, beta: int,
            maximizingPlayer: bool) -> tuple:
        pass

    def ai_move(self, board: dict):
        valid_columns = self.get_valid_columns(board)
        selected_column = valid_columns[randint(0, len(valid_columns)-1)]
        gb.validate_winner(gb.P2_AI, selected_column)
