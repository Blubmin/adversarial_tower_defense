
from random import randint
from board import BoardState

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

class NoAction:
   def __init__(self):
      self.name = "NoAction"
class PlaceTowerAction:
   def __init__(self, x, y):
      self.name = "PlaceTowerAction"
      self.x = x
      self.y = y
class PlaceUnitAction:
   def __init__(self, x):
      self.name = "PlaceUnitAction"
      self.x = x


class ActionState:
   def __init__(self, boardState, action, score):
      self.boardState = boardState
      self.action = action
      self.score = score


class StaticUnitAgent:
   def __init__(self, actionStates):
      self._actionStates = actionStates
      self._nextStateIndex = 0

   def step(self, state):
      # If there is still a state that needs to be executed
      if self._nextStateIndex < len(self._actionStates):
         nextState = self._actionStates[self._nextStateIndex]
         # If the state should be executed
         if state.stepCount >= self._actionStates[self._nextStateIndex].boardState.stepCount:
            self._nextStateIndex += 1
            # Execute the action associated with the state
            return nextState.action
      return NoAction()

   def gameOver(self, score):
      pass

class TowerAgent:
   def __init__(self):
      self._actionStates = []

   def step(self, state):
      if len(self._actionStates) < 10:
         if randint(0, 100) == 0:
            action = PlaceTowerAction(randint(0, 9), randint(0, 9)) 
            actionState = ActionState(state, action, None)
            self._actionStates.append(actionState)
            return action
      return NoAction()

   def gameOver(self, score):
      for actionState in self._actionStates:
         actionState.score = score
      # TODO: store action states in database

class Generator:
   def __init__(self):
      self._unitAgent = StaticUnitAgent([
         ActionState(BoardState(10, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(50, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(100, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(150, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(200, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(250, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(300, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(350, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(400, 0, 0), PlaceUnitAction(randint(0, 9)), None),
         ActionState(BoardState(450, 0, 0), PlaceUnitAction(randint(0, 9)), None)
      ])

   def init(self):
      self._unitAgent._nextStateIndex = 0
      self._towerAgent = TowerAgent()

   def step(self, stepCount, board):
      boardState = board.getState(stepCount)
      boardState.stepCount = stepCount

      board.execute(self._unitAgent.step(boardState))
      board.execute(self._towerAgent.step(boardState))

   def gameOver(self, board):
      score = board.getScore()
      self._unitAgent.gameOver(score)
      self._towerAgent.gameOver(score)




