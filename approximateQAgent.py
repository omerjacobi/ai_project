# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from learningAgents import ReinforcementAgent
from featureExtractors import *
import numpy as np
import abalone
import config
import randomAgent
import gameState
import tk
import evaluation as eval
import alphaBetaAgent

import random,util,math


def eval_fn(game_state, agent_index):
    score = 0
    if eval.lost_marbles(game_state, agent_index) != 0:
        score += eval.lost_marbles(game_state, agent_index) * 1000
    if len(game_state._marbles.get_owner(agent_index)) < 9:
        score -= 1000000
    if len(game_state._marbles.get_owner(agent_index * (-1))) < 9:
        score += 1000000
    dist_from_center = eval.dist_from_center(game_state, agent_index)
    if dist_from_center < 24:
        score += 400
    elif dist_from_center < 30:
        score += 300
    elif dist_from_center < 35:
        score += 200
    elif dist_from_center < 40:
        score += 100
    group_score = eval.own_marbles_grouping(game_state, agent_index)
    if group_score > 55:
        score += 320
    elif group_score > 50:
        score += 240
    elif group_score > 45:
        score += 180
    elif group_score > 40:
        score += 80
    score += eval.attacking_opponent(game_state, agent_index) * 10
    score -= eval.attacked_by_opponent(game_state, agent_index) * 10
    return score


class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, alpha=alpha, epsilon=epsilon, gamma=gamma, numTraining=numTraining)
    self.q_values = util.Counter()
    self.agent_index = 1
    self.training()

  def training(self):
      # enemy = randomAgent.RandomAgent()
      enemy = alphaBetaAgent.AlphaBetaAgent(depth=1)
      for i in range(self.numTraining):
          board = abalone.Game_Board()
          board.start(config.Players.Black.positions, config.Players.White.positions)
          initial = board.get_initial()
          self.startEpisode()
          while True:
            state = gameState.GameState(board.get_marbles(), initial)
            action = self.getAction(state, self.agent_index, board)
            new_state = gameState.GameState(board.get_marbles(), initial)
            if board.get_looser():
                break
            self.update(state, action, new_state, eval_fn(new_state, self.agent_index) - eval_fn(state, self.agent_index), self.agent_index)
            # Time for enemy move
            state = new_state
            enemy.get_action(state, -self.agent_index, board)
            if board.get_looser():
                new_state = gameState.GameState(board.get_marbles(), initial)
                break
          self.update(state, action, new_state, eval_fn(new_state, self.agent_index) - eval_fn(state, self.agent_index), self.agent_index)
          print("Finished Traing number: " + str(i+1))
      print("Finished training!!!!!!!")

  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """

    return self.q_values[self.generate_string(action, state)]

  def generate_string(self, action, state):
      action_list = list()
      group = action[0][0]
      for marble in group:
          action_list.append((marble['owner'], marble['position']))
      action_list = str(action_list)
      state_list = list()
      for marble in state._marbles:
          state_list.append((marble['owner'], marble['position']))
      state_list = str(state_list)
      return action_list, state_list

  def getMaxQValueActionPair(self, state, player_index):
      legal_actions = state.get_legal_actions(player_index)
      if len(legal_actions) == 0:
        return 0, None
      best_res = -np.inf
      best_action = None
      for action in legal_actions:
          q_val = self.getQValue(state, action)
          if q_val > best_res:
              best_res = q_val
              best_action = action
          elif q_val == best_res:
              rand_index = np.random.randint(2)
              best_action = best_action if rand_index == 1 else action
      return best_res, best_action

  def getValue(self, state, player_index):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    return self.getMaxQValueActionPair(state, player_index)[0]

  def getPolicy(self, state, player_index):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    return self.getMaxQValueActionPair(state, player_index)[1]


  def get_action(self, state, player_index, board):
      action = self.getPolicy(state, player_index)
      if isinstance(board, tk.Game_Board):
          board.move(action[0], True)
          board.update_idletasks()
      else:
          board.move(action[0][0], action[0][1])
          board.next()



  def getAction(self, state, player_index, board):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legal_actions = state.get_legal_actions(player_index)
    action = None
    if len(legal_actions) > 0:
      if util.flipCoin(self.epsilon):
        rand_index = np.random.randint(len(legal_actions))
        action = legal_actions[rand_index]
      else:
        action = self.getPolicy(state, player_index)
    if isinstance(board, tk.Game_Board):
        board.move(action[0], True)
        board.update_idletasks()
    else:
        board.move(action[0][0], action[0][1])
        board.next()
    return action


  def update(self, state, action, nextState, reward, player_index):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    string = self.generate_string(action, state)
    self.q_values[string] = ((1 - self.alpha) * self.q_values[string]) + \
                                    self.alpha * (reward + self.discount * self.getMaxQValueActionPair(nextState, player_index)[0])


class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    # You might want to initialize weights here.
    self.weight = util.Counter()
    "*** YOUR CODE HERE ***"

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    features = self.featExtractor.getFeatures(state,action)
    ret_value = 0
    for feature in features:
        ret_value += features[feature] * self.weight[feature]
    return ret_value


  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    "*** YOUR CODE HERE ***"
    features = self.featExtractor.getFeatures(state,action)
    precalc = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)
    for feature in features:
        self.weight[feature] += self.alpha * precalc * features[feature]


  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
      pass
