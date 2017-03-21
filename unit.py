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
        self._health = 200
        self._shouldDestroy = False
        self._isAtGoal = False

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
            


def astar(unit, board):
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
        for node in neighbors(board, bestNode):
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

def neighbors(board, node):
    neighborNodes = []
    if node[0] > 0:
        neighborNodes.append((node[0]-1, node[1], node, node[3] + 1))
    if node[0] < board._width-1:
        neighborNodes.append((node[0]+1, node[1], node, node[3] + 1))
    if node[1] > 0:
        neighborNodes.append((node[0], node[1]-1, node, node[3] + 1))
    if node[1] < board._height:
        neighborNodes.append((node[0], node[1]+1, node, node[3] + 1))
    return neighborNodes

def removeBestNode(board, openNodes, start, goalY):
    bestScore = board._width * board._height
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
