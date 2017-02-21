import pygame

class Bullet:
    def __init__(self, x, y, vx, vy):
        self._image = pygame.image.load("bullet.png").convert_alpha()
        self._x = x
        self._y = y
        self._vx = vx
        self._vy = vy
        self._shouldDestroy = False

    def setShouldDestroy(self):
        self._shouldDestroy = True

    def step(self):
        self._x += self._vx
        self._y += self._vy
