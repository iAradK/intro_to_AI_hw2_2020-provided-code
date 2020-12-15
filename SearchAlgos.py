"""Search Algos: MiniMax, AlphaBeta
"""
import collections

from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT

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
    return  state.rival_score + added_score


def can_I_move(board, location):
    can_move = False
    for i in [-1,1]:
        if board[location[0]+i][location[1]] not in [1,2,-1] or \
                board[location[0]][location[1]+i] not in [1,2,-1]:
            can_move = True
    return can_move


def perform_move(state, move):
    #TODO: given a state and a move, returns the new state after the move


def succ(board, close, cur_pos, depth):
    states = set()
    for move in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        new_pos = (cur_pos[0] + move[0], cur_pos[1], move[1])
        if board[new_pos[0]][new_pos[1]] in [1, 2, -1] or new_pos in close:
            continue
        states.add((new_pos, depth+1))
    return states

def find_fruits(state):
    close, open = set(), collections.deque([(state.self_pos,0)])
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
            best_hueristic = value + 500 - 100*dist
            continue
        if value + 500 - 100*dist > best_hueristic:
            best_hueristic = value + 500 - 100*dist
            best_pos = pos


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
        #TODO: erase the following line and implement this function.
        if can_I_move == False: #is goal state
            return calc_score()




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
        #TODO: erase the following line and implement this function.
        raise NotImplementedError
