"""Contains method for the A* star search algorithm

Author:
    Christopher Buch Madsen
    11306394

Description:
    This file implements the A* algorithm, a function used as the heuristic for
    A* and the distance function used.
"""


from queue import PriorityQueue
from node import Node
import numpy as np


def manhattan_distance(index1=(), index2=()):
    """Returns an int

    Calculates the Manhattan distance for a given pair of arbitrarily sized
    vectors (board indices) |x1 - y1| + ... |xn - yn|.
    """
    md = 0
    for a1, a2 in zip(index1, index2):
        md += abs(a1-a2)
    return md


def heuristic(board, node_coordinate, start_coordinate, goal_coordinate):
    """ Returns a float

    Calculates the heuristic/cost used in the A* algorithm for denoting the
    weight of a given node/coordinate. The heigher the heuristic the more
    expensive/less prioritised the node will be when traversing.
    """
    # The cost is initially just the Manhattan distance
    cost = manhattan_distance(node_coordinate, goal_coordinate)

    # If a node is adjacent to a gate on the CircuitBoard its cost is
    # drastically increased. This excludes the start and goal gates.
    adjacents = board.get_adjacent_coordinates(node_coordinate, cube=True)
    if goal_coordinate in adjacents:
        adjacents.remove(goal_coordinate)
    if start_coordinate in adjacents:
        adjacents.remove(start_coordinate)
    if any(adjacent in adjacents for adjacent in board.gate_coordinates):
        cost += 1000

    # 3/4 of amount of non-empty spots in the node's layer is added to its cost
    # to discourage overcrowding single layers.
    nonzeros = np.count_nonzero(board.board[node_coordinate[0]])
    cost += nonzeros * 0.75

    # To encourage moving upwards, each layer has a weight which decreases the
    # cost with a factor of the weight.
    height_weights = [1, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    cost *= height_weights[node_coordinate[0]]
    return cost


def reconstruct_path(current):
    """ Returns list of tuples

    Reconstructs the path by traversing through the parents of parents of the
    node that found the goal and adding their coordinates to a list until the
    start gate is again reached.
    """
    path = [current.coord]
    parent = current.parent
    while parent:
        path = [parent.coord] + path
        parent = parent.parent
    path = path[1:]
    return path


def A_star(board, gate1, gate2, wire_id, simple_heuristic=False):
    """ Returns a list of tuples

    Implementation of the A* algorithm utilizing the Node class and a
    PriorityQueue. The board is traversed by generating children nodes and
    computing their costs based on a heuristic function. The least costly
    children are prioritised through the queue and the path is saved in the
    nodes parents. When a node is visited it is removed from the priority queue
    and added to a dictionary of visited nodes. If a path is found it returns
    all the coordinates in the path.
    """
    # Initializing all the necessary variables/instances
    start_node = Node(gate1.coord)
    open_queue = PriorityQueue()
    open_queue.put(start_node)
    closed_set = {}
    open_set = set()
    open_set.add(start_node)
    goal_adjacents = board.get_adjacent_coordinates(gate2.coord)

    # The main loop for traversing the board.
    while not open_queue.empty():
        # Getting least costly node and removing it from the queue
        current = open_queue.get()
        open_set.remove(current)

        # If a path has been found reconstruct and return path
        if current.coord in goal_adjacents and not current == gate1:
            return reconstruct_path(current)

        # Loop for spawning children nodes and checking their validity.
        for coordinate in board.get_adjacent_coordinates(current.coord):
            # Ignore the child if place is taken and not taken by the goal.
            if board.board[coordinate] and coordinate != gate2.coord:
                continue

            # If the node has already been visited, get the pre-computed
            # instantiated node, otherwise instantiate a new one.
            if coordinate in closed_set:
                neighbour = closed_set[coordinate]
            else:
                neighbour = Node(coordinate, current, float("inf"))

            # Precompute an updated cost with the heuristic function
            if simple_heuristic:
                cost = current.cost + manhattan_distance(coordinate,
                                                         gate2.coord)
            else:
                cost = current.cost + heuristic(board, coordinate,
                                                gate1.coord, gate2.coord)

            # If the child is cheaper, update its cost.
            if cost < neighbour.cost:
                neighbour.cost = cost
                closed_set[neighbour.coord] = neighbour

                # If not in priority queue add it to expand nodes to visit.
                if neighbour not in open_set:
                    open_set.add(neighbour)
                    open_queue.put(neighbour)
    return None
