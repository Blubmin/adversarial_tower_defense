import pygame
import math

from tower import Tower
from unit import Unit

class BoardState:
    def __init__(self, board):
        self.unitsDeployed = len(board._units) + board._unitsDestroyed + board._unitsThatReachedGoal
        self.towersDeployed = 0
        self.towersInUpperLeft = 0
        self.towersInUpperRight = 0
        self.towersInLowerLeft = 0
        self.towersInLowerRight = 0
        self.unitsOnLeftSide = 0
        self.unitsOnRightSide = 0
        for col in range(0, board._width):
            for row in range(0, board._height):
                tower = board._towers[row][col]
                if not (tower is None):
                    self.towersDeployed += 1
                    if tower._x < board._width/2:
                        if tower._y < board._height/2:
                            self.towersInUpperLeft += 1
                        else:
                            self.towersInLowerLeft += 1
                    else:
                        if tower._y < board._height/2:
                            self.towersInUpperRight += 1
                        else:
                            self.towersInLowerRight += 1
        for unit in board._units:
            if unit._x < board._width/2:
                self.unitsOnLeftSide += 1
            else:
                self.unitsOnRightSide += 1

    def normalizedDistToState(self, boardState):
        thisVector = []
        otherVector = []
        # Find the sum of all the state values
        thisTotal = 0.0
        otherTotal = 0.0
        for key in self.__dict__:
            thisTotal += pow(self.__dict__[key], 2)
            otherTotal += pow(boardState.__dict__[key], 2)
        thisTotal = math.sqrt(thisTotal)
        otherTotal = math.sqrt(otherTotal)
        # Normalize the state by dividing by the sum
        for key in self.__dict__:
            if thisTotal > 0:
                thisVector.append(self.__dict__[key] / thisTotal)
            if otherTotal > 0:
                otherVector.append(boardState.__dict__[key] / otherTotal)
        # Get the dist between the normalized states (max distance would be 1)
        dist = 0.0
        for i in range(0, len(thisVector)):
            dist += abs(thisVector[i] - otherVector[i])
        return dist


class Board:
    def __init__(self, offset_x, offset_y):
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._cell_size = 32
        self._width = 10
        self._height = 10
        self._towers = [[None for x in range(self._height)] for x in range(self._width)]
        self._last_tower = None
        self._units = []
        self._bullets = []
        self._unitsThatReachedGoal = 0
        self._unitsDestroyed = 0

    def hasTower(self, x, y):
        if x < 0 or x >= self._width:
            return False
        if y < 0 or y >= self._width:
            return False
        return self._towers[x][y] != None

    def add_tower(self, tower):
        if self.hasTower(tower._x, tower._y):
            return False
        self._towers[tower._x][tower._y] = tower
        if not self.path_exists():
            self._towers[tower._x][tower._y] = None
            return False
        self._last_tower = tower
        return True

    def add_unit(self, unit):
        self._units.append(unit)

    def add_bullet(self, bullet):
        self._bullets.append(bullet)

    def step(self):
        for unit in self._units:
            unit.step(self)

        # Check for updates on all units
        for unit in self._units:
            if unit._shouldDestroy:
                self._unitsDestroyed += 1
                self._units.remove(unit)

            elif unit._y > self._height:
                self._unitsThatReachedGoal += 1
                unit.setIsAtGoal()
                self._units.remove(unit)

        # Check for updates on all bullets
        for bullet in self._bullets:
            bullet.step()

            if bullet._shouldDestroy:
                self._bullets.remove(bullet)
                continue

            # Check for out of bounds
            if bullet._x > self._width or bullet._x < 0 or bullet._y > self._height+2 or bullet._y < -2:
                bullet.setShouldDestroy()

            else:
                # Check for collisions
                for unit in self._units:
                    if self.has_collision(bullet, unit):
                        unit.damage(50)
                        bullet.setShouldDestroy()
                        break

        # Updates towers
        for i in range(self._width):
            for j in range(self._height):
                if (self._towers[i][j] is None):
                    continue
                self._towers[i][j].step(self)

    # The state of the board at a given step (used by the generator)
    def getState(self):
        return BoardState(self)

    # The score for the game (used by the generator)
    def getScore(self):
        return self._unitsDestroyed

    def execute(self, action):
        if action.name == "PlaceUnitAction":
            self.add_unit(Unit(action.x, -1))
        elif action.name == "PlaceTowerAction":
            self.add_tower(Tower(action.x, action.y))

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
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # if self.contains_point(mouse_x, mouse_y):
        #     s = Tower._image_transparent.copy()
        #     screen.blit(s, self.trunc_screen(mouse_x, mouse_y))

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

    def path_exists(self):
        for x in range(len(self._towers[0])):
            if self.path_from(x, 0) is None:
                continue
            return True
        return False

    def path_from(self, x, y):
        if self.hasTower(x, y):
            return None

        open_nodes = []
        nodes = [[(False, -1, (-1, -1)) for x in range(0, self._height)] for x in range(0, self._width)]
        nodes[x][y] = (True, 0, None)
        open_nodes.append((0, (x, y)))

        while len(open_nodes) > 0:
            node = open_nodes.pop(0)

            if node[1][1] is 9:
                path = []
                path.append(node[1])
                temp = nodes[node[1][0]][node[1][1]]
                while temp[2] is not None:
                    path = [temp[2]] + path
                    temp = nodes[temp[2][0]][temp[2][1]]
                return path

            for i in range(max(0, node[1][0] - 1), min(self._width, node[1][0] + 2)):
                for j in range(max(0, node[1][1] - 1), min(self._height, node[1][1] + 2)):
                    if self.hasTower(i, j):
                        continue
                    if i is node[1][0] and j is node[1][1]:
                        continue
                    if i is not node[1][0] and j is not node[1][1]:
                        continue
                    if nodes[i][j][0] and node[0] + 1 >= nodes[i][j][1]:
                        continue

                    open_nodes.append((node[0] + 1, (i, j)))
                    nodes[i][j] = (True, node[0] + 1, node[1])

            open_nodes.sort(key=lambda n: n[0])

        return None