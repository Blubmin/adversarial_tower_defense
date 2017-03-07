
from random import randint

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

class State:
   def __init__(self, action, score):
      pass

class StaticUnitAgent
   def __init__(self, states):
      self.states = states
      self.nextState = 0

   def step(self, state):
      if state.step >= self.states[nextState]:
         return self.states[nextState].action






