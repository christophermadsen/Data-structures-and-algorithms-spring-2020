"""Contains the Node class

Author:
    Christopher Buch Madsen
    11306394

Description:
    This file implements the node class used in the A* algorithm.
"""


class Node:
    """ This represents a node used in the A* algorithm. The node contains its own
    coordinates, cost and its parent node. In the class functions for hashing
    and comparing to other nodes/coordinates have been implemented to make it
    possible to use the node with python's native PriorityQueue.
    """
    def __init__(self, coord=(), parent=None, cost=0):
        self.coord = coord
        self.parent = parent
        self.cost = cost

    def __hash__(self):
        return hash(self.coord)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coord == other.coord
        else:
            return self.coord == other

    def __le__(self, other):
        if isinstance(other, Node):
            return self.cost <= other.cost
        else:
            return self.cost <= other

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.cost < other.cost
        else:
            return self.cost < other

    def __ge__(self, other):
        if isinstance(other, Node):
            return self.cost >= other.cost
        else:
            return self.cost >= other

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.cost > other.cost
        else:
            return self.cost > other
