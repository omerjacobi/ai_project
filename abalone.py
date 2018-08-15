# Copyright (C) 2010 Unai Zalakain De Graeve
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''Game logic of Abalone'''

from operator import add, sub
from gettext import gettext as _
from library import NoNegIndexList, Reductors
from copy import deepcopy
import numpy

# representation of teams.
# NOTE: they can't be 0.
ERRORMSG12 = _('You can\'t move there.')
ERRORMSG11 = _('You can\'t push the enemy.')
ERRORMSG10 = _('You can\'t push your own marbles.')
ERRORMSG9 = _('You can\'t push an enemy in a lateral move.')
ERRORMSG8 = _('The marbles aren\'t yours.')
ERRORMSG7 = _('The group of marbles isn\'t valid.')
ERRORMSG6 = _('You can\'t move there.')
ERRORMSG5 = _('You can\'t push the enemy.')
ERRORMSG4 = _('You can\'t push your own marbles.')
ERRORMSG3 = _('You can\'t push an enemy in a lateral move.')
ERRORMSG2 = _('The marbles aren\'t yours.')
ERRORMSG1 = _('The group of marbles isn\'t valid.')
BLACK = 1
WHITE = -1
BOTH = 2


class Action(list):
    STOP = 5

    def __init__(self, group, direction):
        self.append((Group(group), direction))

    def __hash__(self):
        return tuple(self[0]).__hash__


class Matrix(list):
    '''Matrix() -> list with all the positions of an abalone's board.'''

    def __init__(self):
        rows = range(1, 10)
        ranges = zip([1] * 5 + range(2, 6), range(6, 10) + [10] * 5)

        self.rows = NoNegIndexList(rows)
        self.columns = NoNegIndexList(rows)

        rows = iter(rows)
        for r in ranges:
            row = rows.next()
            self.extend([(row, column) for column in range(*r)])


class Marble(dict):
    '''Marble() -> dict with 'position' and 'owner' 
    keys that represents an abalone's marble.'''

    def __init__(self, position, owner):
        self['position'] = position
        self['owner'] = owner

    def __hash__(self):
        return dict.__hash__(self)


class MarbleManager(list):
    '''MarbleManager(Marbles) -> list of Marble objects with special
    methods get_pos and get_owner.'''

    def get_pos(self, positions):
        '''get_pos(positions) -> get the Marble objects that have their
        position key in positions.
        
        positions -> list of (row, column) tuples.'''
        return [marble for marble in self if marble['position'] in positions]

    def get_owner(self, owner):
        '''get_owner(owner) -> get the Marble objects that have their
        owner key == owner.
        
        owner -> BLACK or WHITE'''
        if (owner == BOTH):
            return [self]
        return [marble for marble in self if marble['owner'] == owner]


class Group(list):
    '''Group(Marbles) -> list of Marble objects with special methods
    update and is_valid.'''

    def __init__(self, marbles=[]):
        # assert all([ isinstance(marble, Marble) for marble in marbles ]), self.__doc__
        self.extend(sorted(marbles, key=lambda marble: marble['position']))


    def get_owner(self):
        if (len(self)) > 0:
            return self[0]['owner']
        return 0


    def __hash__(self):
        return list(self).__hash__

    # def update(self, new):
    #     '''update(updated_marbles) -> update the position attribute of
    #     the marbles in the Group with the position attribute of others.
    #
    #     updated_marbles -> updated marbles to get the position attr.'''
    #     for old_m, new_m in zip(self, new):
    #         old_m['position'] = new_m['position']


    def is_valid(self):
        '''is_valid() -> return bool saying if this Group is a valid one.
        If valid, set "owner" and "positions" attributes with the owner and
        the positions of the marbles.'''

        # must have between 1 and 3 members
        if not 1 <= len(self) <= 3:
            return False

        # the owner of all the marbles must be the same
        # owners = [marble['owner'] for marble in self ]
        # if not Reductors.equal(owners):
        #     return False
        # self.owner = owners[0]
        # self.owner = self[0]['owner']
        # the position of the marbles must be in line
        positions = [marble['position'] for marble in self]
        if not len(positions) == 1:
            rows = [pos[0] for pos in positions]
            columns = [pos[1] for pos in positions]
            rows_consec = Reductors.consec(rows)
            columns_consec = Reductors.consec(columns)
            if not any((
                        Reductors.equal(rows) and columns_consec,
                        rows_consec and Reductors.equal(columns),
                        rows_consec and columns_consec)):
                return False
        self.positions = positions

        return True


class Logic(Matrix):
    '''Logic() -> group of methods with the game logic of abalone.'''
    marbles = []

    def set_marbles(self, marbles):
        self.marbles = marbles

    def is_legal_move_logic(self, group, direction, current):
        assert self.is_in_matrix(group), ERRORMSG1
        # make sure the moved group isn't thrown outside the grid:
        moved_group = self.get_moved(group, direction)
        assert len(group) == len(moved_group) and self.is_in_matrix(moved_group)

        assert group.get_owner() == current, ERRORMSG2

        obstacles = self.get_obstacles(group, direction)

        if not obstacles:
            moved_group = self.get_moved(group, direction)

        else:
            assert not self.is_lateral_move(group, direction), ERRORMSG3

            assert obstacles.is_valid()
            assert obstacles.get_owner() is not current, ERRORMSG4

            enemy = self.get_mirror_obstacles(group, direction)
            assert self.is_pushable(group, enemy), ERRORMSG5
            moved_group = self.get_moved(group, direction)
        assert len(group) == len(moved_group) and moved_group.is_valid() and self.is_in_matrix(
            moved_group), ERRORMSG6
        return True

    def is_in_matrix(self, group):
        '''is_in_matrix(group) -> return True if group is in Matrix,
        False otherways.
        
        group -> Group instance.'''
        return True
        # return all([ marble['position'] in self for marble in group ])

    def get_moved(self, group, direction):
        '''get_moved(group, direction) -> return the group moved in direction.

        group -> Group instance.
        direction -> direction of movement, in range(6)'''
        diffs = 1, 1, 0, -1, -1, 0
        row_diff = diffs[(direction + 1) % 6]
        column_diff = diffs[direction]

        l = []
        for marble in group:
            row = marble['position'][0] + row_diff
            col = marble['position'][1] + column_diff
            if row > 0 and row < 10 and col > 0 and col < 10:
                if (row, col) in self:
                    l.append(Marble((row, col), marble['owner']))
                    # try:
                    #     row = self.rows[self.rows.index(marble['position'][0]) + row_diff]
                    #     column = self.columns[self.columns.index(marble['position'][1]) + column_diff]
                    # except IndexError:
                    #     pass
                    # else:
                    #     if (row, column) in self:
                    #         l.append(Marble((row, column), marble['owner']))
        return Group(l)

    def get_obstacles(self, group, direction):
        '''get_obstacles(group, direction) -> return the obstacles when trying to move
        group in direction.
        
        group -> Group instance.
        direction -> direction of movement, in range(6).'''
        moved_group = self.get_moved(group, direction)
        diff = [marble['position'] for marble in moved_group if marble not in group]
        return Group([marble for marble in self.marbles if marble['position'] in diff])

    def is_lateral_move(self, group, direction):
        '''is_lateral_move(group, direction) -> return True if the movement
        of group in direction is a lateral move, False otherways.
        
        group -> Group instance.
        direction -> direction of movement, in range(6).'''
        moved_group = self.get_moved(group, direction)
        return all([marble not in group for marble in moved_group])

    def get_mirror_obstacles(self, group, direction):
        '''get_mirror_obstacles(group, direction) -> return the obstacles when
        trying to move group in direction len(group) times.
        
        group -> Group instance.
        direction -> direction of movement, in range(6).'''
        obstacles = []
        for movement in range(len(group)):
            obstacle = self.get_obstacles(group, direction)
            if not obstacle:
                break
            obstacles.extend(obstacle)
            group = self.get_moved(group, direction)
        return Group(obstacles)

    def is_pushable(self, group, mirror_obstacles):
        '''is_pushable(group, mirror_obstacles) -> return True if group
        can push the mirror_obstacles, False otherways.
        
        group -> Group instance
        mirror_obstacles -> obstacles returned by Logic.get_mirror_obstacles'''
        return all((
            mirror_obstacles.is_valid(),
            self.is_in_matrix(mirror_obstacles),
            len(group) > len(mirror_obstacles),
        ))


class Game_Board(object):
    '''Game() -> An abalone game.'''

    logic = Logic()

    def start(self, black=(), white=()):
        '''start(black=(), white=()) -> start a new game. 
        
        black -> positions of the marbles of the black team.
        white -> positions of the marbles of the white team.'''
        self.marbles = MarbleManager(
            [Marble(position, BLACK) for position in black] + \
            [Marble(position, WHITE) for position in white]
        )
        self.current = BLACK
        self.initial = len(black), len(white)
        self.end_of_game=False
    def get_marbles(self):
        return MarbleManager([Marble(marble['position'], marble['owner']) for marble in self.marbles])

    def get_initial(self):
        return self.initial

    def get_looser(self):
        '''get_looser() -> get the looser team, False if no one.'''
        for team, initial in zip((BLACK, WHITE), self.initial):
            if initial - len(self.marbles.get_owner(team)) >=6:
                return team
        return False

    def next(self):
        '''next() -> switch the actual player.'''
        if self.current == BLACK:
            self.current = WHITE
        else:
            self.current = BLACK

    def move(self, positions_or_group, direction):
        if isinstance(positions_or_group, Group):
            group = positions_or_group
        else:
            group = Group(self.marbles.get_pos(positions_or_group))

        self.logic.marbles = self.marbles

        assert group.is_valid() and self.logic.is_in_matrix(group), ERRORMSG7
        assert group.get_owner() == self.current, ERRORMSG8

        obstacles = self.logic.get_obstacles(group, direction)
        moved_enemy, enemy = [], []
        if not obstacles:
            moved_group = self.logic.get_moved(group, direction)

        else:
            assert not self.logic.is_lateral_move(group, direction), ERRORMSG9
            assert obstacles.is_valid()
            assert obstacles.get_owner() is not self.current, ERRORMSG10

            enemy = self.logic.get_mirror_obstacles(group, direction)
            assert self.logic.is_pushable(group, enemy), ERRORMSG11

            moved_enemy = self.logic.get_moved(enemy, direction)
            moved_group = self.logic.get_moved(group, direction)

        assert len(group) == len(moved_group) and moved_group.is_valid() and self.logic.is_in_matrix(
            moved_group), ERRORMSG12
        for marble in group + enemy:
            if marble not in self.marbles:
                print('hhh')
            else:
                self.marbles.remove(marble)

        for marble in moved_group + moved_enemy:
            if marble not in self.marbles:
                self.marbles.append(marble)
            else:
                print('problem ; marble already inside')
        # group.update(moved_group)
        return Action(moved_group, direction)

    def is_valid_move(self, positions_or_group, direction):
        if isinstance(positions_or_group, Group):
            group = positions_or_group
        else:
            group = Group(self.marbles.get_pos(positions_or_group))

        self.logic.set_marbles(self.marbles)
        return self.logic.is_legal_move_logic(group, direction, self.current)

    def get_all_moves(self, group):
        '''
        returns all of the possible moves of the group
        '''
        action_list = []
        for i in range(0, 6):
            try:
                if self.is_valid_move(group, i):
                    act = Action(group, i)
                    action_list.append(act)
            except:
                continue
        return action_list
