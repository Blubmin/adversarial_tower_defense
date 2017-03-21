
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
      