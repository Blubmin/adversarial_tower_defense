import pygame

from tower import Tower

class TowerAgent:
    def __init__(self):
        self._towers = []

    def init(self, board):
        tower = Tower(1, 8)
        self._towers.append(tower)
        board.add_tower(tower)

    def step(self, board):
        return

    def render(self):
        pass
