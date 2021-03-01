"""Contains the CircuitBoardWire class

Author:
    Christopher Buch Madsen
    11306394

Description:
    This file implements the CircuitBoardWire class.
"""


class CircuitBoardWire:
    """ The CircuitBoardWire is used for marking wires placements in the board
    of the CircuitBoard class. It contains its wire ID from its netlist, a path
    obtained through the A* algorithm and the head and tail connected to a gate
    in the CircuitBoard. The wire is also hashable by its ID.
    """
    def __init__(self, path, wire_id, start, end):
        self.wire = path
        self.id = wire_id
        self.start = start
        self.end = end

    def __hash__(self):
        return self.id
