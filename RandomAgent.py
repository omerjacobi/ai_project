import  random
from abalone import Action

class RandomAgent():
    """
    random agent
    """

    def __init__(self,depth=None,evaluation_function=None):
        self.depth = depth
        self.evaluation_function = evaluation_function

    def get_action(self,state, player_index,board):
        """
        Returns the random action
        """
        legal_moves = state.get_legal_actions(player_index)
        if len(legal_moves) == 0:
            return Action.STOP
        index=random.randint(0,len(legal_moves)-1)
        board.move(legal_moves[index][0], True)
        board.update_idletasks()
        board.update()
        return legal_moves[index][0]

