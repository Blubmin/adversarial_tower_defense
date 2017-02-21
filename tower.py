import pygame


class Tower:
    def __init__(self, x, y):
        self._image = pygame.image.load("tower.png").convert_alpha()
        self._x = x
        self._y = y