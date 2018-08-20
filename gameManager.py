import timeit

import abalone
import config
import tk as abaloneTk
import alphaBetaAgent
import gameState
import humanAgent
import randomAgent
import approximateQAgent

class Agent_repr(object):
    def __init__(self, type, depth, num_of_training, player_index):
        self.agent = None
        if type == 'AlphaBetaAgent':
            self.agent = alphaBetaAgent.AlphaBetaAgent(depth)
        if type == 'KeyboardAgent':
            self.agent = humanAgent.HumanAgent()
        if type == 'RandomAgent':
            self.agent = randomAgent.RandomAgent()
        if type == 'QLearningAgent':
            self.agent = approximateQAgent.QLearningReplayMemory(player_index=player_index, num_training=num_of_training)



class Game(object):
    def __init__(self, agent1_type, agent2_type, board_type,depth, num_of_training):
        super(Game, self).__init__()
        self.tkState = None
        self.player1 = Agent_repr(agent1_type, depth, num_of_training, 1)
        self.player2 = Agent_repr(agent2_type, depth, num_of_training, -1)
        self.board = self.create_board(board_type)
        self.depth = depth
        self._state = None
        """if 'humanPlayer'=0 no player is human 1,2 indicate which is human, 3 means both are human"""
        self.humanPlayers = int(agent1_type == 'KeyboardAgent') + int(agent2_type == 'KeyboardAgent') * 2

    def create_board(self, type):
        if type == 'SummaryDisplay':
            return abalone.Game_Board()
        elif type == 'GUI':
            return abaloneTk.Game_Board()
        return None

    def run(self):
        self.board.start(config.Players.Black.positions, config.Players.White.positions)
        initial = self.board.get_initial()
        player_index = 1
        if self.humanPlayers == 3:
            state = abaloneTk.Game_Board()
            state.start(config.Players.Black.positions, config.Players.White.positions)
            state.mainloop()
        else:
            if isinstance(self.board, abaloneTk.Game_Board):
                self.board.update_idletasks()
            self.board.changed = False
            turn_counter = 0
            while True:
                marbles = self.board.get_marbles()
                state = gameState.GameState(marbles, initial)
                self.board.changed = False
                if player_index == 1:
                    self.player1.agent.get_action(state, player_index, self.board)
                else:
                    start_time = timeit.default_timer()
                    self.player2.agent.get_action(state, player_index, self.board)

                    elapsed = timeit.default_timer() - start_time

                    # print(elapsed)
                if self.board.get_looser():
                    return self.board.get_looser(), turn_counter
                player_index *= -1
                turn_counter += 1
