import pygame

from tower import Tower

class TowerAgent:
   def __init__(self):
      self._towers = []

   def init(self, board):
      board.addTower(Tower(1, 1))

   def step(self, board):
      pass
      
   def render(self):
      pass
