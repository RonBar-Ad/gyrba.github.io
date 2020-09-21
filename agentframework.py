# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 14:53:59 2020

@author: Ron
"""

import random
import math

# The Agent class:
# Variables: y and x (coordinates)
# Methods: move and get for each variable
class Agent:
   def __init__(self, y, x, environment, agents, cannibal):
       self.y = y
       self.x = x
       self.environment = environment
       self.agents = agents
       self.cannibal = True if cannibal < 0.2 else False
       self.alive = True
       self.store = 0
       
       


   def __str__(self):
       string = "ID: " + str(self.agents.index(self)) + " Y: " + str(self.y) + " X: " + str(self.x) + " store: " + str(self.store)
       return string
       
   # get_y and get_x act to retrieve
   # the values of the y and x coordinates
   def get_y(self):
       return self.y
   
   def get_x(self):
       return self.x
   
   def get_store(self):
        return self.store
    
   def set_store(self, store):
       self.store = store
       
   def get_cannibal(self):
       return self.cannibal

   def get_life_signs(self):
       return self.alive
   
   def die(self):
       self.alive = False

   def move(self):
       random_y = random.random()
       random_x = random.random()
       if random_y > 0.5 and self.y < len(self.environment)-2:
           self.y += 1
       elif random_y < 0.5 and self.y > 0:
           self.y -= 1
       if random_x > 0.5 and self.x < len(self.environment)-2:
           self.x += 1
       elif random_x < 0.5 and self.x > 0:
           self.x -= 1
    
   def eat(self):
       y = int(self.y)
       x = int(self.x)
       try:
           elements = self.environment[y][x]
       except IndexError:
           elements = 0
       if elements > 10:
           self.store += 10
           self.environment[y][x] -= 10
       elif elements > 0:
           self.store += elements
           self.environment[y][x] -= elements
           
       if self.store > 100:
           self.environment[y][x] += (self.store /2)
           self.store = self.store / 2

   def distance_between(self, agent):
       y = 0
       x = 0
       other = self.agents[agent]
       if self.y > other.get_y():
           y = (self.y - other.get_y()) ** 2
       else:
           y = (other.get_y() - self.y) ** 2
       if self.x > other.get_x():
           x = (self.x - other.get_x()) ** 2
       else:
           x = (other.get_x() - self.x) ** 2
       return math.sqrt(y+x)
   
   def share_with_neighbours(self, neighbours):
       for i in range(neighbours):
           if i != self.agents.index(self):
               try:
                   distance = self.distance_between(i)
               except IndexError:
                   distance = neighbours+1
               if distance <= neighbours:
                   total = self.store + self.agents[i].store
                   self.store = total/2
                   self.agents[i].set_store(total/2)
                   #print("sharing " + str(distance) + " " + str(total/2))
              
   def steal_from_neighbours(self, neighbours):
       for i in range(neighbours):
           if i != self.agents.index(self):
               distance = self.distance_between(i)
               if (distance <= neighbours) and (self.agents[i].get_store() - self.store > 20):
                   self.store += self.agents[i].get_store() / 2
                   self.agents[i].set_store(self.agents[i].get_store() / 2)
                   
   def eat_neighbour(self, neighbours):
       full = False
       i = 0
       while (full == False and i < neighbours):
           if i != self.agents.index(self) and self.agents[i].get_life_signs():
               distance = self.distance_between(i)
               if distance <= neighbours and self.cannibal:
                   self.store += self.agents[i].get_store()
                   self.agents[i].die()
                   full = True
           i += 1