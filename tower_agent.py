import pygame

from tower import Tower

class TowerAgent:
    def __init__(self):
        self._towers = []
        self._score = 0

    def init(self, board):
        tower = Tower(1, 8)
        self._towers.append(tower)
        board.add_tower(tower)

    def step(self, board):
        for unit in board._units:
            if unit._shouldDestroy:
                self._score += 1

    def render(self, screen, xCoord, yCoord):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Tower Score: {0}".format(self._score), 1, (255,255,0))
        screen.blit(label, (xCoord, yCoord))
