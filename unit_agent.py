import pygame

from math import sqrt
from random import randint
from unit import Unit
from actions import *

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
            time = randint(0, maxSteps-300)
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
                actionState = ActionState(stepCount, board.getState(), action, None)
                self._actionStates.append(actionState)
                return action
        return NoAction()

    def gameOver(self, score):
        for actionState in self._actionStates:
            actionState.score = score
            # SaveState(actionState)


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
                actionState = ActionState(stepCount, board.getState(), action, None)
                self._actionStates.append(actionState)
        return NoAction()

    def gameOver(self, score):
        for actionState in self._actionStates:
            actionState.score = score
            SaveState(actionState)




# Unit types
# Unit behaviors
# shortest path
# avoid towers
# group together

# Try implementing flocking-type behavior






