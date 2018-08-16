# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import numpy as np
import abalone
import alphaBetaAgent
import config
import evaluation as eval
import gameState
import tk
import util
from learningAgents import ReinforcementAgent
import featureExtractors
from copy import deepcopy


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

    def __init__(self, player_index=0, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining=10):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, alpha=alpha, epsilon=epsilon, gamma=gamma,
                                    numTraining=numTraining)
        self.q_values = util.Counter()
        self.agent_index = player_index
        self.training()

    def training(self):
        # enemy = randomAgent.RandomAgent()
        enemy = alphaBetaAgent.AlphaBetaAgent(depth=1)
        for i in range(self.numTraining):
            board = abalone.Game_Board()
            board.start(config.Players.Black.positions, config.Players.White.positions)
            initial = board.get_initial()
            self.startEpisode()
            curr_index = 1
            while True:
                marbles = deepcopy(board.get_marbles())
                state = gameState.GameState(marbles, initial)
                marbles2 = deepcopy(state._marbles)
                if self.agent_index == curr_index:
                    action = self.getAction(state, curr_index, board)
                    marbles3 = deepcopy(state._marbles)
                    marbles4 = deepcopy(board.get_marbles())
                    new_state = state.generate_successor(curr_index,action)
                    marbles5 = new_state._marbles
                    marbles6 = state._marbles
                    marbles7 = board.get_marbles()
                    reward = self.reward_calc(curr_index, new_state=new_state, state=state)
                    self.update(state, action, new_state, reward, self.agent_index)
                    if board.get_looser():
                        break
                else:
                    enemy.get_action(state, curr_index, board)
                    if board.get_looser():
                        break
                curr_index *= -1
            print("Finished Traing number: " + str(i + 1))
            print(
            "Training winner is: QLearner" if board.get_looser() != self.agent_index else "Training winner is: enemy")
        print("Finished training!!!!!!!")

    def reward_calc(self, curr_index, new_state, state):
        eaten_marble = len(state._marbles.get_owner(-curr_index)) - len(
            new_state._marbles.get_owner(-curr_index))
        lost_marble = len(state._marbles.get_owner(curr_index)) - len(new_state._marbles.get_owner(
            curr_index))
        reward = 1 + eaten_marble*100 + lost_marble*-100
        if len(new_state._marbles) != 28:
            print ("check")
        return reward

    def getQValue(self, state, action, player_index = 0):
        """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """

        return self.q_values[self.generate_string(action, state)]

    def generate_string(self, action, state):
        action_list = list()
        group, direction = action[0]

        for marble in group:
            action_list.append((marble['owner'], marble['position']))
        action_list = str(action_list) + str(direction)
        state_list = list()
        for marble in state._marbles:
            state_list.append((marble['owner'], marble['position']))
        state_list = state.create_state_string(self.agent_index)
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
                                self.alpha * (reward + self.discount *
                                              self.getMaxQValueActionPair(nextState, player_index)[
                                                  0])


class AbaloneAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, player_index=0, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=10):
        """
      These default parameters can be changed from the pacman.py command line.
      For example, to change the exploration rate, try:
          python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

      alpha    - learning rate
      epsilon  - exploration rate
      gamma    - discount factor
      numTraining - number of training episodes, i.e. no learning after these many episodes
      """
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, player_index=player_index, epsilon=epsilon,gamma=gamma,
                                alpha=alpha, numTraining=numTraining)




class ApproximateQAgent(AbaloneAgent):
    """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """

    def __init__(self, player_index=0, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining=10):
        self.featExtractor = featureExtractors.SimpleExtractor()
        self.weight = util.Counter()
        AbaloneAgent.__init__(self, player_index=player_index, epsilon=epsilon,gamma=gamma,
                                alpha=alpha, numTraining=numTraining)
        # You might want to initialize weights here.
        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action, player_index = 0):
        """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state,action,player_index)
        ret_value = 0
        for feature in features:
            ret_value += features[feature] * self.weight[feature]
        return ret_value

    def update(self, state, action, nextState, reward, player_index):
        """
       Should update your weights based on transition
    """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state,action,player_index)
        precalc = reward + self.discount * self.getValue(nextState,player_index) - self.getQValue(state, action)
        for feature in features:
            self.weight[feature] += self.alpha * precalc * features[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        AbaloneAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
