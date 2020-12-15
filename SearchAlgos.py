"""Search Algos: MiniMax, AlphaBeta
"""
import collections

from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT, get_directions

from players.our_structurs import State


def calc_score(state, new_pos, player_type):
    board_pos = state.board[new_pos[0]][new_pos[1]]
    added_score = 0
    if board_pos > 2:
        added_score += board_pos
    temp_board = state.board
    if not can_I_move(state.board, new_pos):
        added_score -= state.fine_score
    if player_type == 1:
        return state.my_score + added_score
    return state.rival_score + added_score


def can_I_move(board, pos):
    num_steps_available = 0
    for d in get_directions():
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


def calc_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def succ(board, close, cur_pos, depth):
    states = set()
    for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        new_pos = (cur_pos[0] + move[0], cur_pos[1], move[1])
        if board[new_pos[0]][new_pos[1]] in [1, 2, -1] or new_pos in close:
            continue
        states.add((new_pos, depth + 1))
    return states


def find_fruits(state):
    close, open = set(), collections.deque([(state.self_pos, 0)])
    close.add(state.self_pos)
    fruits = {}
    while open:
        cur = open.popleft()
        close.add(cur[0])
        if cur[1] == 6:
            continue
        for next in succ(state.board, close, cur[0], cur[1]):
            if state.board[next[0][0]][next[0][1]] > 2:
                fruits[next[0]] = next[1]
            open.append(next)
    return fruits


def heuristic_calc(state):
    best_pos = (0, 0)
    best_hueristic = -1
    closest_fruit_score = 0
    for pos, value in state.fruits.items():
        dist = calc_dist(state.self_pos, pos)
        if dist > 5:
            continue
        if best_hueristic == -1:
            best_pos = pos
            best_hueristic = value + 500 - 100 * dist
            continue
        if value + 500 - 100 * dist > best_hueristic:
            best_hueristic = value + 500 - 100 * dist
            best_pos = pos


def get_legal_moves(board, location):
    legal_moves = []
    for d in get_directions():
        i = location[0] + d[0]
        j = location[1] + d[1]

        # check legal move
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
            legal_moves.append((i, j))
    return legal_moves


def calc_direction(old_loc, new_loc):
    return (new_loc[0] - old_loc[0], new_loc[1] - old_loc[1])


class SearchAlgos:
    def __init__(self, utility, succ, perform_move, goal=None):
        """The constructor for all the search algos.m
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):
    def search(self, state: State, depth, maximizing_player):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if maximizing_player is True:  # my turn
            location = state.my_location
        else:
            location = state.rival_location
        if location is None:
            print(state.board)
        if can_I_move(state.board, location) is False or depth == 0:  # is goal state or at end of depth
            return (calc_score(state, location, 1), None)

        if maximizing_player is True:
            max_val = -1000000
            best_direction = None
            for child in get_legal_moves(state.board, location):
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    del fruits[child]
                # print('######################')
                # print(state.board)
                # print(state.my_location)
                tmp_board = state.board.copy()
                tmp_board[state.my_location[0]][state.my_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 1  # Update new location
                my_score = calc_score(state, child, 1)
                # print('######################')
                # print(tmp_board)
                new_state = State(tmp_board, state.fine_score, my_score, state.rival_score, fruits)
                # print(new_state.my_location)
                # print(can_I_move(state.board, new_state.my_location), depth, '++++++++++++++++++++++++++++++')
                (val, _) = self.search(new_state, depth - 1, False)
                if max_val < val:
                    best_direction = calc_direction(location, child)
                    max_val = val
            return (max_val, best_direction)
        else:
            min_val = 1000000
            best_direction = None
            for child in get_legal_moves(state.board, location):
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    del fruits[child]
                tmp_board = state.board.copy()
                # print(state.board)
                tmp_board[state.rival_location[0]][state.rival_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 2  # Update new location
                new_state = State(tmp_board, state.fine_score, state.my_score, state.rival_score, fruits)
                (val, _) = self.search(new_state, depth - 1, True)
                if val < min_val:
                    best_direction = calc_direction(location, child)
                    min_val = val
            return (min_val, best_direction)


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        raise NotImplementedError
