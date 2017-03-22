
from random import randint
from board import BoardState
from unit_agent import *
from actions import *
from mongo_wrapper import MongoWrapper
from tower_agent import TowerAgent

def generateNewVector(vectors):
   newVector = []
   for i in range(0, len(vectors[0])):
      vector3.append(randint(0, len(vectors)))

def mutateVector(vector, mutationChance):
   newVector = []
   for i in range(0, len(vector)):
      if randint(0, 1/mutationChance) == 0:
         vector[i]

# class StaticUnitAgent:
# class StaticTowerAgent:

class Agent:
   def __init__(self, database):
      self.states = [] # (board state, tower placement region, score)

   def step(self, state):
      pass

# Unit State:
   # #units in region 1
   # #units in region 2
   # #units in region 3
   # #units in region 4

# Tower State:
   # #towers in region 1
   # #towers in region 2
   # #towers in region 3
   # #towers in region 4

# Game State:
   # step count
   # #units on board
   # #towers on board
   # Unit State
   # Tower State

      # First 1000 Games:
         # if 1 out of MaxFrames/MaxTowerCount == 0
         # Place tower and store state
            # when placing tower, use separate state (# units in each region) to choose location
            # choose randomly

      # After 1000 Games:
         # Get distance to nearest state
         # If distance < value and score > value2, then perform action associated with state (placement of tower)
         # else random chance (1 out of 100) to place tower anyway
         # When placing tower, use stored location + random variance (up to 2 blocks away)

   def gameOver(self, heuristic):
      for state in self.states:
         # store state in database with the heuristic score
         pass


# For training
   # init StaticUnitAgent
   # init TowerAgent
   # start game and get action from each agent every step
   # Each Step
      # Get current state from board
      # pass state to agent's step method
      # get action from agents
      # perform action
   # After 1000 steps, call gameover method on both agents










# class TowerAgent:
#    def __init__(self):
#       self._actionStates = []
#       self._lastBoardState = None
#
#    def step(self, board, stepCount):
#       state = board.getState()
#       if len(self._actionStates) < 10 and state != self._lastBoardState:
#          self._lastBoardState = state
#          if self.gamesPlayed >= 100:
#             return self.step2(board, stepCount)
#          else:
#             if randint(0, 50) == 0:
#                action = PlaceTowerAction(randint(0, 9), randint(0, 9))
#                while board.hasTower(action.x, action.y):
#                   action = PlaceTowerAction(randint(0, 9), randint(0, 9))
#                actionState = ActionState(stepCount, state, action, None)
#                self._actionStates.append(actionState)
#                return action
#       return NoAction()
#
#    def step2(self, board, stepCount):
#       state = board.getState()
#       nearestState = GetNearestState(state)
#       dist = state.normalizedDistToState(nearestState.boardState)
#       # print("Dist to nearest state: ", dist)
#       # print("Score of nearest state: ", nearestState.score)
#       if randint(0, 50) == 0:
#          action = PlaceTowerAction(randint(0, 9), randint(0, 9))
#          actionState = ActionState(stepCount, state, action, None)
#          self._actionStates.append(actionState)
#          return action
#       else:
#          if not (nearestState.action is NoAction):
#             if board.hasTower(nearestState.action.x, nearestState.action.y):
#                return NoAction()
#             actionState = ActionState(stepCount, state, nearestState.action, None)
#             self._actionStates.append(actionState)
#          return nearestState.action
#
#    def gameOver(self, score):
#       for actionState in self._actionStates:
#          actionState.score = score
#          # TODO: store action states in database
#          SaveState(actionState)

class Generator:
   def __init__(self):
      self.gamesPlayed = 0

   def init(self):
      # if self.gamesPlayed > 100:
      # self._unitAgent = RandomUnitAgent(10, 10, 1000)

      # self._unitAgent = StaticUnitAgent([
      #    ActionState(0, None, PlaceUnitAction(9), None),
      #    ActionState(75, None, PlaceUnitAction(9), None),
      #    ActionState(150, None, PlaceUnitAction(9), None),
      #    ActionState(225, None, PlaceUnitAction(9), None),
      #    ActionState(300, None, PlaceUnitAction(9), None),
      #    ActionState(375, None, PlaceUnitAction(9), None),
      #    ActionState(450, None, PlaceUnitAction(9), None),
      #    ActionState(525, None, PlaceUnitAction(9), None),
      #    ActionState(600, None, PlaceUnitAction(9), None),
      #    ActionState(675, None, PlaceUnitAction(9), None)
      # ])
      self._unitAgent = UnitAgent(10)
      # self._towerAgent = TowerAgent()
      self._towerAgent = TowerAgent(10)
      self._towerAgent.gamesPlayed = self.gamesPlayed

   def step(self, stepCount, board):
      boardState = board.getState()

      # board.execute(self._unitAgent.step(board, stepCount))
      # board.execute(self._towerAgent.step(board, boardState))
      self._unitAgent.step(board)
      self._towerAgent.step(board)

   def gameOver(self, board):
      score = board.getScore()
      # self._unitAgent.gameOver(score)
      self._unitAgent.gameOver(board)
      self._towerAgent.gameOver(board)
      # print(savedStates)
      print("Game {0} Finished (score = {1})".format(self.gamesPlayed, score))
      self.gamesPlayed += 1




