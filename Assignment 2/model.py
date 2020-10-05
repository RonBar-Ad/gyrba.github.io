# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 11:51:27 2020

@author: Ron
"""

import agent
import random
import csv

def readEnvironmentFromFile(file):
    environment = []
    f = open(file, newline='')
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)
    return environment

def randomisePreferences(stores):
    for i in stores:
        pass

MAX_AGENTS = 100
MAX_MOVES = 20
MAX_NEIGHBOURS = 20
MAX_MONEY
environmentFileName = 'in.txt'
environment = []
agents = []
stores = []

environment = readEnvironmentFromFile(environmentFileName)
env_max = len(environment)
for i in range(MAX_AGENTS):
    try:
        init_y = int((env_max-1)*random.random())
        init_x = int((env_max-1)*random.random())
        preferences = randomisePreferences()
        agents.append(agent.Agent(init_y, init_x, preferences, stores, MAX_MONEY))
