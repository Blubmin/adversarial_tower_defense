import pygame
from pygame.locals import *

from board import Board
from unit_agent import UnitAgent
from tower import Tower
from tower_agent import TowerAgent
from generator import Generator

class App:
    def __init__(self):
        self._running = True
        self._image_surf = None
        self._board = None
        self._agents = [TowerAgent(10), UnitAgent(10)]
        self._generator = Generator()


    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode((320, 444), pygame.HWSURFACE)
        self._running = True
        self._board = Board(0, 64)
        self._steps = 0

        # for agent in self._agents:
        #     agent.init(self._board)
        self._generator.init()


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        # Quit game on pressing ESC
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                self._running = False
            elif event.key == K_SPACE:
                self.on_init()
                # self._board = Board(0, 64)
                # self._steps = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                x, y = pygame.mouse.get_pos()
                if not self._board.contains_point(x, y):
                    return
                grid_x, grid_y = self._board.screen_to_grid(x, y)
                tower = Tower(grid_x, grid_y)
                self._board.add_tower(tower)

    def on_loop(self):
        # for agent in self._agents:
        #     agent.step(self._board)
        self._generator.step(self._steps, self._board)
        self._board.step()

    def on_render(self):
        self._screen.fill((0, 0, 0))
        
        self._board.draw(self._screen)
        # xCoord = 10
        # for agent in self._agents:
        #     agent.render(self._screen, xCoord, 10)
        #     xCoord += (self._board._width * self._board._cell_size) / len(self._agents)
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Step: {0}".format(self._steps), 1, (255,255,0))
        self._screen.blit(label, (10, 10))

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
            if self._steps < 1000:
                self.on_loop()
                self.on_render()
            elif self._steps == 1000:
                self._generator.gameOver(self._board)
            self._steps += 1
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
