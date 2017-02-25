import pygame

from bullet import Bullet


class Tower:

    def __init__(self, x, y):
        Tower._image = pygame.image.load("tower.png").convert_alpha()
        Tower._image_transparent = pygame.image.load("tower_transparent.png").convert_alpha()
        self._x = x
        self._y = y
        self._shootingDelay = 0
        self._timeOfLastShot = 0

    def step(self, board):
        self._shootingDelay -= 1
        for unit in board._units:
            if board.distance(self, unit) < 5:
                self.shoot(board, unit)

    def shoot(self, board, target):        
        if self._shootingDelay <= 0:
            self._shootingDelay = 100
            dist = board.distance(self, target)
            dx = (target._x - self._x) / dist / 3
            dy = (target._y - self._y) / dist / 3
            board.add_bullet(Bullet(self._x, self._y, dx, dy))
