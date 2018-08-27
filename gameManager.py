
import abalone
import config
import tk as abaloneTk
import alphaBetaAgent
import gameState
import humanAgent
import randomAgent
import NNAgent

class Agent_repr(object):
    def __init__(self, type, depth, num_of_training, player_index, train_agent_str, train_agent_hue,
                 show_tk, load_NN_data):
        self.agent = None
        heuristics = [alphaBetaAgent.eval_fn_original, alphaBetaAgent.eval_fn_lost_marbles,
                      alphaBetaAgent.eval_fn_sumito, alphaBetaAgent.eval_fn_defensive,
                      alphaBetaAgent.aggressive_eval_fn]
        heuristics_str = ['Full', 'Lost marbles', 'Sumito', 'Defensive', 'Aggressive_Full']

        if type == 'AlphaBetaAgent':
            self.agent = alphaBetaAgent.AlphaBetaAgent(depth)
            if show_tk:
                self.agent.show_tk()
        if type == 'KeyboardAgent':
            self.agent = humanAgent.HumanAgent()
        if type == 'RandomAgent':
            self.agent = randomAgent.RandomAgent(show_tk)
        if type == 'NNAgent':
            if train_agent_str== 'AlphaBetaAgent':
                hue = heuristics[0]
                if train_agent_hue!=None:
                    hue = heuristics[heuristics_str.index(train_agent_hue)]
                train_agent = alphaBetaAgent.AlphaBetaAgent(1, hue)
                if show_tk:
                    self.train_agent.show_tk()
            elif train_agent_str == 'KeyboardAgent':
                train_agent = humanAgent.HumanAgent()
            else:
                train_agent_str = 'RandomAgent'
                train_agent = randomAgent.RandomAgent(show_tk)
            if train_agent_hue == None:
                train_agent_hue = 'no_hue'
            self.agent = NNAgent.NN(train_agent, train_agent_str, train_agent_hue,
                                    player_index=player_index, num_training=num_of_training, show_tk=show_tk, load_data=load_NN_data)



class Game(object):
    def __init__(self, train_agent, train_agent_hue, agent1_type, agent2_type, board_type, depth,
                 num_of_training, load_data):
        super(Game, self).__init__()
        self._is_tk = board_type == 'GUI'
        # self.tkState = None
        self.player1 = Agent_repr(agent1_type, depth, num_of_training, 1, train_agent,
                                  train_agent_hue, self._is_tk, load_data)
        self.player2 = Agent_repr(agent2_type, depth, num_of_training, -1, train_agent,
                                  train_agent_hue, self._is_tk, load_data)
        self.board = self.create_board(board_type)

        self._state = None
        """if 'humanPlayer'=0 no player is human 1,2 indicate which is human, 3 means both are human"""
        self.humanPlayers = int(agent1_type == 'KeyboardAgent') + int(agent2_type == 'KeyboardAgent') * 2

    def create_board(self, type):
        if type == 'SummaryDisplay':
            return abalone.Game_Board()
        elif type == 'GUI':
            self._is_tk = True
            return abaloneTk.Game_Board()
        return None

    def run(self):
        self.board.start(config.Players.Black.positions, config.Players.White.positions)
        initial = self.board.get_initial()
        player_index = 1
        marbles = self.board.get_marbles()
        gameState.GameState(marbles, initial, True)
        if self.humanPlayers == 3:
            state = abaloneTk.Game_Board()
            state.start(config.Players.Black.positions, config.Players.White.positions)
            state.mainloop()
        else:
            if self._is_tk:
                self.board.update_idletasks()
            self.board.changed = False
            turn_counter = 0
            while True:
                marbles = self.board.get_marbles()
                state = gameState.GameState(marbles, initial)
                self.board.changed = False
                if player_index == 1:
                    count = self.player1.agent.get_action(state, player_index, self.board)
                else:
                    # start_time = timeit.default_timer()
                    self.player2.agent.get_action(state, player_index, self.board)

                    # elapsed = timeit.default_timer() - start_time

                    # print(elapsed)
                if self.board.get_looser():
                    loser = self.board.get_looser()
                    if self._is_tk:
                        self.board.stop()
                    return loser, turn_counter
                player_index *= -1
                turn_counter += 1
                if turn_counter > 5000:
                    if self._is_tk:
                        self.board.stop()
                    return 0, turn_counter


