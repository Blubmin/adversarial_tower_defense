import pygame
from pygame.locals import *
 
theApp = None

class Tower:
    def __init__(self):
        self._image = pygame.image.load("tower.png").convert_alpha()

class Board:
    def __init__(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._grid_size = 32
        self._width = 10
        self._height = 10
        self._towers = [[None for x in range(self._height)] for x in range(self._width)]

    def addTower(self, tower, x, y):
        self._towers[x][y] = tower

    def draw(self):
        line_color = (125, 125, 125)
        for x in range(self._offset_x, self._offset_x + self._width * self._grid_size + 1, self._grid_size):
            pygame.draw.line(theApp._display_surf, line_color, (x, self._offset_y), (x, self._offset_y + self._height * self._grid_size))

        for y in range(self._offset_y, self._offset_y + self._height * self._grid_size + 1, self._grid_size):
            pygame.draw.line(theApp._display_surf, line_color, (self._offset_x, y), (self._offset_x + self._width * self._grid_size, y))

        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                theApp._display_surf.blit(self._towers[i][j]._image, (i * self._grid_size + self._offset_x, j * self._grid_size + self._offset_y))

class App:
    def __init__(self):
        self._running = True
        self._image_surf = None
        self._board = None
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((320,444), pygame.HWSURFACE)
        self._running = True
        self._board = Board(0, 64)
        self._board.addTower(Tower(), 1, 1)
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        self._board.draw()

        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()