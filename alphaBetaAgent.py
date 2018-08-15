import numpy as np
import evaluation as eval
from abalone import Action, Marble, MarbleManager
import tk


def eval_fn(game_state, agent_index):
    score = 0
    if eval.lost_marbles(game_state, agent_index) != 0:
        score += eval.lost_marbles(game_state, agent_index) * 1000
    if len(game_state._marbles.get_owner(agent_index)) < 9:
        score -= 1000000
    if len(game_state._marbles.get_owner(agent_index * (-1))) < 9:
        score += 1000000
    dist_from_center = eval.dist_from_center(game_state, agent_index)
    if dist_from_center < 24:
        score += 400
    elif dist_from_center < 30:
        score += 300
    elif dist_from_center < 35:
        score += 200
    elif dist_from_center < 40:
        score += 100
    group_score = eval.own_marbles_grouping(game_state, agent_index)
    if group_score > 55:
        score += 320
    elif group_score > 50:
        score += 240
    elif group_score > 45:
        score += 180
    elif group_score > 40:
        score += 80
    score += eval.attacking_opponent(game_state, agent_index) * 10
    score -= eval.attacked_by_opponent(game_state, agent_index) * 10
    return score


def aggressive_eval_fn(game_state, agent_index):
    score = 0
    if eval.lost_marbles(game_state, agent_index) != 0:
        score += eval.lost_marbles(game_state, agent_index) * 1000
    if len(game_state._marbles.get_owner(agent_index)) < 9:
        score -= 1000000
    if len(game_state._marbles.get_owner(agent_index * (-1))) < 9:
        score += 1000000
    dist_from_center = eval.dist_from_center(game_state, agent_index)
    if dist_from_center < 24:
        score += 800
    elif dist_from_center < 30:
        score += 600
    elif dist_from_center < 35:
        score += 400
    elif dist_from_center < 40:
        score += 200
    group_score = eval.own_marbles_grouping(game_state, agent_index)
    if group_score > 55:
        score += 80
    elif group_score > 50:
        score += 60
    elif group_score > 45:
        score += 45
    elif group_score > 40:
        score += 20
    score += eval.attacking_opponent(game_state, agent_index) * 800
    score -= eval.attacked_by_opponent(game_state, agent_index) * 800
    return score


class AlphaBetaAgent():
    """
    Minimax agent with alpha-beta pruning
    """

    def __init__(self, depth, evaluation_function=aggressive_eval_fn):
        self.depth = depth
        self.evaluation_function = evaluation_function
        self.transposition_table = dict()

    def get_action(self, game_state, agent_index, board):
        """
        Returns the minimax action using self.evaluation_function
        """
        # self.evaluation_function = eval_fn if agent_index == 1 else aggressive_eval_fn

        def max_agent(game_state, agent_index, depth, alpha, beta):

            legal_moves = game_state.get_legal_actions(agent_index)
            if len(legal_moves) == 0:
                return Action.STOP
            # action_list = game_state.get_legal_actions(agent_index)  # todo change to legal moves
            action_list = legal_moves

            best_score = float("-inf")
            # Action.Stop is always acpeted
            best_action = Action.STOP
            for index, action in enumerate(action_list):
                # if depth == 0:
                # print (index)

                successor = game_state.generate_successor(agent_index, action)
                successor_state_string = successor.create_state_string(agent_index)
                if self.transposition_table.has_key(successor_state_string):
                    score = self.transposition_table[successor_state_string]
                else:
                    score = min_agent(successor, -agent_index, depth, alpha, beta)
                    self.transposition_table[successor_state_string] = score
                if score > best_score:
                    best_score = score
                    best_action = action
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    return best_score
            if depth:
                return best_score
            return best_action

        def min_agent(game_state, agent_index, depth, alpha, beta):
            legal_moves = game_state.get_legal_actions(agent_index)
            if len(legal_moves) == 0:
                return Action.STOP
            # action_list = game_state.get_legal_actions(agent_index)
            action_list = legal_moves

            best_score = float("inf")
            for action in action_list:
                successor = game_state.generate_successor(agent_index, action)
                successor_state_string = successor.create_state_string(agent_index)
                # finish the depth tree
                if depth == self.depth - 1:
                    score = self.evaluation_function(successor, -agent_index)
                    self.transposition_table[successor_state_string] = score
                # continue to the tree

                else:
                    if self.transposition_table.has_key(successor_state_string):
                        score = self.transposition_table[successor_state_string]
                    else:
                        score = max_agent(successor, -agent_index, depth + 1, alpha, beta)
                        self.transposition_table[successor_state_string] = score
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    return best_score
            return best_score

        game_state = self.marble_list_creator(game_state)
        a = max_agent(game_state, agent_index, 0, float("-inf"), float("inf"))
        if isinstance(board, tk.Game_Board):
            board.move(a[0], True)
            board.update_idletasks()
        else:
            board.move(a[0][0], a[0][1])
            board.next()
        return a[0]

    def marble_list_creator(self, state):
        marble_list = list()
        for marble in state._marbles:
            marble_list.append(Marble(marble['position'], marble['owner']))
        state._marbles = MarbleManager(marble_list)
        return state


