import itertools
import numpy as np
from abalone import Group, Logic, Action, Marble, MarbleManager
import multiprocessing
import numpy

BLACK = 1
WHITE = -1

def unwrap_self_g(arg, **kwarg):
    return GameState.get_all_moves2(*arg, **kwarg)


class GameState(object):
    def __init__(self, marbles, initial_length):
        self._marbles = MarbleManager(marbles)
        self._logic = Logic()
        self.initial = initial_length
        self.arr_state_rpr = numpy.zeros(shape=(9, 9), dtype=np.int64)  # todo to make sure if this process is
        # needed or can be spare
        self.player_how_lost_marble = 0
        self.state_string_need_update = True

    def create_state_string(self, player_index):
        if self.state_string_need_update:
            for marble in self._marbles:
                if (marble['owner'] == 1):
                    self.arr_state_rpr[marble['position'][0] - 1][marble['position'][1] - 1] = 1
                else:
                    self.arr_state_rpr[marble['position'][0] - 1][marble['position'][1] - 1] = 2

            self._state_string = np.array2string(np.reshape(self.arr_state_rpr, newshape=(81)),
                                                 max_line_width=300)
            self.state_string_need_update = False
        return self._state_string + str(player_index)

    def get_looser(self):
        '''get_looser() -> get the looser team, False if no one.'''
        for team, initial in zip((BLACK, WHITE), self.initial):
            if initial - len(self._marbles.get_owner(team)) >=6:
                return team
        return False

    # def get_legal_actions(self, agent_index):
    #     "returns all of the legal moves of the current player.todo implement get_all_moves in group class"
    #
    #     legal_actions = []
    #     player_marbles = self._marbles.get_owner(agent_index)
    #     for i in range(1, 4):
    #         for subset in itertools.combinations(player_marbles, i):
    #             group = Group(subset)
    #             if group.is_valid():
    #                 pool=multiprocessing.Pool(multiprocessing.cpu_count())
    #                 curlist=pool.apply_async(unwrap_self_g,group,agent_index,self._marbles).get()
    #                 legal_actions +=curlist
    #                 pool.terminate()
    #     legal_actions.reverse()
    #     return legal_actions
    #
    # def get_all_moves(self, group, agent_index):
    #     '''
    #     returns all of the possible moves of the group
    #     '''
    #     action_list = []
    #     for i in [0,1,2, 3, 4, 5]:
    #         try:
    #             self._logic.set_marbles(self._marbles)
    #             if self._logic.is_legal_move_logic(group, i, agent_index):
    #                 act = Action(group, i)
    #                 action_list.append(act)
    #         except AssertionError:
    #             continue
    #     return action_list
    #
    # def get_all_moves2(self, group, agent_index,marbles):
    #     '''
    #     returns all of the possible moves of the group
    #     '''
    #     action_list = []
    #     for i in [0,1,2, 3, 4, 5]:
    #         try:
    #             logic=Logic()
    #             if logic.is_legal_move_logic(group, i, agent_index):
    #                 act = Action(group, i)
    #                 action_list.append(act)
    #         except AssertionError:
    #             continue
    #     return action_list

    def get_legal_actions(self, agent_index):
        "returns all of the legal moves of the current player.todo implement get_all_moves in group class"

        legal_actions = []
        player_marbles = self._marbles.get_owner(agent_index)
        for i in range(1, 4):
            for subset in itertools.combinations(player_marbles, i):
                group = Group(subset)
                if group.is_valid():
                    legal_actions += self.get_all_moves(group, agent_index)
        legal_actions.reverse()
        return legal_actions

    def get_all_moves(self, group, agent_index):
        '''
        returns all of the possible moves of the group
        '''
        action_list = []
        for i in [0,1,2, 3, 4, 5]:
            try:
                self._logic.set_marbles(self._marbles)
                if self._logic.is_legal_move_logic(group, i, agent_index):
                    act = Action(group, i)
                    action_list.append(act)
            except AssertionError:
                continue
        return action_list

    # todo to erase if not useful
    def get_empty_spots(self):
        return np.where(self._board == 0)

    def apply_action(self, action, agent_index):
        (group,direction)=(action[0][0],action[0][1])
        self._logic.marbles=self._marbles
        moved_group = self._logic.get_moved(group, direction)
        enemy = self._logic.get_mirror_obstacles(group, direction)
        moved_enemy = self._logic.get_moved(enemy, direction)
        for marble in group + enemy:
            if marble not in self._marbles:
                print('hhh')
            else:
                self._marbles.remove(marble)

        for marble in moved_group + moved_enemy:
            if marble not in self._marbles:
                self._marbles.append(marble)
            else:
                print('problem ; marble already inside')

        looser = self.get_looser()
        self.state_string_need_update = True
        self.is_terminal = True if looser else False

    def generate_successor(self, agent_index=1, action=Action.STOP):
        # new_marbles = MarbleManager([Marble(marble['position'],marble['owner']) for marble in \
        #         self._marbles])
        successor = GameState(self._marbles, self.initial)
        successor.apply_action(action, agent_index)
        return successor

    def is_final_state(self):
        return self.is_terminal



        # tk=abaloneTk.Game_Board()
        # tk.start(config.Players.Black.positions,config.Players.White.positions)
        # tk.mainloop()
