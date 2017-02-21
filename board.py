import pygame


class Board:
    def __init__(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._grid_size = 32
        self._width = 10
        self._height = 10
        self._towers = [[None for x in range(self._height)] for x in range(self._width)]

    def add_tower(self, tower, x, y):
        self._towers[x][y] = tower

    def draw(self, display_surf):
        line_color = (125, 125, 125)
        for x in range(self._offset_x, self._offset_x + self._width * self._grid_size + 1, self._grid_size):
            pygame.draw.line(display_surf, line_color, (x, self._offset_y),
                             (x, self._offset_y + self._height * self._grid_size))

        for y in range(self._offset_y, self._offset_y + self._height * self._grid_size + 1, self._grid_size):
            pygame.draw.line(display_surf, line_color, (self._offset_x, y),
                             (self._offset_x + self._width * self._grid_size, y))

        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                display_surf.blit(self._towers[i][j]._image,
                                  (i * self._grid_size + self._offset_x, j * self._grid_size + self._offset_y))