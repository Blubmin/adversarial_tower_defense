import pygame

from functools import reduce
from operator import iadd
from random import randrange
from random import choice
from tower import Tower
from mongo_wrapper import MongoWrapper

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

    def init(self, board):
        self._towers = []
        self._score = 0
        for i in range(0, self._maxUnits):
            self.placeTower(board)
            # tower = Tower(i, 8)
            # self._towers.append(tower)
            # board.add_tower(tower)

    def step(self, board):
        rand = randrange(0, 100)
        return (self.placeTower(board) if rand is 1 else None)

    def gameOver(self, board):
        tower_data = map( lambda x: {"state": x[0].__dict__, "action": x[1], "score": board._unitsDestroyed} ,self._actions_taken)
        MongoWrapper().save_tower_data(tower_data)

    def placeTower(self, board):
        if board._num_towers >= 10:
            return None
        tower_data = MongoWrapper().get_tower_data()

        count = board._num_towers
        if board._last_tower is None:
            action = "place_randomly"
        else:
            action = choice(self._actions) # Picks a random action
        while not getattr(self, action)(board): # Performs the action
            assert board._num_towers == count, "{}: actual {} expected {}".format(action, board._num_towers, count)
            action = choice(self._actions)
        self._actions_taken += [(TowerState(board), action)] # Keeps track of actions taken in this game
        assert board._num_towers == count + 1, "{}: actual {} expected {}".format(action, board._num_towers, count + 1)
        return action

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

    def place_randomly(self, board):
        tower = Tower(randrange(0, board._width), randrange(0, board._height))

        count = board._num_towers
        while not board.add_tower(tower):
            assert count == board._num_towers, "place along path False error"
            tower = Tower(randrange(0, board._width), randrange(0, board._height))
        assert count + 1 == board._num_towers, "place along path True error"
        return True

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