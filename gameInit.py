#!/usr/bin/env python

import argparse
import numpy
import gameManager
from gameState import GameState
import os
# from game import Game, RandomOpponentAgent
# from game_state import GameState
# from graphics_display import GabrieleCirulli2048GraphicsDisplay
# from keyboard_agent import KeyboardAgent
#
# NUM_OF_INITIAL_TILES = 2
#
#

import config


class GameRunner(object):
    def __init__(self, board=None, agent1=None, agent2=None,depth=None, num_of_training=None):
        super(GameRunner, self).__init__()
        self._agent1 = agent1
        self._agent2 = agent2
        self.board = board
        self.depth=depth
        self.current_game = None
        self.num_of_training = num_of_training
        self.game = None

    def new_game(self, *args, **kw):
        # self.quit_game()
        if not self.game:
            self.game = gameManager.Game(self._agent1, self._agent2, self.board, self.depth, self.num_of_training)
        self.current_game = self.game
        return self.game.run()

    def quit_game(self):
        if self.current_game is not None:
            self.current_game.quit()


# def create_agent(args):
#     if args.agent == 'ReflexAgent':
#         from multi_agents import ReflexAgent
#         agent = ReflexAgent()
#     else:
#         agent = util.lookup('multi_agents.' + args.agent, globals())(depth=args.depth,
#                                                                      evaluation_function=args.evaluation_function)
#     return agent


def main():
    parser = argparse.ArgumentParser(description='Abalone game.')
    displays = ['GUI', 'SummaryDisplay']
    agents = ['KeyboardAgent', 'MonteCarlo', 'AlphaBetaAgent', 'RandomAgent', 'QLearningAgent']
    parser.add_argument('--display', choices=displays, help='The game ui.', default=displays[0], type=str)
    parser.add_argument('--agent1', choices=agents, help='The agent.', default=agents[2], type=str)
    parser.add_argument('--agent2', choices=agents, help='The agent.', default=agents[2], type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=2,
                        type=int)
    parser.add_argument('--num_of_games', help='The number of games to run.', default=1, type=int)
    parser.add_argument('--num_of_training', help='The number of training to run.', default=10, type=int)
    parser.add_argument('--initial_board', help='Initial board for new games.', default=None, type=str)
    # TODO check if keyboard and SummaryDisplay
    args = parser.parse_args()
    if args.initial_board is not None:
        a = 1
        # TODO implement here diffrent start board
    board = args.display
    num_of_games = args.num_of_games
    # TODO implement diffrent boards kind (display/no display)
    game_runner = GameRunner(board=board, agent1=args.agent1, agent2=args.agent2,depth=args.depth, num_of_training=args.num_of_training)
    victories = [0,0]    # index 0 is for BLACK, index 1 is for white
    game_or_games = " game:" if num_of_games == 1 else " games:"
    print("\tRunning " + str(num_of_games) + game_or_games)
    for i in range(num_of_games):
        loser, turns = game_runner.new_game()
        winner_str = "Black" if loser == -1 else "White"
        print("Game #" + str(i + 1) + " ended after " + str(turns) + " turns. Winner: " + winner_str)
        if loser == -1:
            victories[0] += 1
        else:
            victories[1] += 1
    if num_of_games > 1:
        print("\t*** SUMMARY ***")
        print("Black player won " + str(victories[0]) + " games")
        print("White player won " + str(victories[1]) + " games")


if __name__ == '__main__':
    main()
    # input("Press Enter to continue...")
