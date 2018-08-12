import itertools
import numpy as np
from abalone import Group, Logic ,Action, Marble, MarbleManager
import config
import tk as abaloneTk
from copy import deepcopy
import numpy

BLACK = 1
WHITE = -1

class GameState(object):
    def __init__(self, marbles, initial_length):
        self._marbles = marbles
        self._logic = Logic()
        self.initial = initial_length
        self.arr_state_rpr = numpy.zeros(shape=(9, 9))#todo to make sure if this process is needed or can be spare
        for marble in self._marbles:
            if(marble['owner']==1):
                self.arr_state_rpr[marble['position'][0]-1][marble['position'][1]-1]=1
            else:
                self.arr_state_rpr[marble['position'][0]-1][marble['position'][1]-1]=2
    def get_looser(self):
        '''get_looser() -> get the looser team, False if no one.'''
        for team, initial in zip((BLACK, WHITE), self.initial):
            if initial - len(self._marbles.get_owner(team)) >= initial / (14/6.0):
                return team
        return False


    def get_legal_actions(self, agent_index):
        "returns all of the legal moves of the current player.todo implement get_all_moves in group class"
        legal_actions = []
        player_marbles = self._marbles.get_owner(agent_index)
        for i in range(1,4):
            for subset in itertools.combinations(player_marbles, i):
                group=Group(subset)
                if group.is_valid():
                    legal_actions += self.get_all_moves(group, agent_index)
        legal_actions.reverse()
        return legal_actions

    def get_all_moves(self, group, agent_index):
        '''
        returns all of the possible moves of the group
        '''
        action_list=[]
        for i in range(0, 6):
            try:
                self._logic.set_marbles(self._marbles)
                if self._logic.is_legal_move_logic(group, i, agent_index):
                    act = Action(group, i)
                    action_list.append(act)
            except AssertionError:
                continue
        return action_list


    #todo to erase if not useful
    def get_empty_spots(self):
        return np.where(self._board == 0)


    def apply_action(self, action, agent_index):
        positions_or_group = action[0][0]
        direction = action[0][1]

        # if isinstance(positions_or_group, Group):
        #     group = positions_or_group
        # else:
        group = Group([Marble(marble['position'],marble['owner']) for marble in \
                positions_or_group])
        # group = Group(self._marbles.get_pos(positions_or_group.positions))
        self._logic.set_marbles(self._marbles)
        is_valid = self._logic.is_legal_move_logic(positions_or_group, direction, agent_index)
        if is_valid:
            moved_group = self._logic.get_moved(group, direction)
            enemy = self._logic.get_mirror_obstacles(group, direction)
            moved_enemy = self._logic.get_moved(enemy, direction)
            if len(enemy) > len(moved_enemy):
                self._marbles.remove(enemy[-1])
                enemy.pop(-1)
            enemy.update(moved_enemy)
            group.update(moved_group)
        looser = self.get_looser()
        self.is_terminal = True if looser else False



    def generate_successor(self, agent_index = 1, action = 5):
        new_marbles = MarbleManager([Marble(marble['position'],marble['owner']) for marble in \
                self._marbles])
        successor = GameState(new_marbles, self.initial)
        successor.apply_action(action, agent_index)
        return successor

    def is_final_state(self):
        return self.is_terminal



# tk=abaloneTk.Game_Board()
# tk.start(config.Players.Black.positions,config.Players.White.positions)
# tk.mainloop()