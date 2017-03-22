import pygame

from math import sqrt

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
STOP = 4

class Unit:
    def __init__(self, x, y):
        self._image = pygame.image.load("unit.png").convert_alpha()
        self._x = x
        self._y = y
        self._speed = 0.05
        self._direction = None
        self._lastNode = (x, y)
        self._nextNode = None
        self._health = 300
        self._shouldDestroy = False
        self._isAtGoal = False
        self._dangerMap = [[0 for x in range(10)] for x in range(11)]
        self._safetyMap = [[0 for x in range(10)] for x in range(11)]
        self._towers = []
        self._path = []
        self._drawPath = False

    def setShouldDestroy(self):
        self._shouldDestroy = True

    def setIsAtGoal(self):
        self._isAtGoal = True

    def damage(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._shouldDestroy = True

    def step(self, board):
        # If no astar has been calculated yet, calculate it
        if not self._nextNode:
            astar(self, board)
        else:
            # If it is at the next node in the path, and there are still nodes left to be traversed
            if self.isAtNextNode(board) and len(self._path) > 0:
                self._lastNode = self._nextNode
                # If tower placements changed, recompute astar
                if self.didTowerConfigurationChange(board):
                    astar(self, board)
                # Else go to next node in path
                else:
                    self._nextNode = self._path[0]
                    self._direction = directionFromNodes(self._lastNode, self._nextNode)
                    self._path = self._path[1:]

        # Move in direction of next node
        moveX = self._nextNode[0] - self._x
        moveY = self._nextNode[1] - self._y
        if abs(moveX) < self._speed:
            self._x += moveX
        else:
            self._x += self._speed if (self._nextNode[0] > self._x) else -self._speed
        if abs(moveY) < self._speed:
            self._y += moveY
        else:
            self._y += self._speed if (self._nextNode[1] > self._y) else -self._speed

    def isAtNextNode(self, board):
        if abs(self._nextNode[0] - self._x) <= 0.1 and abs(self._nextNode[1] - self._y) <= 0.1:
            return True
        # if self._direction == NORTH:
        #     if self._y <= self._nextNode[1]+0.01:
        #         return True
        # elif self._direction == EAST:
        #     if self._x >= self._nextNode[0]-0.01:
        #         return True
        # elif self._direction == SOUTH:
        #     if self._y >= self._nextNode[1]-0.01:
        #         return True
        # elif self._direction == WEST:
        #     if self._x <= self._nextNode[0]+0.01:
        #         return True
        return False

    def calculateDanger(self, board):
        # Reset danger map to all 0s
        self._dangerMap = [[0 for x in range(board._width)] for x in range(board._height+1)]
        towerRange = 3
        towerRangeSquared = towerRange * towerRange
        # Find all towers on the board
        for y in range(board._height):
            for x in range(board._width):
                # For each tower, add 1 danger to all cells within its range
                if board._towers[x][y]:
                    for dy in range(max(0, y-towerRange), min(y+towerRange, board._height+1)):
                        for dx in range(max(0, x-towerRange), min(x+towerRange, board._width)):
                            # If cell is within tower range
                            dist = sqrt(pow(y-dy, 2) + pow(x-dx, 2))
                            if dist < towerRange:
                                self._dangerMap[dy][dx] += 3#towerRange-dist
    def calculateSafety(self, board):
        # Reset safety map to all 0s
        self._safetyMap = [[0 for x in range(board._width)] for x in range(board._height+1)]
        unitRange = 2
        # For each unit on the board
        for unit in board._units:
            if unit != self:
                # Subtract 1 danger from all cells within radius of unit
                for dy in range(max(0, int(self._y)-unitRange), min(int(self._y)+unitRange, board._height+1)):
                    for dx in range(max(0, int(self._x)-unitRange), min(int(self._x)+unitRange, board._width)):
                        # If cell is within tower range
                        dist = sqrt(pow(int(self._y)-dy, 2) + pow(int(self._x)-dx, 2))
                        if dist < unitRange:
                            self._safetyMap[dy][dx] += 1#towerRange-dist
    def printDangerMap(self, board):
        print()
        for y in range(board._height+1):
            for x in range(board._width):
                print(int(self._dangerMap[y][x]), "", end='')
            print()
    def printSafetyMap(self, board):
        print()
        for y in range(board._height+1):
            for x in range(board._width):
                print(int(self._safetyMap[y][x]), "", end='')
            print()

    def didTowerConfigurationChange(self, board):
        newTowers = []
        for col in range(0, board._width):
            for row in range(0, board._height):
                tower = board._towers[row][col]
                if not (tower is None):
                    newTowers.append(tower)
        if self._towers != newTowers:
            self._towers = newTowers
            return True
        return False


def astar(unit, board):
    # Calculate danger
    # unit.calculateDanger(board)
    # unit.calculateSafety(board)
    # unit.printDangerMap(board)
    # unit.printSafetyMap(board)


    # print("({0},{1})".format(unit._lastNode[0], unit._lastNode[1]))
    start = (unit._lastNode[0], unit._lastNode[1], None, 0)
    # start = (int(unit._x+0.01), int(unit._y+0.01), None, 0) # (x, y, parent, g-score)
    goalY = board._height

    # Fix error where out of bounds (-1) + 0.05 is not the right value (expect -1, get 0)
    # if unit._lastNode[1] <= -0.99:
    #     start = (unit._lastNode[0], int(unit._lastNode[1]-0.02), None, 0)

    # print("Unit ({0},{1})".format(start[0], start[1]))
    # if board.hasTower(start[0], start[1]):
    #     print("Unit is on tower")

    closedNodes = []
    openNodes = []
    bestNode = None

    # Add initial node
    openNodes.append(start)

    # While the open list has nodes, remove the best node, check if at goal, generate neighbor nodes, 
    while openNodes:

        # Remove the best node
        bestNode = removeBestNode(board, openNodes, start, goalY)
        # print("Node ({0},{1}) = {2}".format(bestNode[0], bestNode[1], heuristic(bestNode, start, goalY)))

        # Add this node to list of already explored nodes
        closedNodes.append(bestNode)

        # Generate neighbor nodes and add unexplored nodes to open list
        for node in neighbors(unit, board, bestNode):
            # Ignore nodes that have already been explored
            matchingClosedNode = next((n for n in closedNodes if n[0] == node[0] and n[1] == node[1]), None)
            if matchingClosedNode:
                continue
            # Ignore nodes that contain a tower
            if board.hasTower(node[0], node[1]):
                continue
            # Check if neighbor is at goal
            if node[1] == goalY:
                pathForNode(unit, node, start)
                return
            # If the neighbor already exists in the open list, replace it only if the neighbor has a better heuristic value
            matchingOpenNode = next((n for n in openNodes if n[0] == node[0] and n[1] == node[1]), None)
            if matchingOpenNode:
                matchingIndex = openNodes.index(matchingOpenNode)
                if node[3] < matchingOpenNode[3]:
                    openNodes[matchingIndex] = node
            else:
                openNodes.append(node)

def pathForNode(unit, node, start):
    unit._path = [(node[0], node[1])]

    # Follow path backward to find next action to take
    tempNode = node
    while tempNode[2] != start:
        tempNode = tempNode[2]
        unit._path = [(tempNode[0], tempNode[1])] + unit._path

    # Get direction from next action
    unit._direction = directionFromNodes(start, tempNode)
    unit._nextNode = tempNode#unit._path[0]
    unit._path = unit._path[1:]

def directionFromNodes(start, next):
    if next[0] - start[0] > 0.5:
    # if next[0] > start[0]:
        return EAST
    if next[0] - start[0] < -0.5:
    # if next[0] < start[0]:
        return WEST
    if next[1] - start[1] > 0.5:
    # if next[1] > start[1]:
        return SOUTH
    if next[1] - start[1] < -0.5:
    # if next[1] < start[1]:
        return NORTH
    return STOP

def neighbors(unit, board, node):
    neighborNodes = []
    if node[0] > 0:
        neighborNodes.append((node[0]-1, node[1], node, node[3] + 1 + unit._dangerMap[node[1]][node[0]-1] - unit._safetyMap[node[1]][node[0]-1]))
    if node[0] < board._width-1:
        neighborNodes.append((node[0]+1, node[1], node, node[3] + 1 + unit._dangerMap[node[1]][node[0]+1] - unit._safetyMap[node[1]][node[0]+1]))
    if node[1] > 0:
        neighborNodes.append((node[0], node[1]-1, node, node[3] + 1 + unit._dangerMap[node[1]-1][node[0]] - unit._safetyMap[node[1]-1][node[0]]))
    if node[1] < board._height:
        neighborNodes.append((node[0], node[1]+1, node, node[3] + 1 + unit._dangerMap[node[1]+1][node[0]] - unit._safetyMap[node[1]+1][node[0]]))
    return neighborNodes

def removeBestNode(board, openNodes, start, goalY):
    bestScore = board._width * board._height * 100000
    bestNode = None
    for node in openNodes:
        score = heuristic(node, start, goalY)
        if score < bestScore:
            bestScore = score
            bestNode = node
    openNodes.remove(bestNode)
    return bestNode

def heuristic(node, start, goalY):
    return node[3] + distToGoal(node, goalY)

def distBetweenNodes(current, dest):
    return abs(current[0]-dest[0]) + abs(current[1]-dest[1])

def distToGoal(node, goalY):
    return goalY - node[1]
