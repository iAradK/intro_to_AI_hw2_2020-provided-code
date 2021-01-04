"""Search Algos: MiniMax, AlphaBeta
"""
import collections

from utils import ALPHA_VALUE_INIT, BETA_VALUE_INIT, get_directions

from players.our_structurs import State


def preform_move(state: State, dest_location, IsMyTurn) -> State:
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

    if can_I_move(board, my_location) == False:
        my_score -= penalty
    if can_I_move(board, rival_loaction) == False:
        rival_score -= penalty
    new_state = State(board, penalty, my_score, rival_score, fruits, turn)
    return new_state


def calc_score(state, player_type):
    if not can_I_move(state.board, state.my_location):
        state.my_score -= state.fine_score
    if not can_I_move(state.board, state.rival_location):
        state.rival_score -= state.fine_score
    return state.my_score - state.rival_score


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


def find_fruits(state):
    close, open = set(), collections.deque([(state.my_location, 0)])
    close.add(state.my_location)
    fruits = {}
    while open:
        cur = open.popleft()
        close.add(cur[0])
        if cur[1] == min(len(state.board), len(state.board[0])) - state.turn:
            continue
        for next in succ(state.board, close, cur[0], cur[1]):
            if state.board[next[0][0]][next[0][1]] > 2:
                fruits[next[0]] = next[1]
            open.append(next)
    return fruits


def find_longest_route_aux(board, curr_pos, new_pos, depth):
    temp_board = board.copy()
    temp_board[curr_pos[0]][curr_pos[1]] = -1
    if depth == 5:
        return 0
    max = 0
    if not can_I_move(temp_board, new_pos):
        return 0
    for d in get_legal_moves(board, new_pos):
        temp = 1 + find_longest_route_aux(temp_board, new_pos, d, depth + 1)
        if temp > max:
            max = temp
    return max


def find_longest_route(state, isMe):
    max = 0
    if isMe == True:
        for d in get_legal_moves(state.board, state.my_location):
            temp = find_longest_route_aux(state.board, state.my_location, d, 0)
            if temp > max:
                max = temp
    else:
        for d in get_legal_moves(state.board, state.rival_location):
            temp = find_longest_route_aux(state.board, state.rival_location, d, 0)
            if temp > max:
                max = temp
    return max


def just_get_any_legal_location(state: State):
    loc = get_legal_moves(state.board, state.my_location)[0]
    return calc_direction(state.my_location, loc)

def calc_nearby_fruits(state, location):
    score = 0
    for key, value in state.fruits.items():
        if calc_dist(location, key) <= 3:
            score += value*0.1
    return score

def heuristic_calc(state):
    heuristic = 0
    fruits = find_fruits(state)
    # fruit_time = min(len(state.board), len(state.board[1])) - state.turn
    # for key, value in list(fruits.items()):
    #     if value > fruit_time:
    #         fruits.pop(key)
    #         continue
        # if calc_dist(state.my_location, key) > calc_dist(state.rival_location, key):  # TODO: check if > or >=
        #     fruits.pop(key)
    max_fruit = -100000000
    for key, value in fruits.items():
        real_value = state.fruits[key] - 0.1*value*(state.fruits[key]) + calc_nearby_fruits(state, key)
        if real_value > max_fruit:
            max_fruit = real_value
    # x = find_longest_route(state, True)
    if max_fruit == -100000000:
        heuristic += find_longest_route(state, True) * (state.fine_score / 1)
        heuristic -= find_longest_route(state, False) * (state.fine_score / 2)
        # print(x)
    else:
        if max_fruit == 0:
            max_fruit = 1
        heuristic += find_longest_route(state, True) * (state.fine_score / (max_fruit*3)) * 2
        heuristic -= find_longest_route(state, False) * (state.fine_score / (max_fruit*6)) * 1/2
        heuristic += real_value
    return heuristic

# returns the value of the closest fruit (manhattan distance)
def heuristic_calc_light(state):
    heuristic = 0
    fruits = find_fruits(state)
    fruit_time = min(len(state.board), len(state.board[1])) - state.turn
    min_dist = 10000
    score = 0
    for key, value in list(fruits.items()):
        if calc_dist(state.my_location, key) < min_dist:
            min_dist = calc_dist(state.my_location, key)
            score = state.fruits[key]
    return score


def heuristic1(state, isMe): # Uses manhattan distance for fruits
    heuristic = 0
    max_fruit = -100000000
    for key, value in state.fruits:
        if isMe is True:
            location = state.my_location
        else:
            location= state.rival_location
        real_value = state.fruits[key] - 0.1 * value * (calc_dist(key, location)) + calc_nearby_fruits(state, key)
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


def heuristic2(state, isMe):
    heuristic = 0
    max_fruit = -100000000
    fruit_new_vals = {}
    if isMe is True:
        location = state.my_location
    else:
        location = state.rival_location
    for key, value in state.fruits:
        real_value = state.fruits[key] - 0.1 * value * (calc_dist(key, location)) + calc_nearby_fruits(state, key)
        fruit_new_vals[key] = real_value

    fruit_val = 0
    for key, val in fruit_new_vals: # Calc value of location, not only the best fruit near by
        fruit_val += 0.5 * val * (calc_dist(key, location))

    if max_fruit == -100000000:
        heuristic += find_longest_route(state, True) * (state.fine_score / 1)
        heuristic -= find_longest_route(state, False) * (state.fine_score / 2)
        # print(x)
    else:
        if max_fruit == 0:
            max_fruit = 1
        heuristic += find_longest_route(state, True) * (state.fine_score / (max_fruit * 3)) * 2
        heuristic -= find_longest_route(state, False) * (state.fine_score / (max_fruit * 6)) * 1 / 2
        heuristic += fruit_val
    return heuristic


def heuristic3(state, isMe):
    fruits = find_fruits(state)
    fruit_time = min(len(state.board), len(state.board[1])) - state.turn
    min_dist = 10000
    score = 0
    if isMe is True:
        location = state.my_location
    else:
        location = state.rival_location

    for key, value in list(fruits.items()):
        dist = calc_dist(location, key)
        if dist < min_dist:
            min_dist = dist
            score = state.fruits[key]

    rival_dist = calc_dist(state.my_location, state.rival_location)

    if can_I_move(state.board, state.my_location):
        return score - state.fine_score
    return score + 0.2*rival_dist


def heuristic4(state, isMe):
    heuristic = 0
    max_fruit = -100000000
    fruit_new_vals = {}
    if isMe is True:
        location = state.my_location
    else:
        location = state.rival_location
    for key, value in state.fruits:
        real_value = state.fruits[key] - 0.1 * value * (calc_dist(key, location)) + calc_nearby_fruits(state, key)
        fruit_new_vals[key] = real_value

    fruit_val = 0
    for key, val in fruit_new_vals: # Calc value of location, not only the best fruit near by
        fruit_val += 0.5 * val * (calc_dist(key, location))

    rival_dist = calc_dist(state.my_location, state.rival_location)

    if can_I_move(state.board, state.my_location):
        return fruit_val - state.fine_score
    return fruit_val + 0.2*rival_dist


def get_legal_moves(board, location):
    legal_moves = []
    for d in get_directions():
        i = location[0] + d[0]
        j = location[1] + d[1]

        # check legal move
        if 0 <= i < len(board) and 0 <= j < len(board[0]) and (board[i][j] not in [-1, 1, 2]):
            legal_moves.append((i, j))
    return legal_moves


def remove_fruits_from_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 2:
                board[i][j] = 0


def calc_direction(old_loc, new_loc):
    return (new_loc[0] - old_loc[0], new_loc[1] - old_loc[1])


def can_I_win_with_fine(state: State, maximizing_player):
    if maximizing_player is True:
        return state.my_score - state.rival_score > state.fine_score

    return state.rival_score - state.my_score > state.fine_score


def get_heuristic_for_move(state, move, agent, heuristic_type):
    if heuristic_type == 0:
        return heuristic_calc(state)
    if heuristic_type == 1:
        return heuristic_calc_light(preform_move(state, move, agent))
    elif heuristic_type == 11:
        return heuristic_calc(preform_move(state, move, agent))
    elif heuristic_type == 22:
        return heuristic2(preform_move(state, move, agent), agent)
    elif heuristic_type == 33:
        return heuristic3(preform_move(state, move, agent), agent)
    elif heuristic_type == 44:
        return heuristic4(preform_move(state, move, agent), agent)

def sorted_moves(state, agent, heuristic_type):
    if agent is True:
        moves = get_legal_moves(state.board, state.my_location)
    else:
        moves = get_legal_moves(state.board, state.rival_location)
    #Change here?
    moves.sort(key=(lambda move: get_heuristic_for_move(state, move, agent, heuristic_type)))
    return moves


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

def choose_heuristic(state, heuristic_type, isMe):
    if heuristic_type == 0:
        return heuristic_calc(state)
    if heuristic_type == 1:
        return heuristic_calc_light(state)
    elif heuristic_type == 11:
        return heuristic1(state, isMe)
    elif heuristic_type == 22:
        return heuristic2(state, isMe)
    elif heuristic_type == 33:
        return heuristic3(state, isMe)
    elif heuristic_type == 44:
        return heuristic4(state, isMe)


class MiniMax(SearchAlgos):
    def search(self, state: State, depth, maximizing_player, heuristic_type=0):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param: heuristic_type: 0 is normal, 1 is light
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        # find_fruits(state)
        if maximizing_player is True:  # my turn
            location = state.my_location
        else:
            location = state.rival_location
        if location is None:
            print("WTF?!?!", state.board)
            #print
            exit()
        if can_I_move(state.board, location) is False \
                or can_I_win_with_fine(state, maximizing_player):  # is goal state or at end of depth
            if can_I_win_with_fine(state, maximizing_player):  # We want to make it worth to get the fine
                if maximizing_player is True:
                    state.my_score += 10000
                else:
                    state.rival_score += 10000
            return (calc_score(state, 1), None)
        if depth == 0:
            if heuristic_type == 1:
                return (heuristic_calc_light(state), None)
            return (choose_heuristic(state, heuristic_type, True), None)
            # return (heuristic_calc(state), None)
        fruit_vanish = min(len(state.board), len(state.board[0]))
        if state.turn == fruit_vanish:
            remove_fruits_from_board(state.board)
        if maximizing_player is True:
            max_val = -1000000
            best_direction = None
            sorted_moves(state, 0, heuristic_type)
            for child in get_legal_moves(state.board, location):
                score_to_add = 0
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    del fruits[child]
                    score_to_add += state.board[child[0]][child[1]]
                tmp_board = state.board.copy()
                tmp_board[state.my_location[0]][state.my_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 1  # Update new location
                new_state = State(tmp_board, state.fine_score, state.my_score + score_to_add, state.rival_score,
                                  fruits, state.turn + 1)
                (val, _) = self.search(new_state, depth - 1, False)
                if max_val < val:
                    best_direction = calc_direction(location, child)
                    max_val = val
            return (max_val, best_direction)
        else:
            min_val = 1000000
            best_direction = None
            for child in get_legal_moves(state.board, location):
                score_to_add = 0
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    score_to_add += state.board[child[0]][child[1]]
                    del fruits[child]
                tmp_board = state.board.copy()
                tmp_board[state.rival_location[0]][state.rival_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 2  # Update new location
                new_state = State(tmp_board, state.fine_score, state.my_score, state.rival_score + score_to_add,
                                  fruits, state.turn)
                (val, _) = self.search(new_state, depth - 1, True)
                if val < min_val:
                    best_direction = calc_direction(location, child)
                    min_val = val
            return (min_val, best_direction)


class AlphaBeta(SearchAlgos):
    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT, heuristic_type=0):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :param: heuristic_type: 0 is normal, 1 is light
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        if maximizing_player is True:  # my turn
            location = state.my_location
        else:
            location = state.rival_location
        if location is None:
            print("WTF?!?!", state.board)
            exit()
        if can_I_move(state.board, location) is False or depth == 0:
               # or can_I_win_with_fine(state, maximizing_player):  # is goal state or at end of depth TODO:
            # if can_I_win_with_fine(state, maximizing_player):  # We want to make it worth to get the fine
            #     if maximizing_player is True:
            #         state.my_score += 10000
            #     else:
            #         state.rival_score += 10000
            return (calc_score(state, 1), None)
        if depth == 0:
            if heuristic_type == 1:
                return (heuristic_calc_light(state), None)
            return (choose_heuristic(state, heuristic_type, True), None)
            # return (heuristic_calc(state), None)
        fruit_vanish = min(len(state.board), len(state.board[0]))
        if state.turn == fruit_vanish:
            remove_fruits_from_board(state.board)
        if maximizing_player is True:
            max_val = -1000000
            best_direction = None
            for child in sorted_moves(state, True, heuristic_type):
                score_to_add = 0
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    del fruits[child]
                    score_to_add += state.board[child[0]][child[1]]
                tmp_board = state.board.copy()
                tmp_board[state.my_location[0]][state.my_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 1  # Update new location
                new_state = State(tmp_board, state.fine_score, state.my_score + score_to_add, state.rival_score,
                                  fruits, state.turn + 1)
                (val, _) = self.search(new_state, depth - 1, False)
                if max_val < val:
                    best_direction = calc_direction(location, child)
                    max_val = val
            return (max_val, best_direction)
        else: 
            min_val = 1000000
            best_direction = None
            for child in sorted_moves(state, False, heuristic_type):
                score_to_add = 0
                fruits = state.fruits.copy()
                if state.board[child[0]][child[1]] > 2:  # if we are on a fruit
                    score_to_add += state.board[child[0]][child[1]]
                    del fruits[child]
                tmp_board = state.board.copy()
                tmp_board[state.rival_location[0]][state.rival_location[1]] = -1  # Update old location
                tmp_board[child[0]][child[1]] = 2  # Update new location
                new_state = State(tmp_board, state.fine_score, state.my_score, state.rival_score + score_to_add,
                                  fruits, state.turn)
                (val, _) = self.search(new_state, depth - 1, True)
                if val < min_val:
                    best_direction = calc_direction(location, child)
                    min_val = val
            return (min_val, best_direction)
