import pygame
import random

from unit import Unit

class UnitAgent:
    def __init__(self):
        self._units = []
        self._maxUnits = 10

    def init(self, board):
        unit = Unit(random.randint(0, board._width - 1), -2)
        self._units.append(unit)
        board.add_unit(unit)

    def step(self, board):
        for unit in self._units:
            if unit._shouldDestroy:
                self._units.remove(unit)
            elif unit._isAtGoal:
                self._units.remove(unit)
            else:
                unit._y += 0.05

    def render(self):
        pass