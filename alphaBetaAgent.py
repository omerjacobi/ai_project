import numpy as np
import Evaluation as eval

class Agent():
    """
    Minimax agent with alpha-beta pruning
    """
    DEPTH = 2
    
    def evaluation_function(self, game_state, agent_index):
        return (100 * eval.win_or_lose(game_state, agent_index)) + eval.lost_marbles(game_state, agent_index) + \
               eval.dist_from_center(game_state, agent_index) + eval.own_marbles_grouping(state, agent_index) - \
               eval.opposing_marbles_grouping(state, agent_index)
    
    def get_action(self, game_state, agent_index):
        """
        Returns the minimax action using self.evaluation_function
        """
        legal_moves = game_state.get_legal_actions(agent_index)
        if len(legal_moves) == 0:
            return Action.STOP
        scores = [self.alpha_beta_search(-agent_index, game_state.generate_successor(0, action), DEPTH, -np.inf, np.inf) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        return legal_moves[np.random.choice(best_indices)]

    def alpha_beta_search(self, agent_index, game_state, depth, alpha, beta):
        """
        Returns the minimax value of a state using alpha-beta search
        """
        legal_moves = game_state.get_legal_actions(agent_index)
        if len(legal_moves) == 0 or depth == 0:
            return self.evaluation_function(game_state, agent_index)
        if agent_index == 0:
            current = -np.inf
            for action in legal_moves:
                current = max(current, self.alpha_beta_search(-agent_index, game_state.generate_successor(agent_index, action), depth, alpha, beta))
                alpha = max(alpha, current)
                if beta <= alpha:
                    break
            return current
        elif agent_index == 1:
            current = np.inf
            for action in legal_moves:
                current = min(current, self.alpha_beta_search(-agent_index, game_state.generate_successor(agent_index, action), depth - 1, alpha, beta))
                beta = min(beta, current)
                if beta <= alpha:
                    break
            return current
        else:
            raise Exception("Illegal agent index")