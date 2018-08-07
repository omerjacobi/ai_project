import itertools
import abalone
from abalone import Group
class GameState(object):
    def __init__(self,curPlayer,game,board=None,score=0,done=False):
        super(GameState, self).__init__()
        self._done=done
        self._score=score
        self._board=board
        self._game=game
        self._currentPlayer=curPlayer


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


    def get_legal_actions(self, agent_index):
        if agent_index == 0:
            return self.get_agent_legal_actions()
        elif agent_index == 1:
            return self.get_opponent_legal_actions()
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
#

    def apply_opponent_action(self, action):
        if self._board[action.row, action.column] != 0:
            raise Exception("illegal opponent action (%s,%s) isn't empty." % (action.row, action.column))
        if action.value <= 0:
            raise Exception("The action value must be positive integer.")
        self._board[action.row, action.column] = action.value
        if not self.get_agent_legal_actions():
            self._done = True

    def apply_action(self, action):""


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
#
