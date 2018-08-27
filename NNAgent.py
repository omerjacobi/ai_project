#!/usr/bin/env python


# qlearningAgents.py
# ------------------

import abalone
import random
import config
import gameState
import tk as abaloneTk
import util
from agents import BaseAgent
import featureExtractors as fe
import json
import tensorflow as tf




class NN(BaseAgent):
    """Implementation of Q-learing with replay memory, which updates model parameters
        towards a random sample of past experiences
    """
    def __init__(self, training_agent, train_agent_str='random', train_agent_hue='no_hue',
                 epsilon=0.5, gamma=0.990, stepSize=None, player_index=0, num_training=1, show_tk=False):
        self.train_agent_str=train_agent_str
        self.train_agent_hue = train_agent_hue
        self.train_agent = training_agent
        self.fe = fe.SimpleExtractor()
        self.verbose = False
        self.maxEpsilon = epsilon
        self.explorationProb = epsilon
        self.eps_dif = epsilon/num_training
        self.discount = gamma
        self.getStepSize = stepSize
        self.numIters = 1
        self.feature_len = 7
        self.input_placeholder, self.target_placeholder, self.loss, self.train_step, self.sess, \
        self.output, self.merged, self.log_writer = self.define_model(self.feature_len)
        self.agent_index = player_index
        self.numTraining = num_training
        self._show_tk = show_tk
        self.training()

    def training(self):
        enemy = self.train_agent
        """enable TK and disable abalone to see training in GUI"""
        if self._show_tk:
            board = abaloneTk.Game_Board()
        else:
            board = abalone.Game_Board()

        arr = list()

        for i in range(self.numTraining):
            board.start(config.Players.Black.positions, config.Players.White.positions)
            initial = board.get_initial()
            curr_index = 1
            counter = 0
            num_of_marbles_lost = 0
            num_of_marble_eaten = 0
            state = gameState.GameState(board.get_marbles(), initial)
            total_num_eaten = 0
            total_num_lost = 0
            new_state = None
            while True:
                counter += 1
                if self.agent_index == curr_index:
                    state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost = len(state._marbles.get_owner(self.agent_index))
                    num_of_marble_eaten = len(state._marbles.get_owner(-self.agent_index))
                    action = self.takeAction((state, curr_index, board))
                    new_state = gameState.GameState(board.get_marbles(), initial)
                    if board.get_looser() or counter > 3000:
                        new_state = gameState.GameState(board.get_marbles(), initial)
                        break
                else:
                    if new_state is None:
                        new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marble_eaten -= len(new_state._marbles.get_owner(-self.agent_index))
                    enemy.get_action(new_state, curr_index, board)
                    e_new_state = gameState.GameState(board.get_marbles(), initial)
                    num_of_marbles_lost -= len(e_new_state._marbles.get_owner(self.agent_index))
                    if board.get_looser() or counter > 3000:
                        break
                    if counter > 1:
                        if num_of_marble_eaten > 0:
                            total_num_eaten += 1
                        if num_of_marbles_lost > 0:
                            total_num_lost += 1
                        reward = num_of_marble_eaten - num_of_marbles_lost

                        self.incorporateFeedback(state, action, reward, new_state, self.agent_index)

                curr_index *= -1
            if board.get_looser() == self.agent_index:
                self.incorporateFeedback(state, action, -1, new_state, self.agent_index)
                arr.append('lost')
            elif board.get_looser() == -self.agent_index:
                self.incorporateFeedback(state, action, +1, new_state, self.agent_index)
                arr.append('win')
            else:
                self.incorporateFeedback(state, action, 0, new_state, self.agent_index)
                arr.append('draw')
            self.explorationProb -= self.eps_dif
            print("Finished Training number: " + str(i + 1) + " after " + str(counter) + " plays")
            print("Number of marble lost: " + str(total_num_lost) + ", Number of marble enemy lost: " + str( total_num_eaten))
            print("Training winner is: QLearner" if board.get_looser() != self.agent_index else "Training winner is: enemy")
        print("Finished training!!!!!!!")
        self.explorationProb = 0.001
        file = open(
            './train/' + self.train_agent_str + '_hue_' + self.train_agent_hue + '_num_of_trains_' + str(
                self.numTraining) + '_score.txt', 'w')
        file.write(str(arr))
        file.close()
        saver = tf.train.Saver()
        saver.save(self.sess, './train/'+self.train_agent_str+'_hue_'+ self.train_agent_hue +'_num_of_trains_'+ str(self.numTraining)+'_ts')
        if self._show_tk:
            board.stop()

    def get_action(self, state, player_index, board):
        self.takeAction((state, player_index, board))

    def takeAction(self, game_state_tuple):
        """ returns action according to e-greedy policy
        """
        state, player_index, board = game_state_tuple
        self.numIters += 1
        actions = self.actions(state, player_index)
        if random.random() < self.explorationProb:
            action = random.choice(actions)
            if self._show_tk:
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
        if self._show_tk:
            board.move(action[0], True)
            board.update_idletasks()
        else:
            board.move(action[0][0], action[0][1])
            board.next()
        return action


    def toFeatureVector(self, state, action, player_index):
        """converts state/action pair to 1xN matrix for learning
        :param player_index:
        """
        features = self.fe.getFeatures(state,action,player_index)
        return util.dictToNpMatrix(features)


    def incorporateFeedback(self, state, action, reward, newState, player_index):
        """perform NN Q-learning update
        """
        # no feedback at start of game
        if state == {}:
            return

        cur_features = self.toFeatureVector(state, action,player_index)
        target = reward
        if not newState.get_looser():
            # Use the static auxiliary weights as your target
            target += self.discount * max(
                [self.getQ(newState, action,player_index) for action in self.actions(newState,player_index)])

        if self.verbose:
            summary, _ = self.sess.run([self.merged, self.train_step],
                                       feed_dict={
                                           self.input_placeholder: cur_features,
                                           self.target_placeholder: [[target]],
                                       })
            self.log_writer.add_summary(
                summary, self.numIters)
        else:
            self.sess.run([self.train_step],
                          feed_dict={
                              self.input_placeholder: cur_features,
                              self.target_placeholder: [[target]],
                          })




    def getQ(self, state, action, player_index):
        """Network forward pass
        :param player_index:
        """
        features = self.toFeatureVector(state, action, player_index)

        # output is a 1x1 matrix
        output = self.sess.run(self.output,
            feed_dict={
                self.input_placeholder: features,
            })

        return output[0][0]

    def define_model(self, input_size):
        """Defines a Q-learning network
        """

        # input and output placeholders
        inputs = tf.placeholder(tf.float32, shape=[None, input_size], name="input")
        targets = tf.placeholder(tf.float32, shape=[None, 1], name="target")

        # layer 0
        w_0 = tf.Variable(tf.random_normal([input_size, 16]))
        b_0 = tf.Variable(tf.random_normal([16]))
        fc_0 = tf.add(tf.matmul(inputs, w_0), b_0)
        fc_0 = tf.sigmoid(fc_0)

        # layer 1
        w_1 = tf.Variable(tf.random_normal([16, 1]))
        b_1 = tf.Variable(tf.random_normal([1]))
        fc_1 = tf.add(tf.matmul(fc_0, w_1), b_1)
        fc_1 = tf.nn.sigmoid(fc_1)

        # training
        loss = tf.reduce_sum(tf.square(fc_1 - targets))
        # starter_learning_rate = 0.1
        # global_step = tf.Variable(0, trainable=False)
        # learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,
        #                                    10000, 0.96, staircase=True)
        # optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        # train_step = optimizer.minimize(loss)
        train_step = tf.train.AdamOptimizer(.001).minimize(loss)

        # get session, initialize stuff
        config = tf.ConfigProto(
            device_count={'GPU': 0}
        )
        sess = tf.Session(config=config)
        sess.run(tf.global_variables_initializer())

        # log stuff if verbose
        if self.verbose:
            self.variable_summaries(w_0, 'w_0')
            self.variable_summaries(b_0, 'b_0')
            self.variable_summaries(w_1, 'w_1')
            self.variable_summaries(b_1, 'b_1')
            self.variable_summaries(fc_1, 'output')
            self.variable_summaries(fc_1, 'loss')

            merged = tf.summary.merge_all()
            log_writer = tf.summary.FileWriter('./', sess.graph)
        else:
            merged, log_writer = None, None

        return inputs, targets, loss, train_step, sess, fc_1, merged, log_writer


    def variable_summaries(self, var, name):
        """produces mean/std/max/min logging summaries for a variable
        """
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            tf.summary.scalar('mean/' + name, mean)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_sum(tf.square(var - mean)))
            tf.summary.scalar('sttdev/' + name, stddev)
            tf.summary.scalar('max/' + name, tf.reduce_max(var))
            tf.summary.scalar('min/' + name, tf.reduce_min(var))

