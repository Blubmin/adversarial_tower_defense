import pygame
from pygame.locals import *

from board import Board
from unit_agent import UnitAgent
from tower import Tower
from tower_agent import TowerAgent


class App:
    def __init__(self):
        self._running = True
        self._image_surf = None
        self._board = None
        self._agents = [TowerAgent(), UnitAgent()]


    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode((320, 444), pygame.HWSURFACE)
        self._running = True
        self._board = Board(0, 64)

        for agent in self._agents:
            agent.init(self._board)


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        # Quit game on pressing ESC
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                x, y = pygame.mouse.get_pos()
                if not self._board.contains_point(x, y):
                    return
                grid_x, grid_y = self._board.screen_to_grid(x, y)
                tower = Tower(grid_x, grid_y)
                self._board.add_tower(tower)

    def on_loop(self):
        for agent in self._agents:
            agent.step(self._board)
        self._board.step()

    def on_render(self):
        self._screen.fill((0, 0, 0))
        
        self._board.draw(self._screen)
        for agent in self._agents:
            agent.render()

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            start = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
