import pygame
import math

from tower import Tower

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

    def add_tower(self, tower):
        self._towers[tower._x][tower._y] = tower

    def add_unit(self, unit):
        self._units.append(unit)

    def add_bullet(self, bullet):
        self._bullets.append(bullet)

    def step(self):
        # Check for updates on all units
        for unit in self._units:
            if unit._shouldDestroy:
                self._units.remove(unit)

            elif unit._y > self._height:
                unit.setIsAtGoal()
                self._units.remove(unit)

        # Check for updates on all bullets
        for bullet in self._bullets:
            bullet.step()

            if bullet._shouldDestroy:
                self._bullets.remove(bullet)

            else:
                # Check for out of bounds
                if bullet._x > self._width or bullet._x < 0 or bullet._y > self._height or bullet._y < 0:
                    bullet.setShouldDestroy()
                    self._bullets.remove(bullet)

                # Check for collisions
                for unit in self._units:
                    if self.has_collision(bullet, unit):
                        unit.damage(50)
                        bullet.setShouldDestroy()
                        self._bullets.remove(bullet)

        # Updates towers
        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                self._towers[i][j].step(self)

    def distance(self, obj1, obj2):
        return math.sqrt(pow(obj1._x - obj2._x, 2) + pow(obj1._y - obj2._y, 2))

    def has_collision(self, obj1, obj2):
        return self.distance(obj1, obj2) < 0.5

    def draw(self, screen):
        # Draws grid
        line_color = (125, 125, 125)
        for x in range(self._offset_x, self._offset_x + self._width * self._cell_size + 1, self._cell_size):
            pygame.draw.line(screen, line_color, (x, self._offset_y),
                             (x, self._offset_y + self._height * self._cell_size))

        for y in range(self._offset_y, self._offset_y + self._height * self._cell_size + 1, self._cell_size):
            pygame.draw.line(screen, line_color, (self._offset_x, y),
                             (self._offset_x + self._width * self._cell_size, y))

        # Draws mouse tower
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.contains_point(mouse_x, mouse_y):
            s = Tower._image_transparent.copy()
            screen.blit(s, self.trunc_screen(mouse_x, mouse_y))

        # Draws towers
        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                screen.blit(self._towers[i][j]._image, self.grid_to_screen(i, j))

        # Draws enemy units
        for unit in self._units:
            screen.blit(unit._image, self.grid_to_screen(unit._x, unit._y))

        # Draws tower bullets
        for bullet in self._bullets:
            screen.blit(bullet._image, self.grid_to_screen(bullet._x, bullet._y))

    def grid_to_screen(self, x, y):
        return (x * self._cell_size + self._offset_x, y * self._cell_size + self._offset_y)

    def trunc_screen(self, x, y):
        return (((int) (x / self._cell_size)) * self._cell_size,
                ((int) (y / self._cell_size)) * self._cell_size)

    def screen_to_grid(self, x, y):
        return ((int) ((x - self._offset_x) / self._cell_size), (int) ((y - self._offset_y) / self._cell_size))

    def contains_point(self, x, y):
        return (self._offset_x <= x < self._offset_x + self._width * self._cell_size
                and self._offset_y <= y < self._offset_y + self._height * self._cell_size)