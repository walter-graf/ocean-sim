# An Ecological Simulation
## Introduction
Recently I stumbled across a 30 year old C++ workbook by Richard S.
Wiener and Lewis J. Pinson (from 1990). Although the workbook was referring to a
pretty old version of the language it gave a good introduction on OOP. 
In one chapter it covered a lively example of OOP in the form of an
ecological simulation. Instead of implementing this example in a current
version of C++ I chose to convert it to Python which helped me gaining
a better understanding of both OOP concepts and Python. In particular
the C++ implementation made explicit use of pointers, a concept not
available in Python (at least not in this explicit form). In addition
the general differences between a declarative compiler language like C++
and a more loose interpreter language like Python made me thoroughly
think about the right implementation. Being only an occasional
programmer, it was a good exercise to get to know Python better.
## The Ecological Simulation
The program represents an ecological system consisting of an ocean
containing prey, predators, and obstacles. It simulates interactions
among the ocean objects based on a set of rules. It illustrates the use
of OOP including derived classes.
### General Simulation Rules
The ecological simulation takes place in an ocean where
- The obstacles are stable and do not move; they block movement by
other objects in the ocean
- A predator may also be prey to other predators. Therefore, a predator
is a special kind of prey. In the initial simulation predators attack
only prey.
- Both Prey and predators move
- The simulation provides dependent mechanisms for increasing and 
depleting the number of prey and predators.
- Both prey and predators reproduce in random intervals. Thus, each
can increase in numbers.
- Prey die when eaten by a predator
- Predators die if they do not feed within a specified time interval.
### Primary Objects and Class Hierarchy
The following classes exist:
- **Ocean**: An ocean consists of a two-dimensional array of cells
- **Cell**: A cell is an abstract object that is normally empty (can be
perceived as water). Its subclasses represent various kinds of objects
that may be in the ocean. A cell must know what ocean it is contained
within. The ocean will be the same for all cells in a simulation.
  - **Prey**: A prey is a kind of cell. It can move. It can reproduce
  only when it has moved and when its time to reproduce has reached zero
    - **Predator**: A predator is a kind of prey. It can move. It
    prefers to move and eat a neighour prey. It will move to an empty
    cell if no prey is available. In this initial design, a predator 
    will not attack a neighbouring predator. It can reproduce if it
    moves and its time to reproduce is equal or less than 0, it will die
    if it does not eat within a specified time
  - **Obstacle**: An obstacle is a kind of cell. It does not move.
- **Coordinate**: A coordinate is a two-dimensional coordinate pair.