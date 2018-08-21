import random
from abalone import Action
from abalone import Marble
from abalone import MarbleManager
import tk


class RandomAgent():
    """
    random agent
    """

    def __init__(self, depth=None, evaluation_function=None):
        self.depth = depth
        self.evaluation_function = evaluation_function

    def get_action(self, state, player_index, board):
        """
        Returns the random action
        """
        legal_moves = state.get_legal_actions(player_index)
        if len(legal_moves) == 0:
            return Action.STOP
        index = random.randint(0, len(legal_moves) - 1)
        # if isinstance(board, tk.Game_Board):
        #     board.move(legal_moves[index][0], True)
        #     board.update_idletasks()
        # else:
        #TODO restore
        board.move(legal_moves[index][0][0], legal_moves[index][0][1])
        board.next()
        return legal_moves[index][0]
