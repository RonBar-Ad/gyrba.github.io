# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 11:45:24 2020

@author: Ron
"""

class Agent:
    def __init__(self, y, x, pref, stores, money):
        self.y = y
        self.x = x
        self.preferences = pref
        self.stores = stores
        self.money = money
    
    def getY(self):
        return self.y
    def setY(self, y):
        self.y = y
    
    def getX(self):
        return self.x
    def getY(self, x):
        self.x = x
    
    """
    def getPreferences(self):
        return self.preferences
    def setPreferences(self, pref):
        self.preferences = pref
    """
    
    def getMoney(self):
        return self.money
    def setMoney(self, money):
        self.money = money
        
    