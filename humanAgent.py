import time



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
            tk.update()
            tk.update_idletasks()
            time.sleep(0.01)
        # game_state.apply_action(tk.lastMove, agent_index)
        return tk.lastMove[0]
