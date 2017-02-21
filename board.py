import pygame
import math


class Board:
    def __init__(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._cell_size = 32
        self._width = 10
        self._height = 10
        self._towers = [[None for x in range(self._height)] for x in range(self._width)]
        self._units = []
        self._bullets = []

    def addTower(self, tower):
        self._towers[tower._x][tower._y] = tower

    def addUnit(self, unit):
        self._units.append(unit)

    def addBullet(self, bullet):
        self._bullets.append(bullet)

    def step(self):
        # Check for updates on all units
        for unit in self._units:
            if unit._shouldDestroy:
                self._units.remove(unit)

            if unit._y > self._height:
                unit.setIsAtGoal()
                self._units.remove(unit)

        # Check for updates on all bullets
        for bullet in self._bullets:
            bullet.step()

            # Check for out of bounds
            if bullet._x > self._width or bullet._x < 0 or bullet._y > self._height or bullet._y < 0:
                bullet.setShouldDestroy()
                self._bullets.remove(bullet)

            # Check for collisions
            for unit in self._units:
                if self.hasCollision(bullet, unit):
                    unit.setShouldDestroy()
                    bullet.setShouldDestroy()
                    self._bullets.remove(bullet)


    def distance(self, obj1, obj2):
        return math.sqrt(pow(obj1._x - obj2._x, 2) + pow(obj1._y - obj2._y, 2))

    def hasCollision(self, obj1, obj2):
        return self.distance(obj1, obj2) < 0.5

    def draw(self, screen):
        line_color = (125, 125, 125)
        for x in range(self._offset_x, self._offset_x + self._width * self._cell_size + 1, self._cell_size):
            pygame.draw.line(screen, line_color, (x, self._offset_y),
                             (x, self._offset_y + self._height * self._cell_size))

        for y in range(self._offset_y, self._offset_y + self._height * self._cell_size + 1, self._cell_size):
            pygame.draw.line(screen, line_color, (self._offset_x, y),
                             (self._offset_x + self._width * self._cell_size, y))

        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                screen.blit(self._towers[i][j]._image,
                                  (i * self._cell_size + self._offset_x, j * self._cell_size + self._offset_y))

        for unit in self._units:
            screen.blit(unit._image, (unit._x * self._cell_size + self._offset_x, unit._y * self._cell_size + self._offset_y))

        for bullet in self._bullets:
            screen.blit(bullet._image, (bullet._x * self._cell_size + self._offset_x, bullet._y * self._cell_size + self._offset_y))