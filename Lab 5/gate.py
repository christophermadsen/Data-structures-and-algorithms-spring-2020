"""Contains the CircuitBoardGate class and its functions

Author:
    Christopher Buch Madsen
    (11306394)

Description:
    This file implements the CircuitBoardGate class.
"""


class CircuitBoardGate:
    """ The CircuitBoardGate contains its own coordinates in the board and its
    gate ID.
    """
    def __init__(self, coordinate=(), gate_id=int):
        self.coord = coordinate
        self.id = gate_id
