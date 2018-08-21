#!/usr/bin/env python


# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html
from abalone import Group, Logic, Action, Marble, MarbleManager

import numpy as np
import abalone
import alphaBetaAgent
import config
import evaluation as eval
import gameState
import tk as abaloneTk
import util
from agents import RLAgent
import featureExtractors as fe
import randomAgent
from replay_memory import ReplayMemory
import json

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data




class QLearningReplayMemory(RLAgent):
    """Implementation of Q-learing with replay memory, which updates model parameters
        towards a random sample of past experiences
    """
    def __init__(self, epsilon=0.2, gamma=0.993, stepSize=None,
        num_static_target_steps=750, memory_size=5000, replay_sample_size=4, player_index = 0,
                 num_training = 1):
        super(QLearningReplayMemory, self).__init__(fe.SimpleExtractor(), epsilon, gamma, stepSize)
        self.num_static_target_steps = num_static_target_steps
        self.memory_size = memory_size
        self.sample_size = replay_sample_size
        self.replay_memory = ReplayMemory(memory_size)
        self.static_target_weights = self.copyWeights()
        self.agent_index = player_index
        self.numTraining = num_training
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
            curr_index = 1
            counter = 0
            num_of_marbles_lost = 0
            num_of_marble_eaten = 0
            state = gameState.GameState(board.get_marbles(), initial)
            new_state = gameState.GameState(board.get_marbles(), initial)
            reward = 0
            total_num_eaten = 0
            total_num_lost = 0
            new_state = None
            while True:
                # if isinstance(board, abaloneTk.Game_Board):
                #     board.update_idletasks()
                #TODO restore
                counter += 1
                if self.agent_index == curr_index:
                    state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = len(state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = len(state._marbles.get_owner(-self.agent_index))
                    action = self.takeAction((state, curr_index, board))
                    new_state = gameState.GameState(board.get_marbles(), initial)
                    if board.get_looser():
                        new_state = gameState.GameState(board.get_marbles(), initial)
                        break
                else:
                    if new_state is None:
                        new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marble_eaten -= len(new_state._marbles.get_owner(-self.agent_index))
                    enemy.get_action(new_state, curr_index, board)
                    e_new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost -= len(e_new_state._marbles.get_owner(self.agent_index))
                    if board.get_looser():
                        break
                    if counter > 1:
                        if num_of_marble_eaten > 0:
                            total_num_eaten += 1
                        if num_of_marbles_lost > 0:
                            total_num_lost += 1
                        # reward = num_of_marbles_lost * -100 + num_of_marble_eaten * 100
                        reward = num_of_marble_eaten - num_of_marbles_lost

                        self.incorporateFeedback(state, action, reward, new_state, self.agent_index)

                curr_index *= -1
            if board.get_looser() == self.agent_index:
                self.incorporateFeedback(state, action, -1, new_state, curr_index)
            else:
                self.incorporateFeedback(state, action, +1, new_state, curr_index)
            print("Finished Training number: " + str(i + 1) + " after " + str(counter) + " plays")
            print("Number of marble lost: " + str(total_num_lost) + ", Number of marble enemy lost: " + str(
                total_num_eaten))

            print(
                "Training winner is: QLearner" if board.get_looser() != self.agent_index else "Training winner is: enemy")
        print("Finished training!!!!!!!")

    def reward_calc(self, curr_index, new_state, state):
        eaten_marble = len(state._marbles.get_owner(-curr_index)) - len(
            new_state._marbles.get_owner(-curr_index))
        reward = 1 + eaten_marble * 200
        if reward > 1:
            print ("eat marble in training")
        return reward

    def getStaticQ(self, state, action, player_index, features=None):
        """Get the Q-value for a state-action pair using
            a frozen set of auxiliary weights. This could be accomplished with a flag on
            getQ, but we want to make it extremely clear what's going on here
            :param player_index:
        """

        if not features:
            features = self.fe.getFeatures(state, action,player_index)
        score = 0
        for f, v in features.items():
            score += self.static_target_weights[f] * v
        return min(max(score,-1),1)


    def update_static_target(self):
        """update static target weights to current weights.
            This is done to make updates more stable
        """
        self.static_target_weights = self.copyWeights()

    def generate_string(self, state, player_index,action, reward, newState):
        action_list = json.dumps(action[0])
        state_list = state.create_state_string()
        new_state_list = newState.create_state_string()
        return state_list, player_index, action_list, reward, new_state_list


    def load_string(self, state, player_index,action, reward, newState):
        state = gameState.GameState(json_loads_byteified(state))
        action = json_loads_byteified(action)
        action = Action(action[0],action[1])
        newState = gameState.GameState(json_loads_byteified(newState))
        return state, player_index, action, reward, newState



    def incorporateFeedback(self, state, action, reward, newState, player_index):
        """Perform a Q-learning update
        :param player_index:
        """
        # TODO LEAVE TARGET AT REWARD IF END OF GAME
        if state == {}:
            return
        # update the auxiliary weights to the current weights every num_static_target_steps iterations
        if self.numIters % self.num_static_target_steps == 0:
            self.update_static_target()
        self.replay_memory.store(self.generate_string(state, player_index,action, reward, newState))

        for i in range(self.sample_size if self.replay_memory.isFull() else 1):
            state,player_index, action, reward, newState = self.replay_memory.sample()
            state, player_index, action, reward, newState = self.load_string(state, player_index,action, reward, newState)
            prediction = self.getQ(state, action, player_index)
            target = reward
            if not newState.get_looser():
                # Use the static auxiliary weights as your target
                target += self.discount * max(self.getStaticQ(newState, newAction, player_index) for newAction in self.actions(
                    newState, player_index))

            update = target - prediction
            # clip gradient - TODO EXPORT TO UTILS?
            # update = max(-2, update) if update < 0 else min(2, update)
            if update != 0:
                iter_dic = self.fe.getFeatures(state,action,player_index)
                dic_sum = iter_dic.totalCount()
                if dic_sum != 0: #TODO: check
                    for f, v in iter_dic.iteritems():
                        if v != 0:
                            self.weights[f] = self.weights[f] - (update / dic_sum)
        return None
