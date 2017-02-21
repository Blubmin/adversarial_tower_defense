import pygame

from tower import Tower

class TowerAgent:
    def __init__(self):
        self._towers = []

    def init(self, board):
        tower = Tower(1, 8)
        self._towers.append(tower)
        board.addTower(tower)

    def step(self, board):
        for tower in self._towers:
            for unit in board._units:
                if board.distance(tower, unit) < 5:
                    tower.shoot(board, unit)

    def render(self):
        pass
