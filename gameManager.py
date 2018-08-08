import  abalone
import config
import tk as abaloneTk
import alphaBetaAgent
from gameState import GameState
class Agent_repr(object):
    def __init__(self,type):
        self.agent = None
        if type == 'AlphaBetaAgent':
            self.agent = alphaBetaAgent.Agent(2)



class Game(object):
    def __init__(self, agent1_type, agent2_type, board_type):
        super(Game, self).__init__()
        self.player1 = Agent_repr(agent1_type)
        self.player2 = Agent_repr(agent2_type)
        self.board = self.create_board(board_type)
        self._state = None

    def create_board(self,type):
        if type == 'SummaryDisplay':
            return abalone.Game_Board()
        elif type == 'GUI':
            return abaloneTk.Game_Board()
        return None

    def run(self):
        self.board.start(config.Players.Black.positions, config.Players.White.positions)
        player_index  = 1
        while True:
            marbles = self.board.get_marbles()
            state = GameState(marbles)
            if player_index == 1:
                (group, direction) = self.player1.agent.get_action(state, player_index)
            else:
                (group, direction) = self.player2.agent.get_action(state, player_index)
            self.board.move(group,direction)
            if self.board.get_looser():
                break
            player_index *= -1





