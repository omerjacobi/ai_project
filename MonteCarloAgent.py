import random
import math
import hashlib
import logging
import argparse

"""
A quick Monte Carlo Tree Search implementation.  For more details on MCTS see See http://pubs.doc.ic.ac.uk/survey-mcts-methods/survey-mcts-methods.pdf
The State is just a game where you have NUM_TURNS and at turn i you can make
a choice from [-2,2,3,-3]*i and this to to an accumulated value.  The goal is for the accumulated value to be as close to 0 as possible.
The game is not very interesting but it allows one to study MCTS which is.  Some features 
of the example by design are that moves do not commute and early mistakes are more costly.  
In particular there are two models of best child that one can use 
"""

SCALAR = 1 / math.sqrt(2.0)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')

#
# class MonteCarloAgent():
#     """
#     Monte Carlo Agent
#     """
#
#     def __init__(self, depth, evaluation_function=eval_fn):
#         self.depth = depth
#         self.evaluation_function = evaluation_function
#         self.transposition_table = dict()
#
#     def get_action(self, game_state, agent_index, board):
#         """
#         Returns the minimax action using self.evaluation_function
#         """
#
#         def max_agnet(game_state, agent_index, depth, alpha, beta):
#
#             legal_moves = game_state.get_legal_actions(agent_index)
#             if len(legal_moves) == 0:
#                 return Action.STOP
#
#             action_list = legal_moves
#
#             best_score = float("-inf")
#             # Action.Stop is always acpeted
#             best_action = Action.STOP
#             for index, action in enumerate(action_list):
#                 # if depth == 0:
#                 # print (index)
#
#                 successor = game_state.generate_successor(agent_index, action)
#                 successor_state_string = successor.create_state_string(agent_index)
#                 if self.transposition_table.has_key(successor_state_string):
#                     score = self.transposition_table[successor_state_string]
#                 else:
#                     score = min_agent(successor, -agent_index, depth, alpha, beta)
#                 if score > best_score:
#                     best_score = score
#                     best_action = action
#                 alpha = max(alpha, best_score)
#                 if alpha >= beta:
#                     return best_score
#             if depth:
#                 return best_score
#             return best_action
#
#         def min_agent(game_state, agent_index, depth, alpha, beta):
#             legal_moves = game_state.get_legal_actions(agent_index)
#             if len(legal_moves) == 0:
#                 return Action.STOP
#             # action_list = game_state.get_legal_actions(agent_index)
#             action_list = legal_moves
#
#             best_score = float("inf")
#             for action in action_list:
#                 successor = game_state.generate_successor(agent_index, action)
#                 # finish the depth tree
#                 if depth == self.depth - 1:
#                     score = self.evaluation_function(successor, -agent_index)
#                     successor_state_string = successor.create_state_string(agent_index)
#                     self.transposition_table[successor_state_string] = score
#                 # continue to the tree
#
#                 else:
#                     # successor = game_state.generate_successor(agent_index, action)
#                     successor_state_string = successor.create_state_string(agent_index)
#
#                     if self.transposition_table.has_key(successor_state_string):
#                         score = self.transposition_table[successor_state_string]
#                     else:
#                         score = max_agnet(successor, -agent_index, depth + 1, alpha, beta)
#                 best_score = min(score, best_score)
#                 beta = min(beta, best_score)
#                 if alpha >= beta:
#                     return best_score
#             return best_score
#
#         game_state = self.marble_list_creator(game_state)
#         a = max_agnet(game_state, agent_index, 0, float("-inf"), float("inf"))
#         board.move(a[0], True)
#         board.update_idletasks()
#         return a[0]
#
#     def marble_list_creator(self, state):
#         marble_list = list()
#         for marble in state._marbles:
#             marble_list.append(Marble(marble['position'], marble['owner']))
#         state._marbles = MarbleManager(marble_list)
#         return state


class State():
    NUM_TURNS = 10
    GOAL = 0
    MOVES = [2, -2, 3, -3]
    MAX_VALUE = (5.0 * (NUM_TURNS - 1) * NUM_TURNS) / 2
    num_moves = len(MOVES)

    def __init__(self, value=0, moves=[], turn=NUM_TURNS):
        self.value = value
        self.turn = turn
        self.moves = moves

    def next_state(self):
        nextmove = random.choice([x * self.turn for x in self.MOVES])
        next = State(self.value + nextmove, self.moves + [nextmove], self.turn - 1)
        return next

    def terminal(self):
        if self.turn == 0:
            return True
        return False

    def reward(self):
        r = 1.0 - (abs(self.value - self.GOAL) / self.MAX_VALUE)
        return r

    def __hash__(self):
        return int(hashlib.md5(str(self.moves).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        s = "Value: %d; Moves: %s" % (self.value, self.moves)
        return s


class Node():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_expanded(self):
        if len(self.children) == self.state.num_moves:
            return True
        return False

    def __repr__(self):
        s = "Node; children: %d; visits: %d; reward: %f" % (len(self.children), self.visits, self.reward)
        return s


def UCTSEARCH(budget, root):
    for iter in range(int(budget)):
        if iter % 10000 == 9999:
            logger.info("simulation: %d" % iter)
            logger.info(root)
        front = TREEPOLICY(root)
        reward = DEFAULTPOLICY(front.state)
        BACKUP(front, reward)
    return BESTCHILD(root, 0)


def TREEPOLICY(node):
    # a hack to force 'exploitation' in a game where there are many options, and you may never/not want to fully expand first
    while node.state.terminal() == False:
        if len(node.children) == 0:
            return EXPAND(node)
        elif random.uniform(0, 1) < .5:
            node = BESTCHILD(node, SCALAR)
        else:
            if node.fully_expanded() == False:
                return EXPAND(node)
            else:
                node = BESTCHILD(node, SCALAR)
    return node


def EXPAND(node):
    tried_children = [c.state for c in node.children]
    new_state = node.state.next_state()
    while new_state in tried_children:
        new_state = node.state.next_state()
    node.add_child(new_state)
    return node.children[-1]


# current this uses the most vanilla MCTS formula it is worth experimenting with THRESHOLD ASCENT (TAGS)
def BESTCHILD(node, scalar):
    bestscore = 0.0
    bestchildren = []
    for c in node.children:
        exploit = c.reward / c.visits
        explore = math.sqrt(2.0 * math.log(node.visits) / float(c.visits))
        score = exploit + scalar * explore
        if score == bestscore:
            bestchildren.append(c)
        if score > bestscore:
            bestchildren = [c]
            bestscore = score
    if len(bestchildren) == 0:
        logger.warn("OOPS: no best child found, probably fatal")
    return random.choice(bestchildren)


def DEFAULTPOLICY(state):
    while state.terminal() == False:
        state = state.next_state()
    return state.reward()


def BACKUP(node, reward):
    while node != None:
        node.visits += 1
        node.reward += reward
        node = node.parent
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MCTS research code')
    parser.add_argument('--num_sims', action="store", required=True, type=int)
    parser.add_argument('--levels', action="store", required=True, type=int, choices=range(State.NUM_TURNS))
    args = parser.parse_args()

    current_node = Node(State())
    for l in range(args.levels):
        current_node = UCTSEARCH(args.num_sims / (l + 1), current_node)
        print("level %d" % l)
        print("Num Children: %d" % len(current_node.children))
        for i, c in enumerate(current_node.children):
            print(i, c)
        print("Best Child: %s" % current_node.state)

        print("--------------------------------")
