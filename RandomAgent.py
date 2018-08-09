import  random
from abalone import Action

class Agent():
    """
    random agent
    """

    def __init__(self, depth=None, evaluation_function=None):
        self.depth = depth
        self.evaluation_function = evaluation_function

    def get_action(self, game_state, agent_index):
        """
        Returns the random action
        """
        legal_moves = game_state.get_legal_actions(agent_index)
        if len(legal_moves) == 0:
            return Action.STOP
        index=random.randint(0,len(legal_moves)-1)
        return legal_moves[index]

