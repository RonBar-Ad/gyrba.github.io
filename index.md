#Ron Bar-Ad

Ron Bar-Ad is a PhD student with the Data Analytics Centre for Doctoral Training in Manchester, England. He has a BSc in Software Development, not that you should hold that against him, and he desperately loves talking about himself.



#GEOG5995M

##Assessment 1

###Overview<br>

This project consists of a model that emulates objects moving in an area and eating its contents. By eating, the agents take food from the map into their personal stores. If they eat too much, they throw up.

At the end of each round, the agents share what food they have with their neighbours. Agents with much less food than their neighbours will steal food, ending up with more than an even share.

Some agents are cannibals, and at the end of each round they will eat a neighbour. Cannibals also get all the food the neighbour had eaten, but will share their food like everyone else.


###The Code

The code comes in two parts: [the model](https://github.com/RonBar-Ad/gyrba.github.io/blob/master/model.py) and [the agent framework](https://github.com/RonBar-Ad/gyrba.github.io/blob/master/agentframework.py)

You should also download the [input text file](href="https://github.com/RonBar-Ad/gyrba.github.io/blob/master/in.txt) and store it in the same folder under the name "in.txt".