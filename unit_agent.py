import pygame

from math import sqrt
from random import randint
from unit import Unit
from actions import *

# class UnitAgent:
#     def __init__(self, maxUnits):
#         self._units = []
#         self._maxUnits = maxUnits

#     def init(self, board):
#         self._units = []
#         self._placementDelay = 0
#         self._score = 0
#         for i in range(0, self._maxUnits):
#             self.placeUnit(board)

#     def step(self, board):
#         # self._placementDelay -= 1
#         # self.placeUnit(board)
#         for unit in self._units:
#             if unit._shouldDestroy:
#                 self._units.remove(unit)
#             elif unit._isAtGoal:
#                 self._score += 1
#                 self._units.remove(unit)
#             else:
#                 unit.step(board)
#                 # unit._y += 0.05
#         if self._units:
#             print()

#     def placeUnit(self, board):
#         # if self._placementDelay <= 0:
#         #     self._placementDelay = randint(10, 100)
#             unit = Unit(randint(0, board._width - 1), -1)
#             self._units.append(unit)
#             board.add_unit(unit)

#     def render(self, screen, xCoord, yCoord):
#         myfont = pygame.font.SysFont("monospace", 15)
#         label = myfont.render("Unit Score: {0}".format(self._score), 1, (255,255,0))
#         screen.blit(label, (xCoord, yCoord))


class StaticUnitAgent:
    def __init__(self, actionStates):
        self._actionStates = actionStates
        self._nextStateIndex = 0

    def step(self, board, stepCount):
        # If there is still a state that needs to be executed
        if self._nextStateIndex < len(self._actionStates):
            nextState = self._actionStates[self._nextStateIndex]
            # If the state should be executed
            if self._actionStates[self._nextStateIndex].stepCount <= stepCount:
                self._nextStateIndex += 1
                # Execute the action associated with the state
                return nextState.action
        return NoAction()

    def gameOver(self, score):
        pass

class RandomUnitAgent:
    def __init__(self, boardWidth, maxUnits, maxSteps):
        self._actionStates = []
        self._placementTriggers = []
        self._maxUnits = maxUnits
        # Generate random states for when to place units
        for i in range(0, self._maxUnits):
            time = randint(0, maxSteps-100)
            posX = randint(0, boardWidth-1)
            self._placementTriggers.append((time, posX))
        self._placementTriggers = sorted(self._placementTriggers, key=lambda student: student[0])

    def step(self, board, stepCount):
        # If maximum number of units has not been reached
        unitsPlaced = len(self._actionStates)
        if unitsPlaced < self._maxUnits:
            # If the step is less than the next placement trigger, place a unit
            if self._placementTriggers[unitsPlaced][0] <= stepCount:
                action = PlaceUnitAction(self._placementTriggers[unitsPlaced][1])
                actionState = ActionState(board.getState(), action, None)
                self._actionStates.append(actionState)
        return NoAction()

    def gameOver(self, score):
        for actionState in self._actionStates:
            actionState.score = score
            SaveState(actionState)


class SmartUnitAgent:
    def __init__(self, board, maxUnits, maxSteps):
        self._actionStates = []
        self._maxUnits = maxUnits

    def step(self, board, stepCount):
        # If maximum number of units has not been reached
        unitsPlaced = len(self._actionStates)
        if unitsPlaced < self._maxUnits:
            # If the step is less than the next placement trigger, place a unit
            if self._placementTriggers[unitsPlaced][0] <= stepCount:
                action = PlaceUnitAction(self._placementTriggers[unitsPlaced][1])
                actionState = ActionState(board.getState(), action, None)
                self._actionStates.append(actionState)
        return NoAction()

    def gameOver(self, score):
        for actionState in self._actionStates:
            actionState.score = score
            SaveState(actionState)

