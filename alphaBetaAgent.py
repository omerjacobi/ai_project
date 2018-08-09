import numpy as np
import Evaluation as eval
from abalone import Action


def eval_fn(game_state, agent_index):
    return 5 * eval.lost_marbles(game_state, agent_index) + eval.dist_from_center(game_state, agent_index)

class AlphaBetaAgent():
    """
    Minimax agent with alpha-beta pruning
    """
    def __init__(self, depth, evaluation_function=eval_fn,tk=None):
        self.depth = depth
        self.evaluation_function = evaluation_function

    def get_action(self, game_state, agent_index, tk):
        """
        Returns the minimax action using self.evaluation_function
        """

        def max_agnet(game_state, agent_index, depth, alpha, beta):
            legal_moves = game_state.get_legal_actions(agent_index)
            if len(legal_moves) == 0:
                return Action.STOP
            action_list = game_state.get_legal_actions(agent_index)
            best_score = float("-inf")
            # Action.Stop is always acpeted
            best_action = Action.STOP
            for index, action in enumerate(action_list):
                if depth == 0:
                    print (index)
                successor = game_state.generate_successor(agent_index, action)
                score = min_agent(successor, -agent_index, depth, alpha, beta)
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
            action_list = game_state.get_legal_actions(agent_index)
            best_score = float("inf")
            for action in action_list:
                successor = game_state.generate_successor(agent_index, action)
                # finish the depth tree
                if depth == self.depth - 1:
                    score = self.evaluation_function(successor, agent_index)
                # continou to the tree
                else:
                    score = max_agnet(successor, -agent_index, depth + 1, alpha, beta)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    return best_score
            return best_score
        a = max_agnet(game_state, index,0, float("-inf"), float("inf"))
        return a[0]
    # def get_action(self, game_state, agent_index):
    #     """
    #     Returns the minimax action using self.evaluation_function
    #     """
    #     legal_moves = game_state.get_legal_actions(agent_index)
    #     if len(legal_moves) == 0:
    #         return Action.STOP
    #     scores = [self.alpha_beta_search(agent_index, game_state.generate_successor(agent_index, action), self.depth,
    #                                      -np.inf, np.inf, agent_index) for action in legal_moves]
    #     best_score = max(scores)
    #     best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
    #     return legal_moves[np.random.choice(best_indices)]
    #
    #
    # def alpha_beta_search(self, curr_agent_index, game_state, depth, alpha, beta, max_player_index):
    #     """
    #     Returns the minimax value of a state using alpha-beta search
    #     :param max_player_index:
    #     """
    #     if depth == 0:
    #         return self.evaluation_function(game_state, curr_agent_index)
    #     legal_moves = game_state.get_legal_actions(curr_agent_index)
    #     if len(legal_moves) == 0:
    #         return self.evaluation_function(game_state, curr_agent_index)
    #     if curr_agent_index == max_player_index:
    #         current = -np.inf
    #         for action in legal_moves:
    #             current = max(current, self.alpha_beta_search(-curr_agent_index,
    #                                                           game_state.generate_successor(curr_agent_index, action),
    #                                                           depth, alpha, beta, max_player_index))
    #             alpha = max(alpha, current)
    #             if beta <= alpha:
    #                 break
    #         return current
    #     elif curr_agent_index == -max_player_index:
    #         current = np.inf
    #         for action in legal_moves:
    #             current = min(current, self.alpha_beta_search(-curr_agent_index,
    #                                                           game_state.generate_successor(curr_agent_index, action),
    #                                                           depth - 1, alpha, beta, max_player_index))
    #             beta = min(beta, current)
    #             if beta <= alpha:
    #                 break
    #         return current
    #     else:
    #         raise Exception("Illegal agent index")