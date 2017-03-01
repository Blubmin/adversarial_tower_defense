import pygame

class Unit:
    def __init__(self, x, y):
        self._image = pygame.image.load("unit.png").convert_alpha()
        self._x = x
        self._y = y
        self._health = 150
        self._shouldDestroy = False
        self._isAtGoal = False

    def setShouldDestroy(self):
        self._shouldDestroy = True

    def setIsAtGoal(self):
        self._isAtGoal = True

    def damage(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._shouldDestroy = True
