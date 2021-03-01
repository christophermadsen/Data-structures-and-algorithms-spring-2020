####################################
### Datastructuren en Algoritmen ###
######## Trial by Circuits #########

### Author ###
Christopher Buch Madsen (11306394)

### dependencies ###
Python 3.7.#
- numpy
- pandas
- xlrd (for the pandas read_excel)

### Instructions ###
Please see the overview section for a more general overview of my program.

To run the program you can execute main.py, you will see this will start solving
a board and netlist. To change which netlist and board is being solved, I have
included 2 global variables at the top of the file which can be changed freely.

The visualization in the proper betchy format is saved to a .txt file in the
same directory as main.py.

For the 2 netlists I could not solve, I have implemented a loop that randomly
shuffles order of the 2nd half of the netlist. For board 1 netlist 3, without a
shuffle it gets stuck at the last 2 wires, but the 13th shuffle with the random
seed set at the top of the file completely solves the netlist.
For netlist 2 and 3 from board 2, the program is unlikely to completely solve it,
instead the loop will continue for a set amount of iterations. The amount of
iterations for random shuffling can be changed in the global variable at the top
of main.py.

My program can 100% solve netlists 1, 2 and 3 from board 1, as well as netlist 1
from board 2. For netlist 2 and 3 from board 3, there is also provided the
attempts. I am not sure if my program can solve board 2 netlist 2 and 3, because
I only do 20 random iterations on default, but perhaps a few more could do the
trick.

It is possible to KeyboardInterrupt out of the random shuffling loop, but it
will only give the best order for solving the netlist so far, with no visuals.

!!! Remember, the 3 global variables are at the top of main.py !!!

### Overview ###

Files in the program
- main.py
- board.py
- gate.py
- wire.py
- node.py
- A_star_algorithm.py

# main.py
Contains the main loop for running the code. Execute this to get started.

# board.py
Contains the board class. This is the hub for all things involving the board,
from reading the file to interactions between gates, wires and visualization.

# gate.py
Contains the gate class for the board.

# wire.py
Contains the wire class for the board.

# node.py
Contains the node class which is an important feature in my A* implementation.

# A_star_algorithm
This is where the A* algorithm is written, it is the core of the solution
provided in this program. It also contains the heuristic function which is the
most interesting part of my solution.

### Thank you for reading my code! ###
