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
import tk as abaloneTk
import util
from agents import QLearningReplayMemory
import featureExtractors
import randomAgent




class QLearningAgent(QLearningReplayMemory):
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

    def __init__(self, featureExtractor, epsilon=0.5, gamma=0.993, stepSize=None,
        num_static_target_steps=750, memory_size=2500, replay_sample_size=4):
        super(QLearningReplayMemory, self).__init__(featureExtractor, epsilon, gamma, stepSize)
        self.num_static_target_steps = num_static_target_steps
        self.memory_size = memory_size
        self.sample_size = replay_sample_size
        self.replay_memory = ReplayMemory(memory_size)
        self.static_target_weights = self.copyWeights()
        self.q_values = util.Counter()
        self.agent_index = player_index
        self.training()

    def training(self):
        enemy = randomAgent.RandomAgent()
        # enemy = alphaBetaAgent.AlphaBetaAgent(depth=1)
        """enable TK and disable abalone to see training in GUI"""
        board = abalone.Game_Board()
        # board = abaloneTk.Game_Board()

        for i in range(self.numTraining):
            board.start(config.Players.Black.positions, config.Players.White.positions)
            initial = board.get_initial()
            self.startEpisode()
            curr_index = 1
            counter = 0
            num_of_marbles_lost = 0
            num_of_marble_eaten = 0
            state = gameState.GameState(board.get_marbles(), initial)
            new_state = gameState.GameState(board.get_marbles(), initial)
            reward = 0
            total_num_eaten = 0
            total_num_lost = 0
            while True:
                if isinstance(board, abaloneTk.Game_Board):
                    board.update_idletasks()
                counter += 1
                """
                if self.agent_index == curr_index:
                    state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = len(state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = len(state._marbles.get_owner(-self.agent_index))
                    action = self.getAction(state, curr_index, board)
                    new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = num_of_marbles_lost - len(new_state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = num_of_marble_eaten - len(new_state._marbles.get_owner(-self.agent_index))
                    reward = num_of_marble_eaten - num_of_marbles_lost + 100 * eval.win_or_lose(new_state, self.agent_index)
                    self.update(state, action, new_state, reward, self.agent_index)
                    if board.get_looser():
                        # new_state = gameState.GameState(board.get_marbles(), initial)
                        break
                    if counter > 1:
                        if num_of_marble_eaten > 0:
                            total_num_eaten += 1
                        if num_of_marbles_lost > 0:
                            total_num_lost +=1
                else:
                    e_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = len(e_state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = len(e_state._marbles.get_owner(-self.agent_index))
                    enemy.get_action(e_state, curr_index, board)
                    new_e_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = num_of_marbles_lost - len(new_e_state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = num_of_marble_eaten - len(new_e_state._marbles.get_owner(-self.agent_index))
                    reward = num_of_marble_eaten - num_of_marbles_lost + 100 * eval.win_or_lose(new_e_state, self.agent_index)
                    self.update(state, action, new_state, reward, self.agent_index)
                    if board.get_looser():
                        break
                    if counter > 1:
                        if num_of_marble_eaten > 0:
                            total_num_eaten += 1
                        if num_of_marbles_lost > 0:
                            total_num_lost +=1
                        # reward = num_of_marbles_lost * -100 + num_of_marble_eaten * 100
                        # reward = num_of_marble_eaten - num_of_marbles_lost + eval.win_or_lose(new_state, self.agent_index)

                        # self.update(state, action, new_state, reward, self.agent_index)

                """
                if self.agent_index == curr_index:
                    state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = len(state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = len(state._marbles.get_owner(-self.agent_index))
                    action = self.getAction(state, curr_index, board)
                    if board.get_looser():
                        new_state = gameState.GameState(board.get_marbles(), initial)
                        break
                else:
                    e_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marble_eaten -= len(e_state._marbles.get_owner(-self.agent_index))
                    enemy.get_action(e_state, curr_index, board)
                    new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost -= len(new_state._marbles.get_owner(self.agent_index))
                    if board.get_looser():
                        break
                    if counter > 1:
                        if num_of_marble_eaten > 0:
                            total_num_eaten += 1
                        if num_of_marbles_lost > 0:
                            total_num_lost +=1
                        # reward = num_of_marbles_lost * -100 + num_of_marble_eaten * 100
                        reward = num_of_marble_eaten - num_of_marbles_lost

                        self.update(state, action, new_state, reward, self.agent_index)


                curr_index *= -1
            # if board.get_looser() == self.agent_index:
            #     self.update(state, action, new_state, -1, self.agent_index)
            # else:
            #     self.update(state, action, new_state, +1, self.agent_index)
            print("Finished Training number: " + str(i + 1) + " after " + str(counter) + " plays")
            print("Number of marble lost: " + str(total_num_lost) + ", Number of marble enemy lost: " + str(
                total_num_eaten))

            print(
            "Training winner is: QLearner" if board.get_looser() != self.agent_index else "Training winner is: enemy")
        print("Finished training!!!!!!!")

    def reward_calc(self, curr_index, new_state, state):
        eaten_marble = len(state._marbles.get_owner(-curr_index)) - len(
            new_state._marbles.get_owner(-curr_index))
        reward = 1 + eaten_marble*200
        if reward > 1:
            print ("eat marble in training")
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
        if isinstance(board, abaloneTk.Game_Board):
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
        if isinstance(board, abaloneTk.Game_Board):
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

    def getQValue(self, state, action, player_index = 0):
        """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
        """
        features = self.featExtractor.getFeatures(state,action,player_index)
        ret_value = 0
        for feature in features:
            ret_value += features[feature] * self.weight[feature]
        return ret_value

    def update(self, state, action, nextState, reward, player_index):
        """
       Should update your weights based on transition
        """
        features = self.featExtractor.getFeatures(state,action,player_index)
        precalc = reward + self.discount * self.getValue(nextState,player_index) - self.getQValue(state, action)
        for feature in features:
            self.weight[feature] += self.alpha * precalc * features[feature]
        # string = self.generate_string(action, state)
        # self.q_values[string] = precalc

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        AbaloneAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            pass
