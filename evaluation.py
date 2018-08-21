# import abalone
# import gameState
# import config


distances_from_center = {(5, 5): 0,                                                                     # Center position

                         (4, 4): 1, (5, 4): 1, (6, 5): 1, (6, 6): 1, (5, 6): 1, (4, 5): 1,              # 1-step radius positions (center's neighbors)

                         (3, 3): 2, (4, 3): 2, (5, 3): 2, (6, 4): 2, (7, 5): 2, (7, 6): 2, (7, 7): 2,   # 2-step radius positions
                         (6, 7): 2, (5, 7): 2, (4, 6): 2, (3, 5): 2, (3, 4): 2,

                         (2, 2): 3, (3, 2): 3, (4, 2): 3, (5, 2): 3, (6, 3): 3, (7, 4): 3, (8, 5): 3,   # 3-step radius positions
                         (8, 6): 3, (8, 7): 3, (8, 8): 3, (7, 8): 3, (6, 8): 3, (5, 8): 3, (4, 7): 3,
                         (3, 6): 3, (2, 5): 3, (2, 4): 3, (2, 3): 3,

                         (1, 1): 4, (2, 1): 4, (3, 1): 4, (4, 1): 4, (5, 1): 4, (6, 2): 4, (7, 3): 4,   # 4-step radius positions
                         (8, 4): 4, (9, 5): 4, (9, 6): 4, (9, 7): 4, (9, 8): 4, (9, 9): 4, (8, 9): 4,
                         (7, 9): 4, (6, 9): 4, (5, 9): 4, (4, 8): 4, (3, 7): 4, (2, 6): 4, (1, 5): 4,
                         (1, 4): 4, (1, 3): 4, (1, 2): 4}
BLACK = 1
WHITE = -1


def position_in_range(position):
    """
    Returns True iff position is in board, else false
    """
    return abs(position[0] - position[1]) < 5 and position[0] < 10 and position[0] > 0 and position[
                                                                                               1] < 10 and \
           position[1] > 0


def win_or_lose(state, agent_index):
    """
    Returns 1 if agent[agent_index] wins, -1 if loses and 0 if no winner yet
    """
    loser = state.get_looser()
    winner = -loser if loser else 0
    return winner * agent_index


def lost_marbles(state, agent_index):
    """
    Returns the difference between agent[agent_index]'s marbles, to it's opponents marbles
    """
    black_marbles = len(state._marbles.get_owner(BLACK)) * agent_index * BLACK
    white_marbles = len(state._marbles.get_owner(WHITE)) * agent_index * WHITE
    return black_marbles + white_marbles


def dist_from_center(state, agent_index):
    """
    Returns distance from board center
    """
    res = 0
    for marble in state._marbles.get_owner(agent_index):
        res += distances_from_center[tuple(marble['position'])]
    return res


def potential_neighbors(position):
    """
    Returns a list of potential neighbors at a given position
    """
    res = [[position[0] - 1, position[1] - 1],
           [position[0], position[1] - 1],
           [position[0] + 1, position[1]],
           [position[0] + 1, position[1] + 1],
           [position[0], position[1] + 1],
           [position[0] - 1, position[1]]]
    return filter(position_in_range, res)


def own_marbles_grouping(state, agent_index):
    """
    Returns the number of neighboring marbles, for each marble that belongs to agent[agent_index]
    """
    res = 0
    agent_marbles = state._marbles.get_owner(agent_index)
    agent_marbles_positions = map(lambda m: m['position'], agent_marbles)
    for marble in agent_marbles:
        for pos in potential_neighbors(marble['position']):
            if pos in agent_marbles_positions:
                res += 1
    return res


def opposing_marbles_grouping(state, agent_index):
    """
    Returns the number of neighboring marbles, for each marble that belongs to the opponent
    """
    return own_marbles_grouping(state, -agent_index)


def count_row_sequence(marbles_group_positions, start_pos, direction):
    """
    Returns the length of a row sequence of marbles, starting from start_pos
    The implementation depends on that the marble in start_pos is in marbles_group_positions
    """
    res = 1
    for i in range(1, 3):
        if [start_pos[0] + i * direction[0], start_pos[1] + i * direction[1]] in marbles_group_positions:
            res += 1
        else:
            break
    return res


def has_numerical_advantage(agent_marbles_positions, agent_pos, opponent_marbles_positions, opponent_pos, direction):
    """
    Returns True iff a there's a row sequence advantage of up to 3 marbles to agent over it's opponent in a certain row
    """
    return count_row_sequence(agent_marbles_positions, agent_pos, [-direction[0], -direction[1]]) > count_row_sequence(opponent_marbles_positions, opponent_pos, direction)


def has_free_zone_for_sumito(opponent_pos, direction, opponent_marbles_positions, agent_marbles_positions):
    """
    Returns True iff there is a valid space for a Sumito move ('pushing' opponent's marbles)
    """
    sumito_pos = [opponent_pos[0] + direction[0] * (count_row_sequence(opponent_marbles_positions, opponent_pos ,
                                                                       direction)),
                  opponent_pos[1] + direction[1] * (count_row_sequence(opponent_marbles_positions, opponent_pos ,
                                                                       direction))]
    return (not position_in_range(sumito_pos)) or (sumito_pos not in opponent_marbles_positions and sumito_pos not in agent_marbles_positions)


def attacking_opponent(state, agent_index):
    """
    Returns the number of attacking positions (Sumito positions) of the agent
    """
    res = 0
    agent_marbles = state._marbles.get_owner(agent_index)
    opponent_marbles = state._marbles.get_owner(-agent_index)
    agent_marbles_positions = map(lambda m: m['position'], agent_marbles)
    opponent_marbles_positions = map(lambda m: m['position'], opponent_marbles)
    for pos in agent_marbles_positions:
        if [pos[0], pos[1] + 1] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0], pos[1] + 1), (0,1)) \
                    and has_free_zone_for_sumito((pos[0], pos[1] + 1), (0,1), opponent_marbles_positions, agent_marbles_positions):
                res += 1
        if [pos[0], pos[1] - 1] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0], pos[1] - 1), (0,-1)) \
                    and has_free_zone_for_sumito((pos[0], pos[1] - 1), (0,-1), opponent_marbles_positions, agent_marbles_positions):
                res += 1
        if [pos[0] + 1, pos[1] + 1] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0] + 1, pos[1] + 1), (1,1)) \
                    and has_free_zone_for_sumito((pos[0] + 1, pos[1] + 1), (1,1), opponent_marbles_positions, agent_marbles_positions):
                res += 1
        if [pos[0] + 1, pos[1]] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0] + 1, pos[1]), (1,0)) \
                    and has_free_zone_for_sumito((pos[0] + 1, pos[1]), (1,0), opponent_marbles_positions, agent_marbles_positions):
                res += 1
        if [pos[0] - 1, pos[1] - 1] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0] - 1, pos[1] - 1), (-1,-1)) \
                    and has_free_zone_for_sumito((pos[0] - 1, pos[1] - 1), (-1,-1), opponent_marbles_positions, agent_marbles_positions):
                res += 1
        if [pos[0] - 1, pos[1]] in opponent_marbles_positions:
            if has_numerical_advantage(agent_marbles_positions, pos, opponent_marbles_positions, (pos[0] - 1, pos[1]), (-1,0)) \
                    and has_free_zone_for_sumito((pos[0] - 1, pos[1]), (-1,0), opponent_marbles_positions, agent_marbles_positions):
                res += 1
    return res


def attacked_by_opponent(state, agent_index):
    """
    Returns the number of attacking positions (Sumito positions) of the opponent
    """
    return attacking_opponent(state, -agent_index)


# new_black = [(2,2), (2,5), (4,2), (4,4), (5,4), (5,6), (6,4), (6,5), (6,6), (6,7), (7,4), (7,5), (7,6), (7,8)]
# new_white = [(2,4), (3,2), (3,3), (3,5), (4,3), (4,5), (4,6), (4,7), (5,2), (5,3), (5,5), (6,3), (8,6)]
#
# board = abalone.Game_Board()
# board.start(config.Players.Black.positions, config.Players.White.positions)
# board.start(new_black, new_white)
# initial = board.get_initial()
# marbles = board.get_marbles()
# state = gameState.GameState(marbles, initial)
# print(attacked_by_opponent(state, BLACK))