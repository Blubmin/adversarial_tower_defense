import pygame

from math import sqrt
from random import randint, randrange, choice
from unit import Unit
from actions import *
from mongo_wrapper import MongoWrapper

# place random
# place right of last unit
# place left of last unit
# place same as last unit
# place random right side
# place random left side
# place heavy and slow ditto
# place fast and light ditto

class UnitAgent:
    def __init__(self, maxUnits):
        self._maxUnits = maxUnits
        self._actions = ["place_randomly",
                         "place_randomly_right_side",
                         "place_randomly_left_side",
                         "place_same_as_last_unit",
                         "place_left_of_last_unit",
                         "place_right_of_last_unit"] # Same methods but with heavy and light units
        self._actions_taken = []

    def init(self, board):
        for i in range(0, self._maxUnits):
            self.placeUnit(board)

    def step(self, board):
        rand = randrange(0, 50)
        return (self.placeUnit(board) if rand is 1 else None)

    def placeUnit(self, board):
        if board._num_units >= 10:
            return None
        unit_data = MongoWrapper().get_unit_data()
        # for data in unit_data:
        #     print(data)

        count = board._num_units
        if board._last_unit is None:
            action = "place_randomly"
        else:
            action = choice(self._actions) # Picks a random action
        while not getattr(self, action)(board): # Performs the action
            action = choice(self._actions)
        self._actions_taken += [(board.getState(), action)] # Keeps track of actions taken in this game
        return action

    def gameOver(self, board):
        unit_data = map( lambda x: {"state": x[0].__dict__, "action": x[1], "score": board.getScore()}, self._actions_taken)
        MongoWrapper().save_unit_data(unit_data)

    def place_x(self, board, x):
        unit = Unit(x, -1, randint(0, 2))
        return board.add_unit(unit)
    def place_x_of_last_unit(self, board, x):
        if board._last_unit is None:
            return False
        unit = Unit(board._last_unit_initial_location[0] + x, -1, randint(0, 2))
        return board.add_unit(unit)

    def place_same_as_last_unit(self, board):
        return self.place_x_of_last_unit(board, 0)
    def place_left_of_last_unit(self, board):
        return self.place_x_of_last_unit(board, -1)
    def place_right_of_last_unit(self, board):
        return self.place_x_of_last_unit(board, 1)

    def place_randomly(self, board):
        return self.place_x(board, randint(0, board._width-1))
    def place_randomly_right_side(self, board):
        return self.place_x(board, randint(board._width/2, board._width-1))
    def place_randomly_left_side(self, board):
        return self.place_x(board, randint(0, board._width/2-1))

class StaticUnitAgent(UnitAgent):
    def __init__(self, actions_taken, maxUnits):
        super().__init__(maxUnits)
        self._actions_taken = actions_taken

    def init(self):
        pass

    def step(self, board):
        if board._num_units >= 10:
            return None
        for action_taken in self._actions_taken:
            if board.getState().normalizedDistToState(action_taken[0]) < 0.5:
                return action_taken[1]

    def gameOver(self, board):
        pass

    def place_x(self, board, x):
        return super().place_x(board, x)
    def place_x_of_last_unit(self, board, x):
        return super().place_x_of_last_unit(board, x)

    def place_same_as_last_unit(self, board):
        return super().place_same_as_last_unit(board)
    def place_left_of_last_unit(self, board):
        return super().place_left_of_last_unit(board)
    def place_right_of_last_unit(self, board):
        return super().place_right_of_last_unit(board)

    def place_randomly(self, board):
        return super().place_randomly(board)
    def place_randomly_right_side(self, board):
        return super().place_randomly_right_side(board)
    def place_randomly_left_side(self, board):
        return super().place_randomly_left_side(board)

# class StaticUnitAgent:
#     def __init__(self, actionStates):
#         self._actionStates = actionStates
#         self._nextStateIndex = 0

#     def step(self, board, stepCount):
#         # If there is still a state that needs to be executed
#         if self._nextStateIndex < len(self._actionStates):
#             nextState = self._actionStates[self._nextStateIndex]
#             # If the state should be executed
#             if self._actionStates[self._nextStateIndex].stepCount <= stepCount:
#                 self._nextStateIndex += 1
#                 # Execute the action associated with the state
#                 return nextState.action
#         return NoAction()

#     def gameOver(self, score):
#         pass

# class RandomUnitAgent:
#     def __init__(self, boardWidth, maxUnits, maxSteps):
#         self._actionStates = []
#         self._placementTriggers = []
#         self._maxUnits = maxUnits
#         # Generate random states for when to place units
#         for i in range(0, self._maxUnits):
#             time = randint(0, maxSteps-300)
#             posX = randint(0, boardWidth-1)
#             self._placementTriggers.append((time, posX))
#         self._placementTriggers = sorted(self._placementTriggers, key=lambda student: student[0])

#     def step(self, board, stepCount):
#         # If maximum number of units has not been reached
#         unitsPlaced = len(self._actionStates)
#         if unitsPlaced < self._maxUnits:
#             # If the step is less than the next placement trigger, place a unit
#             if self._placementTriggers[unitsPlaced][0] <= stepCount:
#                 action = PlaceUnitAction(self._placementTriggers[unitsPlaced][1])
#                 actionState = ActionState(stepCount, board.getState(), action, None)
#                 self._actionStates.append(actionState)
#                 return action
#         return NoAction()

#     def gameOver(self, score):
#         for actionState in self._actionStates:
#             actionState.score = score
#             # SaveState(actionState)


# class SmartUnitAgent:
#     def __init__(self, board, maxUnits, maxSteps):
#         self._actionStates = []
#         self._maxUnits = maxUnits

#     def step(self, board, stepCount):
#         # If maximum number of units has not been reached
#         unitsPlaced = len(self._actionStates)
#         if unitsPlaced < self._maxUnits:
#             # If the step is less than the next placement trigger, place a unit
#             if self._placementTriggers[unitsPlaced][0] <= stepCount:
#                 action = PlaceUnitAction(self._placementTriggers[unitsPlaced][1])
#                 actionState = ActionState(stepCount, board.getState(), action, None)
#                 self._actionStates.append(actionState)
#         return NoAction()

#     def gameOver(self, score):
#         for actionState in self._actionStates:
#             actionState.score = score
#             SaveState(actionState)




# Unit types
# Unit behaviors
# shortest path
# avoid towers
# group together

# Try implementing flocking-type behavior






