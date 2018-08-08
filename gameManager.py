import abc
from collections import namedtuple
from enum import Enum

import numpy as np
import time
import config
import tk as abaloneTk
import Action



class Agent(object):
    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def evaluation_function(self, game_state):
        return 1


class RandomOpponentAgent(Agent):
    """
    TODO: fill this (get all valid actions and choose a random one)
    """

class Game(object):
    def __init__(self, agent, opponent_agent, display, sleep_between_actions=False):
        super(Game, self).__init__() # TODO: is it ok to call super game ? maybe change the name of class to gamemanager???
        self.sleep_between_actions = sleep_between_actions
        self.agent = agent
        self.display = display
        self.opponent_agent = opponent_agent
        self._state = None

    def run_batch(self, rounds, initial_state):
        results = []
        for i in range(0, rounds):
            results.append(self.run(initial_state))
        return results

    def run(self, initial_state):
        self._state = initial_state
        self.display.initialize(initial_state)
        tk = abaloneTk.Game()
        tk.start(config.Players.Black.positions, config.Players.White.positions)
        return self._game_loop()

    def _game_loop(self):
        while not self._state.is_final_state():
            if self.sleep_between_actions:
                time.sleep(1)
            # self.display.mainloop_iteration()
            action = self.agent.get_action(self._state)
            if action == Action.STOP:
                return
            self._state.apply_action(action,self.display)
            if self._state.is_final_state():
                return                                          # TODO: Think about what this should return
            opponent_action = self.opponent_agent.get_action(self._state)
            self._state.apply_opponent_action(opponent_action)
            # self.display.update_state(self._state, action, opponent_action)
        return self._state.score, self._state.max_tile          # TODO: Think about what this should return
