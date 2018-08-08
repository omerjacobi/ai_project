distances_from_center = {(5,5): 0,
                         (4,4): 1, (5,4): 1, (6,5): 1, (6,6): 1, (5,6): 1, (4,5): 1,
                         (3,3): 2, (4,3): 2, (5,3): 2, (6,4): 2, (7,5): 2, (7,6): 2, (7,7): 2, (6,7): 2, (5,7): 2, (4,6): 2, (3,5): 2, (3,4): 2,
                         (2,2): 3, (3,2): 3, (4,2): 3, (5,2): 3, (6,3): 3, (7,4): 3, (8,5): 3, (8,6): 3, (8,7): 3, (8,8): 3, (7,8): 3, (6,8): 3, (5,8): 3, (4,7): 3, (3,6): 3, (2,5): 3, (2,4): 3, (2,3): 3,
                         (1,1): 4, (2,1): 4, (3,1): 4, (4,1): 4, (5,1): 4, (6,2): 4, (7,3): 4, (8,4): 4, (9,5): 4, (9,6): 4, (9,7): 4, (9,8): 4, (9,9): 4, (8,9): 4, (7,9): 4, (6,9): 4, (5,9): 4, (4,8): 4, (3,7): 4, (2,6): 4, (1,5): 4, (1,4): 4, (1,3): 4, (1,2): 4}
BLACK = 1
WHITE = -1


def position_in_range(position):
    """
    Returns True iff position is in board, else false
    """
    if position[0] > 9 or position[0] < 1 or position[1] > 9 or position[1] < 1:
        return False
    return abs(position[0] - position[1]) <= 4


def win_or_lose(state, agent_index):
    """
    Returns 1 if agent[agent_index] wins, -1 if loses and 0 if no winner yet
    """
    loser = state.get_looser()
    loser = loser if loser else 0
    return loser * agent_index * (-1)


def lost_marbles(state, agent_index):
    """
    Returns the difference between agent[agent_index]'s lost marbles, to it's opponents lost marbles
    """
    black_marbles = len(state.game.marbles.get_owner(agent_index)) * agent_index * BLACK
    white_marbles = len(state.game.marbles.get_owner(agent_index)) * agent_index * WHITE
    return black_marbles + white_marbles


def dist_from_center(state, agent_index):
    """
    Returns distance from board center, which is in position (5,5)
    """
    res = 0
    for marble in state.game.marbles.get_owner(agent_index):
        res += distances_from_center[marble.position]
    return res


def potential_neighbors(position):
    """
    Returns a list of potential neighbors at a given position
    """
    res = [(position[0] - 1, position[1] - 1),
           (position[0], position[1] - 1),
           (position[0] + 1, position[1]),
           (position[0] + 1, position[1] + 1),
           (position[0], position[1] + 1),
           (position[0] - 1, position[1])]
    return filter(position_in_range, res)


def own_marbles_grouping(state, agent_index):
    """
    Returns the number of neighboring marbles, for each marble that belongs to agent[agent_index]
    """
    res = 0
    agent_marbles = state.game.marbles.get_owner(agent_index)
    for marble in agent_marbles:
        for pos in potential_neighbors(marble.position):
            if pos in agent_marbles:
                res += 1
    return res


def opposing_marbles_grouping(state, agent_index):
    return own_marbles_grouping(state, -agent_index)