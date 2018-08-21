# dql gym Pong-v0
# optimize numpy to tf

import gym
import numpy as np
import tensorflow as tf
import sys
import os
import random as random
from collections import deque

env = gym.make('Pong-v0')
CHECK_POINT_DIR = './tensorboard/pong'
tf.set_random_seed(10)
np.random.seed(10)
random.seed(10)

input_size = 80 * 80 * 4
action_space = env.action_space.n
bsize = 32
hl_size = 256
D = deque([], 500*1000)
M = 100000
eps = 1.
gamma = 0.99
aver_reward = None

model = {}
model['W_conv1'] = tf.get_variable("W_conv1", shape=[8, 8, 4, 32], initializer=tf.contrib.layers.xavier_initializer())
model['b_conv1'] = tf.Variable(tf.zeros([32]), name="b_conv1")
model['W_conv2'] = tf.get_variable("W_conv2", shape=[4, 4, 32, 64], initializer=tf.contrib.layers.xavier_initializer())
model['b_conv2'] = tf.Variable(tf.zeros([64]), name="b_conv2")
model['W_conv3'] = tf.get_variable("W_conv3", shape=[3, 3, 64, 64], initializer=tf.contrib.layers.xavier_initializer())
model['b_conv3'] = tf.Variable(tf.zeros([64]), name="b_conv3")
model['W_fc1'] = tf.get_variable("W_fc1", shape=[10 * 10 * 64, hl_size], initializer=tf.contrib.layers.xavier_initializer())
model['b_fc1'] = tf.Variable(tf.zeros([hl_size]), name='b_fc1')
model['W_fc2'] = tf.get_variable("W_fc2", shape=[hl_size, action_space], initializer=tf.contrib.layers.xavier_initializer())
model['b_fc2'] = tf.Variable(tf.zeros([action_space]), name='b_fc2')

X = tf.placeholder(tf.float32, [None, input_size], name="input_x")
x_image = tf.reshape(X, [-1, 80, 80, 4])
h_conv1 = tf.nn.relu(tf.nn.conv2d(x_image, model['W_conv1'], strides=[1, 4, 4, 1], padding='SAME') + model['b_conv1'])
h_conv2 = tf.nn.relu(tf.nn.conv2d(h_conv1, model['W_conv2'], strides=[1, 2, 2, 1], padding='SAME') + model['b_conv2'])
h_conv3 = tf.nn.relu(tf.nn.conv2d(h_conv2, model['W_conv3'], strides=[1, 1, 1, 1], padding='SAME') + model['b_conv3'])
h_conv3_flat = tf.reshape(h_conv3, [-1, 10 * 10 * 64], name="h_pool3_flat")
h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, model['W_fc1']) + model['b_fc1'])
action_pred = tf.matmul(h_fc1, model['W_fc2']) + model['b_fc2']

best_values_op = tf.reduce_max(action_pred, reduction_indices=[1])

correct_pl = tf.placeholder(tf.float32, [None, action_space], name="labels")
loss = tf.reduce_mean(tf.square(action_pred - correct_pl))
optimizer = tf.train.AdamOptimizer(learning_rate=1e-3)
train_op = optimizer.minimize(loss)

def prepro(I):
    I = I[35:195]
    I = I[::2, ::2, 0]
    I[I == 144] = 0
    I[I == 109] = 0
    I[I != 0] = 1
    return I.astype(np.float).ravel()

def get_action(x):
    x = [x]
    action_values = sess.run(action_pred, feed_dict={X: x})
    action_values = np.squeeze(action_values)
    action = np.argmax(action_values)
    return action

def max_val_Q(xs2):
    best_values = sess.run(best_values_op, feed_dict={X: xs2})
    return best_values

def val_Q(xs):
    action_values = sess.run(action_pred, feed_dict={X: xs})
    return action_values

def get_batch():
    batch = random.sample(list(D), bsize)
    D_array = np.array(batch)

    states1 = np.array([data[0] for data in D_array])
    actions = np.array([data[1] for data in D_array])
    rewards = np.array([data[2] for data in D_array])
    states2 = np.array([data[3] for data in D_array])
    dones = np.array([data[4] for data in D_array])

    return states1, actions, rewards, states2, dones

def train(xs, correct):
    sess.run(train_op, feed_dict={X:xs, correct_pl: correct})

sess = tf.Session()
sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
checkpoint = tf.train.get_checkpoint_state(CHECK_POINT_DIR)
if checkpoint and checkpoint.model_checkpoint_path:
    try:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    except:
        print("Error on loading old network weights")
else:
    print("Could not find old network weights")

for episode in xrange(1, M+1):
    observation = env.reset()
    observation = prepro(observation)
    s_t = np.array([observation, observation, observation, observation])
    x = np.reshape(s_t, [input_size])
    cur_reward = 0

    while True:
        if np.random.random() < eps:
            action = np.random.randint(6)
        else:
            action = get_action(x)

        observation2, reward, done, info = env.step(action)
        cur_reward += reward

        observation2 = prepro(observation2)
        s_t2 = np.array([observation2, s_t[0], s_t[1], s_t[2]])
        x2 = np.reshape(s_t2, [input_size])

        D.append([x, action, reward, x2, done])
        x = x2

        if len(D) > bsize:
            xs, actions, rewards, xs2, dones = get_batch()

            second_term = gamma * max_val_Q(xs2)
            second_term[dones] = 0
            ys_label = rewards + second_term

            correct = val_Q(xs)
            correct[range(bsize), actions] = ys_label

            train(xs, correct)

        if done:
            eps = min(eps, 1. / (1 + episode / 5.))
            aver_reward = (aver_reward * 0.9 + cur_reward * 0.1) if aver_reward != None else cur_reward
            print('episode %d, cur_reward %.2f, aver_reward %.2f' % (episode, cur_reward, aver_reward))
            if episode % 10 == 0:
                print("Saving network...")
                if not os.path.exists(CHECK_POINT_DIR):
                    os.makedirs(CHECK_POINT_DIR)
                saver.save(sess, CHECK_POINT_DIR + "/pong", global_step=episode)
            break