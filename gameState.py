import itertools
import numpy as np
from abalone import Group, Logic
import config
import tk as abaloneTk
from copy import deepcopy


class GameState(object):
    def __init__(self, marbles):
        self._marbles = deepcopy(marbles)
        self._logic = Logic()

    """
    TODO: Decide if we want to remove this
    # def get_legal_actions(self, agent_index):#todo to make sure we need the seperation between 2 players.
    #     if agent_index == 1:
    #         return self.get_agent_legal_actions()
    #     elif agent_index == -1:
    #         return self.get_agent_legal_actions()
    #     else:
    #         raise Exception("illegal agent index.")
    # 
    # def get_agent_legal_actions(self):
    #     "returns all of the legal moves of the current player.todo implement get_all_moves in group class"
    #     legal_actions = []
    #     player_marbles=self.game.marbles.get_owner(self._currentPlayer)
    #     for i in range(0,4):
    #         for subset in itertools.combinations(player_marbles,i):
    #             group=Group(subset)
    #             if(group.is_valid()):
    #                 legal_actions+=self._game.get_all_moves(group)
    #     return legal_actions
    """

    def get_legal_actions(self, agent_index):
        "returns all of the legal moves of the current player.todo implement get_all_moves in group class"
        legal_actions = []
        player_marbles = self._marbles.get_owner(agent_index)
        for i in range(0,4):
            for subset in itertools.combinations(player_marbles, i):
                group=Group(subset)
                if group.is_valid():
                    legal_actions += self.get_all_moves(group, agent_index)
        return legal_actions

    def get_all_moves(self, group, agent_index):
        '''
        returns all of the possible moves of the group
        '''
        action_list=[]
        for i in range(0, 6):
            try:
                if self._logic.is_legal_move_logic(group, i, agent_index):
                    act = Action(group, i)
                    action_list.append(act)
            except:
                continue
        return action_list


    #todo to erase if not useful
    def get_empty_spots(self):
        return np.where(self._board == 0)


    def apply_action(self, action, agent_index):
        positions_or_group = action[0][0]
        direction = action[0][1]

        if isinstance(positions_or_group, Group):
            group = positions_or_group
        else:
            group = Group(self._marbles.get_pos(positions_or_group))

        self._logic.marbles = self._marbles
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
        looser = self.game.get_looser()
        self.is_terminal = True if looser else False


    """
    TODO: Decide if we want to remove
    def generate_successor(self,agent_index=1,action=5):
        agent_index = agent_index * (-1)
        successor = GameState(agent_index,self._game) #todo change inputs.
        if agent_index == 1:
            successor.apply_action(action)
        elif agent_index == -1:
            successor.apply_opponent_action(action)
        else:
            raise Exception("illegal agent index.")
        return successor
    """

    def generate_successor(self, agent_index = 1, action = 5):
        successor = GameState(self._marbles)
        successor.apply_action(action, agent_index)
        return successor

    def is_final_state(self):
        return self.is_terminal



tk=abaloneTk.Game_Board()
tk.start(config.Players.Black.positions,config.Players.White.positions)
g=GameState(tk.marbles)
act_list=g.get_legal_actions(1)
tk.mainloop()