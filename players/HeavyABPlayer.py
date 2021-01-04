"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
from players.AbstractPlayer import AbstractPlayer
from SearchAlgos import AlphaBeta, get_legal_moves, calc_direction, just_get_any_legal_location
from SearchAlgos import find_longest_route
import time
from players.our_structurs import State


# TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.game_time = game_time
        self.penalty_score = penalty_score
        self.turn = 0

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.
        self.cur_fruits = None
        self.board = board
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 1:
                    self.self_pos = (i, j)
                if board[i][j] == 2:
                    self.enemy_pos = (i, j)


    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        # TODO: erase the following line and implement this function.
        #print('turn:', self.turn)
        #print(self.board)
        print('--------------------------------------------')

        # time_limit = 2
        start_time = time.time()

        state = State(self.board, self.penalty_score, players_score[0], players_score[1], self.cur_fruits, self.turn)


        minimax_ret = AlphaBeta(None, None, None).search(state=state, depth=2, maximizing_player=True, heuristic_type=44)

        new_pos = (state.my_location[0] + minimax_ret[1][0], state.my_location[1] + minimax_ret[1][1])
        self.board[state.my_location[0]][state.my_location[1]] = -1
        self.board[new_pos[0]][new_pos[1]] = 1
        self.turn += 1
        #print(self.board)
        #print()
        return minimax_ret[1]

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        self.board[self.enemy_pos[0]][self.enemy_pos[1]] = -1
        self.board[pos[0]][pos[1]] = 2
        self.enemy_pos = pos

    def update_fruits(self, fruits_on_board_dict):
        """Update your info on the current fruits on board (if needed).
        input:
            - fruits_on_board_dict: dict of {pos: value}
                                    where 'pos' is a tuple describing the fruit's position on board,
                                    'value' is the value of this fruit.
        No output is expected.
        """
        # TODO: erase the following line and implement this function. In case you choose not to use this function,
        # use 'pass' instead of the following line.
        new_fruit_positions = fruits_on_board_dict.keys()
        if self.cur_fruits is not None:
            for pos in self.cur_fruits.keys():  # Remove old fruits
                if pos not in new_fruit_positions and self.board[pos[0]][pos[1]] not in [-1, 1, 2]:
                    self.board[pos[0]][pos[1]] = 0

        for pos, val in fruits_on_board_dict.items():  # Update new fruits
            if self.board[pos[0]][pos[1]] not in [-1, 1, 2]:
                self.board[pos[0]][pos[1]] = val
        self.cur_fruits = fruits_on_board_dict

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm