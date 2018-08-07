import itertools
import numpy as np
import abalone
from abalone import Group
from gameManager import Action

class GameState(object):
    def __init__(self,curPlayer,game,board=None,score=0,done=False):
        super(GameState, self).__init__()
        self._done=done
        self._score=score
        self._board=board
        self._game=game
        self._currentPlayer=curPlayer
        self.is_terminal = False


    @property
    def done(self):
        return self._done

    @property
    def score(self):
        return self._score

    @property
    def board(self):
        return self._board
    @property
    def game(self):
        return self._game


    def get_legal_actions(self, agent_index):#todo to make sure we need the seperation between 2 players.
        if agent_index == 1:
            return self.get_agent_legal_actions()
        elif agent_index == -1:
            return self.get_agent_legal_actions()
        else:
            raise Exception("illegal agent index.")

    def get_agent_legal_actions(self):
        "returns all of the legal moves of the current player.todo implement get_all_moves in group class"
        legal_actions = []
        player_marbles=self._board.getPlayerMarbles(self._currentPlayer)
        for i in range(0,4):
            for subset in itertools.combinations(player_marbles,i):
                group=Group(subset)
                if(group.is_valid()):
                    legal_actions+=self._game.get_all_moves(group)
        return legal_actions

    #todo to erase if not useful
    def get_empty_spots(self):
        return np.where(self._board == 0)


    def apply_action(self, action):
        self.game.move(action.group,action.direction)
        looser = self.game.get_looser()
        self.is_terminal = True if looser else False


    def generate_successor(self, agent_index=1, action=Action.STOP):
        agent_index=agent_index*(-1)
        successor = GameState(agent_index,self._game)#todo more inputs.
        if agent_index == 1:
            successor.apply_action(action)
        elif agent_index == -1:
            successor.apply_opponent_action(action)
        else:
            raise Exception("illegal agent index.")
        return successor

    def is_final_state(self):
        return self.is_terminal
#
