"""
File for breakout-playing agents

"""
import abc
from constants import *
from collections import defaultdict
import re
import math
import random
import util
import tensorflow as tf
import string
# from function_approximators import *
import random
from replay_memory import ReplayMemory
import copy
from eligibility_tracer import EligibilityTrace
import numpy as np
import tk as abaloneTk

GRADIENT = 5


class BaseAgent(object):
    """abstract base class for all agents
    """
    def takeAction(self, state):
        raise NotImplementedError("Override me")

    def incorporateFedback(self, state, action, reward, newState, player_index):
        raise NotImplementedError("override me")

    def reset(self):
        raise NotImplementedError("overide me")

    def actions(self, state, player_index):
        """returns set of possible actions from a state
        """
        legal_actions = state.get_legal_actions(player_index)
        return legal_actions


    def read_model(self, path):
        """reads model weights from file
            works kind of like an inverse of str()
        """
        model_str = open(path, 'r').read()
        model_str = re.sub("<type '", "", model_str)
        model_str = re.sub("'>", "", model_str)
        model_str = string.replace(model_str, ',)', ')')
        model_str = re.sub("<function <lambda>[^\,]*", "lambda: defaultdict(float)", model_str)
        newWeights = eval(model_str)
        return newWeights

    def write_model(self, path, model=None):
        """writes a model to file
        """
        file = open(path, 'w')
        file.write(str(model))
        file.close()





class RLAgent(BaseAgent):
    """base class for RL agents that approximate the value function.
    """
    def __init__(self, featureExtractor, epsilon=0.5, gamma=0.993, stepSize=None):
        self.fe = featureExtractor
        self.explorationProb = epsilon
        self.discount = gamma
        self.getStepSize = stepSize
        self.numIters = 1
        self.weights = defaultdict(float)


    def incorporateFeedback(self, state, action, reward, newState, player_index):
        raise NotImplementedError("override this")

    def getQ(self, state, action, player_index, features=None):
        """ returns Q-value for s,a pair
        :param player_index:
        """
        if not features:
            features = self.fe.getFeatures(state, action, player_index)
        score = 0
        for f, v in features.items():
            score += self.weights[f] * v
        return score

    def takeAction(self, game_state_tuple):
        """ returns action according to e-greedy policy
        """
        state, player_index, board = game_state_tuple
        self.numIters += 1
        actions = self.actions(state, player_index)
        if random.random() < self.explorationProb:
            action = random.choice(actions)
            if isinstance(board, abaloneTk.Game_Board):
                board.move(action[0], True)
                board.update_idletasks()
            else:
                board.move(action[0][0], action[0][1])
                board.next()
            return action
        scores = [(self.getQ(state, action, player_index), action) for action in actions]
        # break ties with random movement
        if util.allSame([x[0] for x in scores]):
            action = random.choice(scores)[1]
        else:
            action = max(scores)[1]
        if isinstance(board, abaloneTk.Game_Board):
            board.move(action[0], True)
            board.update_idletasks()
        else:
            board.move(action[0][0], action[0][1])
            board.next()
        return action

    def setStepSize(self, size):
        self.stepSize = size

    ####################################
    # step size functions
    # return a wee lil lambda function so that you can still initialize agents with this method:
    #     e.g. stepSize=agents.RLAgent.constant(0.001)
    # Because later getStepSize will be called with the number of iterations and we want
    #   to throw that away
    @staticmethod
    def constant(stepSize):
        """constant step size"""
        return lambda x: stepSize

    @staticmethod
    def inverse(numIters):
        """1/x"""
        return 1.0 / numIters

    @staticmethod
    def inverseSqrt(numIters):
        """1/sqrt(x)"""
        return 1.0 / math.sqrt(numIters)

    def copyWeights(self):
        return copy.deepcopy(self.weights)

    def write_model(self, path, model=None):
        super(RLAgent, self).write_model(path, self.weights)







