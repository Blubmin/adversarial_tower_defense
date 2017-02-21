import pygame


class Tower:
    def __init__(self):
        self._image = pygame.image.load("tower.png").convert_alpha()