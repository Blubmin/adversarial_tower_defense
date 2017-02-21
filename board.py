import pygame


class Board:
    def __init__(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._grid_size = 32
        self._width = 10
        self._height = 10
        self._towers = [[None for x in range(self._height)] for x in range(self._width)]
        self._units = []

    def addTower(self, tower):
        self._towers[tower._x][tower._y] = tower

    def addUnit(self, unit):
        self._units.append(unit)

    def step(self):
        for unit in self._units:
            if unit._y > self._height:
                unit.setIsAtGoal()
                self._units.remove(unit)

    def draw(self, screen):
        line_color = (125, 125, 125)
        for x in range(self._offset_x, self._offset_x + self._width * self._grid_size + 1, self._grid_size):
            pygame.draw.line(screen, line_color, (x, self._offset_y),
                             (x, self._offset_y + self._height * self._grid_size))

        for y in range(self._offset_y, self._offset_y + self._height * self._grid_size + 1, self._grid_size):
            pygame.draw.line(screen, line_color, (self._offset_x, y),
                             (self._offset_x + self._width * self._grid_size, y))

        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                screen.blit(self._towers[i][j]._image,
                                  (i * self._grid_size + self._offset_x, j * self._grid_size + self._offset_y))

        for unit in self._units:
            screen.blit(unit._image, (unit._x * self._grid_size + self._offset_x, unit._y * self._grid_size + self._offset_y))