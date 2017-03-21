
savedStates = []

def SaveState(actionState):
   # Find all states matching the given state that are already in the database
   matchingStates = list(state for state in savedStates if state.boardState == actionState.boardState)
   bestScore = actionState.score
   if matchingStates:
      # For each matching state
      for state in matchingStates:
         if bestScore > state.score:
            savedStates.remove(state)
         else:
            bestScore = state.score
   # Save the given state if it is better than any matching saved states
   if bestScore == actionState.score:
      savedStates.append(actionState)

def GetNearestState(boardState):
   # Sort states based on distance
   sortedStates = sorted(savedStates, key=lambda state: boardState.normalizedDistToState(state.boardState))
   # Sort closest 10 states based on score
   closestStates = sorted(sortedStates[0:10], key=lambda state: state.score)
   # Return best scoring of 10-closest states
   return closestStates[len(closestStates)-1]

def GetNearestUnitPlacementState(boardState):
   pass

class ActionState:
   def __init__(self, stepCount, boardState, action, score):
      self.stepCount = stepCount
      self.boardState = boardState
      self.action = action
      self.score = score

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
      