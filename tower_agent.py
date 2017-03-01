import pygame

from random import randint
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
        # tower = Tower(1, 8)
        # self._towers.append(tower)
        # board.add_tower(tower)

    def step(self, board):
        for unit in board._units:
            if unit._shouldDestroy:
                self._score += 1

    def placeTower(self, board):
        # if self._placementDelay <= 0:
        #     self._placementDelay = randint(10, 100)
            randX = randint(0, board._width - 1)
            randY = randint(0, board._width - 1)
            while board._towers[randX][randY] != None:
                randX = randint(0, board._width - 1)
                randY = randint(0, board._width - 1)
            tower = Tower(randX, randY)
            self._towers.append(tower)
            board.add_tower(tower)

    def render(self, screen, xCoord, yCoord):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Tower Score: {0}".format(self._score), 1, (255,255,0))
        screen.blit(label, (xCoord, yCoord))
