import pygame

from bullet import Bullet


class Tower:

    def __init__(self, x, y):
        Tower._image = pygame.image.load("tower.png").convert_alpha()
        self._x = x
        self._y = y
        self._shootingDelay = 1000
        self._timeOfLastShot = 0

    def step(self, board):
        for unit in board._units:
            if board.distance(self, unit) < 5:
                self.shoot(board, unit)

    def shoot(self, board, target):
        if pygame.time.get_ticks() - self._timeOfLastShot > self._shootingDelay:
            dist = board.distance(self, target)
            dx = (target._x - self._x) / dist / 3
            dy = (target._y - self._y) / dist / 3
            board.add_bullet(Bullet(self._x, self._y, dx, dy))
            self._timeOfLastShot = pygame.time.get_ticks()
