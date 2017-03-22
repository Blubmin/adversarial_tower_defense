import pygame

from random import randrange
from tower import Tower

class TowerAgent:
    def __init__(self, maxUnits):
        self._towers = []
        self._maxUnits = maxUnits

    def init(self, board):
        self._towers = []
        self._score = 0
        for i in range(0, self._maxUnits):
            self.placeTower(board)
            # tower = Tower(i, 8)
            # self._towers.append(tower)
            # board.add_tower(tower)

    def step(self, board):
        for unit in board._units:
            if unit._shouldDestroy:
                self._score += 1

    def placeTower(self, board):
        # if self._placementDelay <= 0:
        #     self._placementDelay = randint(10, 100)
            randX = randrange(0, board._width)
            randY = randrange(0, board._width)
            while board._towers[randX][randY] != None:
                randX = randrange(0, board._width)
                randY = randrange(0, board._width)
            tower = Tower(randX, randY)
            self._towers.append(tower)
            board.add_tower(tower)

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
        self.place_x_y_of_last_tower(board, -1, 0)

    def place_right_of_last_tower(self, board):
        self.place_x_y_of_last_tower(board, 1, 0)

    def place_up_of_last_tower(self, board):
        self.place_x_y_of_last_tower(board, 0, -1)

    def place_down_of_last_tower(self, board):
        self.place_x_y_of_last_tower(board, 0, 1)

    def place_randomly(self, board):
        tower = Tower(randrange(0, board._width), randrange(0, board._height))

        while not board.add_tower(tower):
            tower = Tower(randrange(0, board._width), randrange(0, board._height))

    def place_along_path(self, board):
        paths = map(lambda u: board.path_from(int(u._x), int(u._y)), board._units)
        paths.sort(key=lambda p: len(p))
        for cell in paths[0][1:]:
            if not board.add_tower(Tower(cell[0], cell[1])):
                continue
            return True
        return False