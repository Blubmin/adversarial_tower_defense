import pygame

from functools import reduce
from operator import iadd
from random import randrange
from random import choice

from mongo_wrapper import MongoWrapper
from tower import Tower
from zscore import *

class TowerState:
    def __init__(self, board):
        self.unitsDeployed = len(board._units) + board._unitsDestroyed + board._unitsThatReachedGoal
        self.towersDeployed = board._num_towers
        self.towersInUpperLeft = reduce(iadd, map(lambda t: 1 if t._x < 5 and t._y < 5 else 0, board._tower_list), 0)
        self.towersInUpperRight = reduce(iadd, map(lambda t: 1 if t._x >= 5 and t._y < 5 else 0, board._tower_list), 0)
        self.towersInLowerLeft = reduce(iadd, map(lambda t: 1 if t._x < 5 and t._y >= 5 else 0, board._tower_list), 0)
        self.towersInLowerRight = reduce(iadd, map(lambda t: 1 if t._x >= 5 and t._y >= 5 else 0, board._tower_list), 0)
        self.unitsOnLeftSide = reduce(iadd, map(lambda t: 1 if t._x < 5 else 0, board._units), 0)
        self.unitsOnRightSide  = reduce(iadd, map(lambda t: 1 if t._x >= 5 else 0, board._units), 0)
        self.tick = board._tick

    def top_k(self, k):
        tower_data = MongoWrapper().get_tower_data()
        if tower_data is None:
            return [0]
        tower_data = [d for d in tower_data]
        zscores = []
        items = [[] for x in range(len(tower_data))]
        for key in self.__dict__:
            data = [d["state"][key] for d in tower_data]
            a = data + [self.__dict__[key]]
            zscores += [stats.zscore(numpy.array(a))]
        for i in range(len(tower_data)):
            for z in zscores:
                items[i] += [z[i]]
        z = items[-1]
        distances = [ -1 for x in range(len(tower_data))]



        return items[-1:]

class TowerAgent:
    def __init__(self, maxUnits):
        self._towers = []
        self._maxUnits = maxUnits
        self._actions = ["place_left_of_last_tower",
                         "place_right_of_last_tower",
                         "place_up_of_last_tower",
                         "place_down_of_last_tower",
                         "place_randomly",
                         "place_along_path"]
        self._actions_taken = []

        # For manually calculating zscores
        self._state_actions = None
        self._means = None
        self._sds = None

    def init(self, board):
        self._towers = []
        self._score = 0
        for i in range(0, self._maxUnits):
            self.placeTower(board)
            # tower = Tower(i, 8)
            # self._towers.append(tower)
            # board.add_tower(tower)

    def step(self, board):
        return self.placeTower(board)

    def gameOver(self, board):
        if self._actions_taken:
            tower_data = list(filter(lambda x: x["body_count"] > 0, map( lambda x: {"state": x[0].__dict__, "action": x[1], "score": board.getScore(), "body_count": x[2]._body_count} ,self._actions_taken)))
            if len(tower_data) > 0:
                MongoWrapper().save_tower_data(tower_data)

    def placeTower(self, board):
        if board._num_towers >= 10:
            return None

        # action = self.play_randomly(board)
        action = self.get_action(board)
        if action is None:
            return
        self._actions_taken += [(TowerState(board), action, board._last_tower)]  # Keeps track of actions taken in this game

    def get_action(self, board):
        tower_data = MongoWrapper().get_tower_data()
        if tower_data.count() is not 0:
            self.calc_zscores(board)

        if self._state_actions is None or len(self._state_actions) < 500 or randrange(0, 50) is 1:
            return self.play_randomly(board)
        return self.play_intelligently(board)

    def play_intelligently(self, board):
        state = TowerState(board)

        state_z = []
        for key in state.__dict__:
            state_z += [zscore(state.__dict__[key], self._means[key], self._sds[key])]

        top = self.top_k(state_z, 100)

        top = [self._state_actions[t[1]] for t in top]
        top.sort(key=lambda key: key[1])
        top = top[:10]
        top.sort(key=lambda key: key[2])

        for a in top:
            if getattr(self, a[2])(board):
                return a[2]
        return self.play_randomly(board)

    def play_randomly(self, board):
        action = ""
        if board._last_tower is None:
            action = "place_randomly"
        else:
            action = choice(self._actions)  # Picks a random action
        while not getattr(self, action)(board):  # Performs the action
            action = choice(self._actions)
        return action

    def top_k(self, zs, k):
        ds = []
        for i in range(len(self._state_actions)):
            ds += [(self.dist(zs, self._state_actions[i][0]), i)]
        return sorted(ds, key=lambda key: key[0])[:k]

    def dist(self, a, b):
        d = 0
        for i in range(len(a)):
            d += (a[i] - b[i])**2
        return d

    def calc_zscores(self, board):
        self._means = {}
        self._sds = {}

        state = TowerState(board)

        tower_data = MongoWrapper().get_tower_data()
        tower_data = [d for d in tower_data]

        if len(tower_data) is 0:
            return

        self._state_actions = [[[], -1, "", -1] for x in range(len(tower_data))]

        for key in state.__dict__:
            zscores, mu, sd = zscore_array([d["state"][key] for d in tower_data])
            self._means[key] = mu
            self._sds[key] = sd

            for i in range(len(zscores)):
                self._state_actions[i][0].append(zscores[i])

        for i in range(len(tower_data)):
            self._state_actions[i][1] = tower_data[i]["score"]
            self._state_actions[i][2] = tower_data[i]["action"]
            self._state_actions[i][3] = tower_data[i]["body_count"]

    def render(self, screen, xCoord, yCoord):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Tower Score: {0}".format(self._score), 1, (255,255,0))
        screen.blit(label, (xCoord, yCoord))

    def place_x_y_of_last_tower(self, board, x, y):
        if board._last_tower is None:
            return False
        tower = Tower(board._last_tower._x + x, board._last_tower._y + y)
        return board.add_tower(tower)

    def place_left_of_last_tower(self, board):
        return self.place_x_y_of_last_tower(board, -1, 0)

    def place_right_of_last_tower(self, board):
        return self.place_x_y_of_last_tower(board, 1, 0)

    def place_up_of_last_tower(self, board):
        return self.place_x_y_of_last_tower(board, 0, 1)

    def place_down_of_last_tower(self, board):
        return self.place_x_y_of_last_tower(board, 0, -1)

    def place_randomly_in_range(self, board, x_min, x_max, y_min, y_max):
        tower = Tower(randrange(x_min, x_max), randrange(y_min, y_max))

        count = board._num_towers
        while not board.add_tower(tower):
            assert count == board._num_towers, "place along path False error"
            tower = Tower(randrange(0, board._width), randrange(0, board._height))
        assert count + 1 == board._num_towers, "place along path True error"
        return True

    def place_randomly(self, board):
        return self.place_randomly_in_range(board, 0, board._width, 0, board._height)

    def place_top_left(self, board):
        return self.place_randomly_in_range(board, 0, board._width / 2, 0, board._height / 2)

    def place_bottom_left(self, board):
        return self.place_randomly_in_range(board, 0, board._width / 2, board._height / 2, board._height)

    def place_bottom_right(self, board):
        return self.place_randomly_in_range(board, board._width / 2, board._width, board._height / 2, board._height)

    def place_top_right(self, board):
        return self.place_randomly_in_range(board, board._width / 2, board._width, 0, board._height / 2)

    def place_along_path(self, board):
        if len(board._units) is 0:
            return False
        paths = list(filter(lambda x: x is not None, map(lambda u: board.path_from(int(u._x), int(u._y)), board._units)))
        paths.sort(key=lambda p: len(p))
        i = 0
        while i < len(paths) and len(paths[i][1:]) is 0:
            i += 1
        if i is len(paths):
            return False
        for cell in paths[i][1:]:
            count = board._num_towers
            if not board.add_tower(Tower(cell[0], cell[1])):
                assert count == board._num_towers, "place along path False error"
                continue
            assert count + 1 == board._num_towers, "place along path True error"
            return True
        return False