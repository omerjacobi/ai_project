from gameManager import Agent, Action
import numpy as np

class AlphaBetaAgent(Agent):
    """
    Minimax agent with alpha-beta pruning
    TODO: fill this from top (this is an old implementation [not even final version] of 2048 exercise)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        legal_moves = game_state.get_agent_legal_actions()
        if len(legal_moves) == 0:
            return Action.STOP
        scores = [self.alpha_beta_search(1, game_state.generate_successor(0, action), self.depth - 1, AlphaBetaContainer()) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        return legal_moves[np.random.choice(best_indices)]

    def alpha_beta_search(self, agent_index, game_state, depth, alpha_beta):
        """
        Returns the minimax value of a state using alpha-beta search
        :param agent_index: 0 if Max agent, 1 if Min agent
        :param game_state: Current game state
        :param depth: Available depth in the state sub-tree
        :param alpha: alpha value
        :param beta: beta value
        :return: The MiniMax score for the given gameState
        """
        legal_moves = game_state.get_legal_actions(agent_index)
        if len(legal_moves) == 0 or depth == 0:
            return self.evaluation_function(game_state)
        if agent_index == 0:
            current = -np.inf
            for action in legal_moves:
                current = max(current, self.alpha_beta_search(1 - agent_index, game_state.generate_successor(agent_index, action), depth - 1, alpha_beta))
                alpha_beta.set_alpha(max(alpha_beta.alpha, current))
                if alpha_beta.cutoff_required():
                    break
            return current
        elif agent_index == 1:
            current = np.inf
            for action in legal_moves:
                current = min(current, self.alpha_beta_search(1 - agent_index, game_state.generate_successor(agent_index, action), depth - 1, alpha_beta))
                alpha_beta.set_beta(min(alpha_beta.beta, current))
                if alpha_beta.cutoff_required():
                    break
            return current
        else:
            raise Exception("Illegal agent index")
