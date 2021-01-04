"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
import collections

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
        # time_limit = 2
        start_time = time.time()
        state = State(self.board, self.penalty_score, players_score[0], players_score[1], self.cur_fruits, self.turn)
        succ = self.sorted_moves
        utility = self.calc_score
        preform_move = self.preform_move

        state = State(self.board, self.penalty_score, players_score[0], players_score[1], self.cur_fruits, self.turn)


        minimax_ret = AlphaBeta(succ=succ,utility=utility, perform_move= preform_move).search(state=state, depth=4, maximizing_player=True, heuristic_type=1)

        new_pos = (state.my_location[0] + minimax_ret[1][0], state.my_location[1] + minimax_ret[1][1])
        self.board[state.my_location[0]][state.my_location[1]] = -1
        self.board[new_pos[0]][new_pos[1]] = 1
        self.turn += 1
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
    def preform_move(self, state: State, dest_location, IsMyTurn) -> State:
        board = state.board.copy()
        my_location = state.my_location
        rival_loaction = state.rival_location
        my_score = state.my_score
        rival_score = state.rival_score
        turn = state.turn
        penalty = state.fine_score
        fruits = state.fruits.copy()
        if IsMyTurn == True:
            state.turn + 1
            board[my_location[0]][my_location[1]] = -1
            if board[dest_location[0]][dest_location[1]] > 2:
                my_score += board[dest_location[0]][dest_location[1]]
            board[dest_location[0]][dest_location[1]] = 1
            my_location = dest_location
        else:
            board[rival_loaction[0]][rival_loaction[1]] = -1
            rival_loaction = dest_location
            if board[dest_location[0]][dest_location[1]] > 2:
                rival_score += board[dest_location[0]][dest_location[1]]
            board[dest_location[0]][dest_location[1]] = 2

        if self.can_I_move(board, my_location) == False:
            my_score -= penalty
        if self.can_I_move(board, rival_loaction) == False:
            rival_score -= penalty
        new_state = State(board, penalty, my_score, rival_score, fruits, turn)
        return new_state

    def calc_score(self, state, player_type):
        if not self.can_I_move(state.board, state.my_location):
            state.my_score -= state.fine_score
        if not self.can_I_move(state.board, state.rival_location):
            state.rival_score -= state.fine_score
        return state.my_score - state.rival_score

    def can_I_move(self, board, pos):
        num_steps_available = 0
        for d in self.get_directions():
            i = pos[0] + d[0]
            j = pos[1] + d[1]

            # check legal move
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
                # print(num_steps_available, '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                num_steps_available += 1
        # print(pos, 'line 33')
        if num_steps_available == 0:
            return False
        return True

    """
    def perform_move(state, move):
        #TODO: given a state and a move, returns the new state after the move
    """

    def calc_dist(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def succ(self, board, close, cur_pos, depth):
        states = set()
        if cur_pos is None:
            print('hi')
            print("\n\nBoard = ", board, "\n\n")
        for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
            if not (0 <= new_pos[0] < len(board) and 0 <= new_pos[1] < len(board[0])) \
                    or board[new_pos[0]][new_pos[1]] in [1, 2, -1] or new_pos in close:
                continue
            states.add((new_pos, depth + 1))
        return states

    def find_fruits(self, state):
        close, open = set(), collections.deque([(state.my_location, 0)])
        close.add(state.my_location)
        fruits = {}
        while open:
            cur = open.popleft()
            close.add(cur[0])
            if cur[1] == min(len(state.board), len(state.board[0])) - state.turn:
                continue
            for next in self.succ(state.board, close, cur[0], cur[1]):
                if state.board[next[0][0]][next[0][1]] > 2:
                    fruits[next[0]] = next[1]
                open.append(next)
        return fruits

    def find_longest_route_aux(self, board, curr_pos, new_pos, depth):
        temp_board = board.copy()
        temp_board[curr_pos[0]][curr_pos[1]] = -1
        if depth == 5:
            return 0
        max = 0
        if not self.can_I_move(temp_board, new_pos):
            return 0
        for d in get_legal_moves(board, new_pos):
            temp = 1 + self.find_longest_route_aux(temp_board, new_pos, d, depth + 1)
            if temp > max:
                max = temp
        return max

    def find_longest_route(self, state, isMe):
        max = 0
        if isMe == True:
            for d in get_legal_moves(state.board, state.my_location):
                temp = self.find_longest_route_aux(state.board, state.my_location, d, 0)
                if temp > max:
                    max = temp
        else:
            for d in get_legal_moves(state.board, state.rival_location):
                temp = self.find_longest_route_aux(state.board, state.rival_location, d, 0)
                if temp > max:
                    max = temp
        return max

    def just_get_any_legal_location(self, state: State):
        loc = get_legal_moves(state.board, state.my_location)[0]
        return calc_direction(state.my_location, loc)

    def calc_nearby_fruits(self, state, location):
        score = 0
        for key, value in state.fruits.items():
            if self.calc_dist(location, key) <= 3:
                score += value * 0.1
        return score

    def heuristic_calc(self, state, isMe):
        heuristic = 0
        max_fruit = -100000000
        for key, value in state.fruits.items():
            if isMe is True:
                location = state.my_location
            else:
                location = state.rival_location
            real_value = state.fruits[key] - 0.1 * value * (self.calc_dist(key, location)) + self.calc_nearby_fruits(state, key)
            if real_value > max_fruit:
                max_fruit = real_value
        if max_fruit == -100000000:
            heuristic += find_longest_route(state, True) * (state.fine_score / 1)
            heuristic -= find_longest_route(state, False) * (state.fine_score / 2)
            # print(x)
        else:
            if max_fruit == 0:
                max_fruit = 1
            heuristic += find_longest_route(state, True) * (state.fine_score / (max_fruit * 3)) * 2
            heuristic -= find_longest_route(state, False) * (state.fine_score / (max_fruit * 6)) * 1 / 2
            heuristic += real_value
        return heuristic

    # returns the value of the closest fruit (manhattan distance)
    def heuristic_calc_light(self, state):
        heuristic = 0
        fruits = self.find_fruits(state)
        fruit_time = min(len(state.board), len(state.board[1])) - state.turn
        min_dist = 10000
        score = 0
        for key, value in list(fruits.items()):
            if self.calc_dist(state.my_location, key) < min_dist:
                min_dist = self.calc_dist(state.my_location, key)
                score = state.fruits[key]
        return score

    def get_legal_moves(self, board, location):
        legal_moves = []
        for d in self.get_directions():
            i = location[0] + d[0]
            j = location[1] + d[1]

            # check legal move
            if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
                legal_moves.append((i, j))
        return legal_moves

    def remove_fruits_from_board(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] > 2:
                    board[i][j] = 0

    def calc_direction(self, old_loc, new_loc):
        return (new_loc[0] - old_loc[0], new_loc[1] - old_loc[1])

    def can_I_win_with_fine(self, state: State, maximizing_player):
        if maximizing_player is True:
            return state.my_score - state.rival_score > state.fine_score

        return state.rival_score - state.my_score > state.fine_score

    def get_heuristic_for_move(self, state, move, agent, heuristic_type):
        if heuristic_type == 0:
            return self.heuristic_calc(state, agent)
        if heuristic_type == 1:
            return self.heuristic_calc_light(self.preform_move(state, move, agent))

    def sorted_moves(self, state, agent, heuristic_type):
        if agent is True:
            moves = get_legal_moves(state.board, state.my_location)
        else:
            moves = get_legal_moves(state.board, state.rival_location)
        # Change here?
        moves.sort(key=(lambda move: self.get_heuristic_for_move(state, move, agent, heuristic_type)))
        return moves

    def get_directions(self):
        """Returns all the possible directions of a player in the game as a list of tuples.
        """
        return [(1, 0), (0, 1), (-1, 0), (0, -1)]