"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
import SearchAlgos
import time
#TODO: you can import more modules, if needed


class Player(AbstractPlayer):
    def __init__(self, game_time, penalty_score):
        AbstractPlayer.__init__(self, game_time, penalty_score) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the Minimax algorithm from SearchAlgos.py
        self.game_time = game_time
        self.penalty_score = penalty_score

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, a 2D matrix of the board.
        No output is expected.
        """
        #TODO: erase the following line and implement this function.
        self.board = board
        for i in range(board.len):
            for j in range(board[0].len):
                if board[i][j] == 1:
                    self_pos = (i,j)
                if board[i][j] == 2:
                    enemy_pos = (i,j)


    def make_move(self, time_limit, players_score):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, chosen from self.directions
        """
        #TODO: erase the following line and implement this function.
        start_time = time.time()
        minimax_ret = 0
        counter = 1
        while(time.time() - start_time < time_limit):
            minimax_ret = MiniMax.search(self.board, counter, True)
            counter += 1
        return minimax_ret

    def set_rival_move(self, pos):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        #TODO: erase the following line and implement this function.
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
        #TODO: erase the following line and implement this function. In case you choose not to use it, use 'pass' instead of the following line.
        new_fruit_positions = fruits_on_board_dict.keys()
        for pos in self.cur_fruits.keys(): #Remove old fruits
            if pos not in new_fruit_positions:
                self.board[pos[0]][pos[1]] = 0

        for pos, val in fruits_on_board_dict: #Update new fruits
            if self.board[pos[0]][pos[1]] not in [-1,1,2]:
                self.board[pos[0]][pos[1]] = val

    ########## helper functions in class ##########
    #TODO: add here helper functions in class, if needed


    ########## helper functions for MiniMax algorithm ##########
    #TODO: add here the utility, succ, and perform_move functions used in MiniMax algorithm