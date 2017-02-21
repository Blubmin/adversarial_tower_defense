import pygame
from pygame.locals import *

from tower import Tower
from board import Board


class App:
    def __init__(self):
        self._running = True
        self._image_surf = None
        self._board = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((320, 444), pygame.HWSURFACE)
        self._running = True
        self._board = Board(0, 64)
        self._board.addTower(Tower(), 1, 1)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self._board.draw(self._display_surf)

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
