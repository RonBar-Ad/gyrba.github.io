# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 09:40:47 2020

@author: Ron
""" 


"""
NOTE: Please ensure your iPython graphics is set to Tkinter
      After running the program, allow up to 10 seconds for it to load
      When closing the program, please use the "quit" button and not the window's inbuilt X


This program generates a map, on which every point contains some amount of "food"
Some number of agents is generated, each agent capable of moving, eating and sharing
Eating takes food out of the map and stores it in the agent, leaving a pleasing trail of where each agent has eaten
Eat too much, and they throw up their stores back onto whatever point they're standing on
Sharing takes the total of any nearby agents' stores and divides them equally between them

Some agents are cannibals, who can eat other agents
In doing so, they absorb their stores and remove them from the game
Cannibals can also be eaten by cannibals, though, and can also throw up if they eat too much

Agents are in blue
Cannibals are in green
The northmost and eastmost agents (cannibal or not) are red
"""




'''---------------------------IMPORTS'''

import agentframework #for Agent objects
import random # for random coordinates (see agent-initialising below)
import tkinter #for our GUI
from tkinter import Button # for our GUI
import matplotlib # for our map
matplotlib.use('TkAgg') # defining our GUI backend
import matplotlib.pyplot # for plotting our agents
import matplotlib.animation # for showing movement
import csv # for reading and writing our environment to/from files
import requests # for reading in our starting coordinates from a website
from bs4 import BeautifulSoup # for parsing our coordinates html file



'''---------------------------METHODS'''

    

# inputs: x and y coordinates of 2 agents
# process: calculate direct distance w/ pythagoras theorem
# output: distance between two agents
def distance(y1, x1, y2, x2):
    y = 0
    x = 0
    # determine the larger of each coordinate and subtract the smaller from it
    if y1 > y2:
        y = (y1-y2)**2
    else:
        y = (y2-y1)**2
    if x1 > x2:
        x = (x1-x2)**2
    else:
        x = (x2-x1)**2
    
    # returning our distance by sqr rooting a^2 + b^2
    return (y+x)**-1

# input: name of file to read
# process: read file into 2d list word by word
# output: 2d list
def readEnvironmentFromFile(file):
    environment = []
    f = open(file, newline='')
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    # Creating a list with each value of a row, then adding it to a list of rowlists
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)
    return environment


# used in animation() to limit the number of iterations to MAX_MOVES
def dataGen():
    a = 0
    # the other condition of the main program loop
    global carry_on
    # iterating only up to MAX_MOVES
    while a < MAX_MOVES and carry_on:
        # returns a as it is now, then when the function is called again picks up where a was before
        yield a
        a += 1

# tallies all the food still on the map to evaluate if there is any food left
def checkFood(environment):
    total_food = 0
    i = 0
    while total_food == 0 and i < len(environment):
        for j in range(0, len(environment[i])):
            total_food += environment[i][j]
            if total_food > 0:
                return True
        i += 1
        
        return False

# input: iteration of animation we are currently in
# process: shuffles agents life, then moves the agents, has them eat, then has them share
def update(frame_number):
    fig.clear() # clear the screen completely
    # defining our global from dataGen()
    global carry_on

    # Shuffling agents, this way they don't always go in the same order
    random.shuffle(agents)
     
    # every turn, the agents move up to 1 space,
    #   eat up to 10 points
    #   share food with their neighbours
    #   steal from neighbours who have more than them
    # cannibals also eat 1 neighbour a turn
    for j in agents:
        j.move()
        j.eat()
        j.share_with_neighbours(MAX_NEIGHBOURS)
        j.steal_from_neighbours(MAX_NEIGHBOURS)
        j.eat_neighbour(MAX_NEIGHBOURS)
    
    # the dead agents are removed from the field
    bringOutYourDead(agents)
    # if there is food left on the map, we continue
    carry_on = checkFood(environment)
    # showing the environment map
    matplotlib.pyplot.imshow(environment)
    # showing our agents on the environment
    plotAgents(agents, len(environment))

# process: plots each agent on our graph
def plotAgents(agents, environment_size):
    
    # We find the furthest agents east and north
    eastmost = getHighestX(agents)
    # the y axis is inverted, so we work from max instead of from 0
    northmost = getLowestY(agents, environment_size)
    
    
    for i in agents:
        # the northmost and eastmost agents are plotted in red
        if agents.index(i) == eastmost or agents.index(i) == northmost:
            matplotlib.pyplot.scatter(i.get_x(), i.get_y(), color='red')
        # cannibals are plotted in yellow
        elif i.get_cannibal():
            matplotlib.pyplot.scatter(i.get_x(), i.get_y(), color='yellow')
        # all other agents are plotted in blue
        else:
            matplotlib.pyplot.scatter(i.get_x(), i.get_y(), color='blue')

# iterates through the list to find the agent whose Y coordinate is lowest
# lowest because the Y axis is flipped in our graph
# here, "top" is the maximum value on the Y axis
def getLowestY(agents, top):
    winner = 0
    lowest = top
    for i in agents:
        if i.get_y() < lowest:
            winner = agents.index(i)
            lowest = i.get_y()
    return winner # we only return the winner, in theory we could return just
                  # their ID, but this saves us some space and doesn't slow us down too much

# iterates through the list to find the agent whose X coordinate is highest
def getHighestX(agents):
    winner = 0
    highest = 0
    for i in agents:
        if i.get_x() > highest:
            winner = agents.index(i)
            highest = i.get_x()
    return winner # we only return the winner. We could just return the ID


# destroys any agents who have been eaten by a cannibal and removes them from
# the list of agents
def bringOutYourDead(agents):
    for i in reversed(agents): # reversed so we don't skip any items as we remove them
        if not(i.get_life_signs()):
            agents.remove(i)
            del i

# generates our animation and draws it on our tkinter window
def run():
    # here fig is our graph, update is our turn function, frames keeps track of how many iterations we've had
    # and we don't repeat the animation once it's ended
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=dataGen, repeat=False)
    canvas.draw()

# to find the values in the coordinates list
# this is so the getMultiplicator function can find our multiplicator
def getHighestValueOnOneAxis(values):
    highest = 0
    for i in values:
        if int(i.text) > highest:
            highest = int(i.text)
    return highest # returning the highest coordinate as an integer
            
# this method finds a multiplicator for our starting coordinates:
# if the starting coordinates are in a different from our environment,
#     (e.g. agents only spawn within the first 100x100 coordinates, but
#     environment goes all the way to 300)
# then our multiplicator will be used to change the values to fit our environment.
def getMultiplicator(env_max, yValues, xValues):
    # here env_max is the highest Y coordinate possible in our map
    # this method assumes the map has an equal Y and X axis
    # if they're unequal, create an env_max_x variable for X axis comparison
    
    # finding our highest X and Y values for comparison
    highestY = getHighestValueOnOneAxis(yValues)
    highestX = getHighestValueOnOneAxis(xValues)
    
    # finding our Y-axis multiplicator
    # dividing whichever value is larger by the other
    if env_max > highestY:
        ydiv = env_max/highestY
    elif highestY > env_max:
        ydiv = highestY/env_max
    else:
        ydiv = 1
    
    # finding our X-axis multiplicator
    # dividing whichever value is larger by the other
    if env_max > highestX:
        xdiv = env_max/highestX
    elif highestX > env_max:
        xdiv = highestX/env_max
    else:
        xdiv = 1
        
    # returning them in order Y,X
    return ydiv, xdiv

# for the "quit" button
# this allows the program to end, quitting by
# closing the window will leave the programme running in the background
def bye():
    root.quit()
    root.destroy()

# writes the environment row by row into a csv (comma separated) file
def writeEnvironmentToFile(environment):
    file = open('out.csv', 'w', newline='')
    # we imported csv for this
    writer = csv.writer(file, delimiter=',')
    for row in environment:
        writer.writerow(row)
    file.close()

# writes the total stores of all agents into a text file
def writeStoreToFile(agents):
    file = open('stores.txt', 'a', newline='')
    stores = 0
    for i in agents:
        # stores is a float, we want it simple so we int it
        stores += int(i.get_store())
    # we want to store stores as text so we string it
    stores = str(stores) + "\n" # we also add a \n so the next call of this function will be to a new line
    file.write(stores)
    file.close()



'''---------------------------GLOBAL CONSTANTS'''


# total number of agent objects to be created
MAX_AGENTS = 100
# total number of iterations (how many times we run the update() method)
MAX_MOVES = 20
# number of agents that count as "neighbours", for agents to share food with or steal from (or eat)
MAX_NEIGHBOURS = 20
# the file we take our environment array from
environmentFileName = 'in.txt'
# the site we take our starting coordinates from
agentInitiationFileLocation = "https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html"
# 2d int array that holds our food for every cell on the graph
environment = []
# contains our agentframework objects
agents = []

# creates a graph object to be held in the tkinter window
fig = matplotlib.pyplot.figure(figsize=(7,7))
# the axes on the tkinter window
ax = fig.add_axes([0,0,1,1])
# the global boolean for the stopping condition
carry_on = True


'''---------------------------MAIN PROGRAMME'''
        
# environment initialised
environment = readEnvironmentFromFile(environmentFileName)
# an int of the highest possible Y coordinate
env_max = len(environment)

# using the requests module to get our starting coordinates from the website
# NOTE: NOT VERIFYING CERTIFICATE IS DANGEROUS AND INSECURE.
# It's necessary to connect to the site, but change it if you ever use this program for a purpose other than testing.
r = requests.get(agentInitiationFileLocation, verify=False)
content = r.text # converting the page into an html string
soup = BeautifulSoup(content, 'html.parser') # an html string parser object
yValues = soup.find_all(attrs={"class":"y"}) # getting only the values for y coordinates
xValues = soup.find_all(attrs={"class":"x"}) # getting only the values for x coordinates

# the multiplicator for our starting coordinates, in case they aren't
# using our full environment
div = getMultiplicator(env_max, yValues, xValues)


# Initiating our agents
for i in range(MAX_AGENTS):
    # the try-except makes sure we have enough agents regardless of how many starting coordinates
    # the website included
    try:
        init_y = int(yValues[i].text) # our y coordinate from the website
        # we only mutliply by div if the initial value is too small
        # this is because we know the website's values are too small
        # a more robust system would have cases for too-large values as well
        if init_y < 100: init_y *= div[0]
        init_x = int(xValues[i].text) # our x coordinate from the site
        # again, only multiply if it's too small
        if init_x < 100: init_x *= div[1]
        # create an Agent object and add it to the list
        agents.append(agentframework.Agent(init_y, init_x, environment, agents, random.random()))
        # note the random final variable, to determine cannibalism
    # if we run out of online coordinates
    except IndexError:
        # initialising our y and x as random variables within the confines of the map
        init_y = int((env_max-1)*random.random())
        init_x = int((env_max-1)*random.random())
        # creating an Agent object and adding it to the list
        agents.append(agentframework.Agent(init_y, init_x, environment, agents, random.random())) 

# creating our Tkinter window
root = tkinter.Tk()
root.wm_title("Model") # same name as this py file
# our button to begin the animation loop and start the program
Button(root, text="Run", command=run).pack()
# the button to close the program safely and completely
Button(root, text="Quit", command=bye).pack()
# here we create a graph in a tkinter window by using matplotlib's tkinter backend
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
# and pack the canvas to the top of the screen
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# the mainloop that keeps the tkinter window open
tkinter.mainloop()

# exporting our results
writeEnvironmentToFile(environment)
writeStoreToFile(agents)


'''---------------------------GLOBAL CONSTANTS'''