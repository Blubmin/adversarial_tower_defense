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
        self._nextNode = None
        self._health = 300
        self._shouldDestroy = False
        self._isAtGoal = False
        self._dangerMap = [[0 for x in range(10)] for x in range(11)]

    def setShouldDestroy(self):
        self._shouldDestroy = True

    def setIsAtGoal(self):
        self._isAtGoal = True

    def damage(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._shouldDestroy = True

    def step(self, board):
        # If at next node in astar, recompute astar
        if self.isAtNextNode(board) or not self._nextNode:
            astar(self, board)
        # Move in direction
        if self._direction == NORTH:
            self._y -= self._speed
        elif self._direction == EAST:
            self._x += self._speed
        elif self._direction == SOUTH:
            self._y += self._speed
        elif self._direction == WEST:
            self._x -= self._speed

    def isAtNextNode(self, board):
        if self._direction == NORTH:
            if self._y <= self._nextNode[1]+0.01:
                return True
        elif self._direction == EAST:
            if self._x >= self._nextNode[0]-0.01:
                return True
        elif self._direction == SOUTH:
            if self._y >= self._nextNode[1]-0.01:
                return True
        elif self._direction == WEST:
            if self._x <= self._nextNode[0]+0.01:
                return True
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
    def printDangerMap(self, board):
        print()
        for y in range(board._height+1):
            for x in range(board._width):
                print(int(self._dangerMap[y][x]), "", end='')
            print()
            
# danger = [[0 for x in range(10)] for x in range(11)]
# def calculateDanger(board):
#     # Reset danger map to all 0s
#     danger2 = [[0 for x in range(board._width)] for x in range(board._height+1)]
#     towerRange = 2
#     towerRangeSquared = towerRange * towerRange
#     # Find all towers on the board
#     for y in range(board._height):
#         for x in range(board._width):
#             # For each tower, add 1 danger to all cells within its range
#             if board._towers[y][x]:
#                 print("Found Tower")
#                 for dy in range(max(0, y-towerRange), min(y+towerRange, board._height)):
#                     for dx in range(max(0, x-towerRange), min(x+towerRange, board._width-1)):
#                         # If cell is within tower range
#                         if pow(y-dy, 2) + pow(x-dx, 2) < towerRangeSquared:
#                             danger2[dy][dx] += 1
#                             print(danger2[dy][dx])
#     danger = danger2
# def printDangerMap(board):
#     for y in range(board._height+1):
#         for x in range(board._width):
#             print(danger[y][x], "", end='')
#         print()


def astar(unit, board):
    # Calculate danger
    # unit.calculateDanger(board)
    # unit.printDangerMap(board)


    # print("({0},{1})".format(unit._x, unit._y))
    start = (int(unit._x+0.01), int(unit._y+0.01), None, 0) # (x, y, parent, g-score)
    goalY = board._height

    # Fix error where out of bounds (-1) + 0.05 is not the right value (expect -1, get 0)
    if unit._y == -1:
        start = (int(unit._x+0.01), int(unit._y-0.01), None, 0)

    # print("Unit ({0},{1})".format(start[0], start[1]))
    if board.hasTower(start[0], start[1]):
        print("Unit is on tower")

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
    # Follow path backward to find next action to take
    tempNode = node
    while tempNode[2] != start:
        tempNode = tempNode[2]

    # Get direction from next action
    unit._direction = directionFromNodes(start, tempNode)
    unit._nextNode = (tempNode[0], tempNode[1])

def directionFromNodes(start, next):
    if next[0] > start[0]:
        return EAST
    if next[0] < start[0]:
        return WEST
    if next[1] > start[1]:
        return SOUTH
    if next[1] < start[1]:
        return NORTH
    return STOP

def neighbors(unit, board, node):
    neighborNodes = []
    if node[0] > 0:
        neighborNodes.append((node[0]-1, node[1], node, node[3] + 1 + unit._dangerMap[node[1]][node[0]-1]))
    if node[0] < board._width-1:
        neighborNodes.append((node[0]+1, node[1], node, node[3] + 1 + unit._dangerMap[node[1]][node[0]+1]))
    if node[1] > 0:
        neighborNodes.append((node[0], node[1]-1, node, node[3] + 1 + unit._dangerMap[node[1]-1][node[0]]))
    if node[1] < board._height:
        neighborNodes.append((node[0], node[1]+1, node, node[3] + 1 + unit._dangerMap[node[1]+1][node[0]]))
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
