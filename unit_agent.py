import pygame

from math import sqrt
from random import randint
from unit import Unit

class UnitAgent:
    def __init__(self, maxUnits):
        self._units = []
        self._maxUnits = maxUnits

    def init(self, board):
        self._units = []
        self._placementDelay = 0
        self._score = 0
        for i in range(0, self._maxUnits):
            self.placeUnit(board)

    def step(self, board):
        # self._placementDelay -= 1
        # self.placeUnit(board)
        for unit in self._units:
            if unit._shouldDestroy:
                self._units.remove(unit)
            elif unit._isAtGoal:
                self._score += 1
                self._units.remove(unit)
            else:
                unit.step(board)
                # unit._y += 0.05
        if self._units:
            print()

    def placeUnit(self, board):
        # if self._placementDelay <= 0:
        #     self._placementDelay = randint(10, 100)
            unit = Unit(randint(0, board._width - 1), -1)
            self._units.append(unit)
            board.add_unit(unit)

    def render(self, screen, xCoord, yCoord):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Unit Score: {0}".format(self._score), 1, (255,255,0))
        screen.blit(label, (xCoord, yCoord))

