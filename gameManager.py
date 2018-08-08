import  abalone
import config
import tk as abaloneTk
import alphaBetaAgent
from gameState import GameState
class Agent(object):
    def __init__(self,type):
        agent = None
        if type == 'AlphaBetaAgent':
            agent = alphaBetaAgent.Agent()


class Game(object):
    def __init__(self, agent1_type, agent2_type, board_type):
        super(Game, self).__init__()
        self.agent1 = Agent(agent1_type)
        self.agent2 = Agent(agent2_type)
        self.board = self.board(board_type)
        self._state = None

    def board(self,type):
        if type == 'SummaryDisplay':
            self.board = abalone.Game_Board()
        elif type == 'GUI':
            self.board = abaloneTk.Game_Board()

    def run(self):
        self.board.start(config.Players.Black.positions, config.Players.White.positions)
        player_index  = 1
        while True:
            marbles = self.board.get_marbles()
            state = GameState(marbles)
            if player_index == 1:
                (group, direction) = self.agent1.get_action(state,player_index)
            else:
                (group, direction) = self.agent2.get_action(state,player_index)
            self.board.move(group,direction)
            if self.broad.get_looser():
                break
            player_index *= -1





