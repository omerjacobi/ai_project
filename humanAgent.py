import time


#
# def eval_fn(game_state, agent_index):
#     return 5 * eval.lost_marbles(game_state, agent_index) + eval.dist_from_center(game_state, agent_index)


class HumanAgent():
    """
    Minimax agent with alpha-beta pruning
    """

    def __init__(self, depth=None, evaluation_function=None):
        self.depth = depth
        self.evaluation_function = evaluation_function

    def get_action(self, game_state, agent_index, tk):
        """
        Returns the minimax action using self.evaluation_function
        """
        while not tk.changed:
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        # game_state.apply_action(tk.lastMove, agent_index)
        return tk.lastMove[0]
