import pygame

class Unit:
   def __init__(self, x, y):
        self._image = pygame.image.load("unit.png").convert_alpha()
        self._x = x
        self._y = y
