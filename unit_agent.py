import pygame

from unit import Unit

class UnitAgent:
   def init(self, board):
      board.addUnit(Unit(3, 4))
   def step(self, board):
      pass
   def render(self):
      pass