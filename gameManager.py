import abalone
import config
import tk as abaloneTk
import alphaBetaAgent
import gameState
import humanAgent


class Agent_repr(object):
    def __init__(self, type):
        self.agent = None
        if type == 'AlphaBetaAgent':
            self.agent = alphaBetaAgent.AlphaBetaAgent(1)
        if type == 'KeyboardAgent':
            self.agent = humanAgent.HumanAgent()



class Game(object):
    def __init__(self, agent1_type, agent2_type, board_type):
        super(Game, self).__init__()
        self.tkState = None
        self.player1 = Agent_repr(agent1_type)
        self.player2 = Agent_repr(agent2_type)
        self.board = self.create_board(board_type)
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
            self.board.update_idletasks()
            self.board.changed = False
            while True:
                marbles = self.board.get_marbles()
                state = gameState.GameState(marbles, initial)
                self.board.changed = False
                if player_index == 1:
                    (group, direction) = self.player1.agent.get_action(state, player_index, self.board)
                else:
                    (group, direction) = self.player2.agent.get_action(state, player_index, self.board)
                if self.board.get_looser():
                    break
                player_index *= -1
    #
    # def initializeForHuman(self):
    #     self.tkState = abaloneTk.Game_Board()
    #     self.tkState.start(config.Players.Black.positions, config.Players.White.positions)
