import  abalone
import config
import tk as abaloneTk
import alphaBetaAgent


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

