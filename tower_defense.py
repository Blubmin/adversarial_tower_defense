import pygame
from pygame.locals import *

from board import Board
from unit_agent import RandomUnitAgent
from tower import Tower
from tower_agent import TowerAgent
from generator import Generator
from mongo_wrapper import MongoWrapper

class App:
    def __init__(self):
        self._running = True
        self._image_surf = None
        self._board = None
        self._agents = [TowerAgent(10), RandomUnitAgent(10, 10, 1000)]
        self._generator = Generator()
        self._gamesPlayed = 0
        self._renderFullGame = False
        self._paused = False
        self._debugPath = False


    def on_init(self):
        pygame.init()
        MongoWrapper().clear_collections()
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
            elif event.key == K_r:
                self._renderFullGame = not self._renderFullGame
            elif event.key == K_p:
                self._paused = not self._paused
            elif event.key == K_u:
                self._debugPath = not self._debugPath
                self.on_render()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                x, y = pygame.mouse.get_pos()
                if not self._board.contains_point(x, y):
                    return
                grid_x, grid_y = self._board.screen_to_grid(x, y)

                for unit in self._board._units:
                    if unit._lastNode[0] == grid_x and unit._lastNode[1] == grid_y or unit._nextNode and unit._nextNode[0] == grid_x and unit._nextNode[1] == grid_y:
                        unit._drawPath = not unit._drawPath
                self.on_render()
            if event.button == 3: # Right mouse button
                x, y = pygame.mouse.get_pos()
                if not self._board.contains_point(x, y):
                    return
                grid_x, grid_y = self._board.screen_to_grid(x, y)
                tower = Tower(grid_x, grid_y)
                self._board.add_tower(tower)
                self.on_render()

    def on_loop(self):
        # for agent in self._agents:
        #     agent.step(self._board)
        self._generator.step(self._steps, self._board)
        self._board.step()

    def on_render(self):
        self._screen.fill((0, 0, 0))
        
        # Draw unit paths
        for unit in self._board._units:
            if unit._drawPath or self._debugPath:
                for node in unit._path:
                    nodeX = self._board._offset_x + node[0] * self._board._cell_size
                    nodeY = self._board._offset_y + node[1] * self._board._cell_size
                    rect = pygame.Surface((self._board._cell_size, self._board._cell_size))
                    rect.set_alpha(128)
                    rect.fill((180,0,0))
                    self._screen.blit(rect, (nodeX, nodeY))
        # Draw unit next node
        for unit in self._board._units:
            if unit._drawPath or self._debugPath:
                if unit._nextNode:
                    nodeX = self._board._offset_x + unit._nextNode[0] * self._board._cell_size
                    nodeY = self._board._offset_y + unit._nextNode[1] * self._board._cell_size
                    rect = pygame.Surface((self._board._cell_size, self._board._cell_size))
                    rect.set_alpha(128)
                    rect.fill((0,180,0))
                    self._screen.blit(rect, (nodeX, nodeY))

        self._board.draw(self._screen)

        # Draw unit paths
        # for unit in self._board._units:
        #     if unit._drawPath or self._debugPath:
        #         for node in unit._path:
        #             nodeX = self._board._offset_x + node[0] * self._board._cell_size
        #             nodeY = self._board._offset_y + node[1] * self._board._cell_size
        #             rect = pygame.Surface((self._board._cell_size, self._board._cell_size))
        #             rect.set_alpha(128)
        #             rect.fill((150,0,0))
        #             self._screen.blit(rect, (nodeX, nodeY))

        # xCoord = 10
        # for agent in self._agents:
        #     agent.render(self._screen, xCoord, 10)
        #     xCoord += (self._board._width * self._board._cell_size) / len(self._agents)
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Step: {0}".format(self._steps), 1, (255,255,0))
        self._screen.blit(label, (10, 10))

        label = myfont.render("Score: {0}".format(self._board.getScore()), 1, (255,255,0))
        self._screen.blit(label, ((self._board._width * self._board._cell_size) / 2, 10))

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
            if not self._paused:
                if self._steps < 1000:
                    self.on_loop()
                    if self._renderFullGame:
                        self.on_render()
                elif self._steps >= 1000:
                    self.on_render()
                    self._gamesPlayed += 1
                    self._generator.gameOver(self._board)
                    self.on_init()
                self._steps += 1
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
