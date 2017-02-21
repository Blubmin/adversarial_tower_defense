import pygame

from unit import Unit

class UnitAgent:
    def __init__(self):
        self._units = []

    def init(self, board):
        unit = Unit(3, -2)
        self._units.append(unit)
        board.addUnit(unit)

    def step(self, board):
        for unit in self._units:
            if unit._shouldDestroy:
                self._units.remove(unit)
            elif unit._isAtGoal:
                self._units.remove(unit)
            else:
                unit._y += 0.1

    def render(self):
        pass