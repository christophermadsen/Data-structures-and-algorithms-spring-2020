"""Contains the CircuitBoard class and its functions.

Author:
    Christopher Buch Madsen
    (11306394)

Description:
    This file implements the CircuitBoard class including methods to read a
    given circuit board file, getting adjacent coordinates for a coordinate,
    adding a wire and resetting the board.
"""


import numpy as np
import pandas as pd
from gate import CircuitBoardGate
from wire import CircuitBoardWire
from A_star_algorithm import manhattan_distance, A_star


class CircuitBoard:
    """The CircuitBoard is essentially a Numpy ndarray containing the proper
    dimensions, gates and netlist configurations from a given circuit board
    file it reads the file at instantiation and extracts the information.
    The board contains useful methods for the A* algorithm and is able to add
    wires between gates from paths found in A*. It also contains a method to
    visualize layers and writing all layers to a file in proper Betchy format
    and ways to sort the netlist. For a given circuit board solution it can
    tighten the wires again through A*.
    """

    def __init__(self, filename="", netlist=1):
        self.filename = filename
        self.netlist = netlist
        self.gates = []
        self.gate_coordinates = []
        self.ordered_netlist = []
        self.wires = []
        self.netlist_pairs = []
        self.board = None
        self.read_circuit_file()

    def read_circuit_file(self):
        """No return, called in __init__ and sets initial values.

        Reads a circuit board file, drops empty rows. Extracts the board
        dimensions and initializes an ndarray as the board. Extracts the
        gate coordinates and netlist pairs from the file, and inserts the gates
        into the board ndarray.
        """
        # Reading the file as an excel with pandas + xlrd
        file = pd.read_excel(self.filename, header=None, index=False)
        file = file.dropna(how='all')

        # Extracting the dimensions and initializing the board
        dimensions = file[1][1].split(' ')
        self.dim = (7, int(dimensions[2]), int(dimensions[0]))
        self.board = np.zeros(self.dim, dtype=object)

        # Initializing control booleans and lists for sorting the data
        copy_netlist = False
        copy_gates = False
        gate_coordinates = []
        netlist_pairs = []

        # Main parsing loop. Parses over the file and fills the data into the
        # correct lists based on booleans controlling copying.
        for _, row in file.iterrows():
            if type(row[0]) == str:
                check = row[0].lower()
                if "netlist" in check and f'{self.netlist}' in check:
                    copy_gates = False
                    copy_netlist = True

                elif "netlist" in check and f'{self.netlist}' not in check:
                    copy_netlist = False
                    copy_gates = False

                elif check == 'gate number':
                    copy_gates = True
                continue

            if copy_gates:
                gate_coordinates.append(row.tolist())

            if copy_netlist:
                netlist_pairs.append(row.tolist()[:-1])

        self.netlist_pairs = np.array(netlist_pairs)
        gate_coordinates = np.array(gate_coordinates)

        # Instantiates all the gates and puts them on the board
        for gate in gate_coordinates:
            id = gate[0]
            new_gate = CircuitBoardGate((0, gate[2], gate[1]), id)
            self.gate_coordinates.append((0, gate[2], gate[1]))
            self.board[new_gate.coord] = new_gate
            self.gates.append(new_gate)

    def get_adjacent_coordinates(self, node_coordinate=(), cube=False):
        """ Returns a list of tuples

        Given a node_coordiante it calculates its valid adjacent indices. If
        the bool "cube" is set to True it will include the entire cube of
        coordinates surrounding the given coordinate, i.e also the diagonals.
        """
        q, r, s = node_coordinate
        neighbours = [
            (q-1, r, s),
            (q+1, r, s),
            (q, r-1, s),
            (q, r+1, s),
            (q, r, s-1),
            (q, r, s+1)
        ]

        if cube:
            neighbours += [
                (q-1, r-1, s-1),
                (q+1, r+1, s+1),
                (q+1, r-1, s-1),
                (q+1, r+1, s-1),
                (q-1, r+1, s-1),
                (q-1, r-1, s+1),
                (q+1, r-1, s+1),
                (q-1, r+1, s+1)
            ]

        adjacents = []
        for index, adjacent in enumerate(neighbours):
            q, r, s = adjacent
            if q < 0 or q >= self.dim[0]:
                continue
            elif r < 0 or r >= self.dim[1]:
                continue
            elif s < 0 or s >= self.dim[2]:
                continue
            adjacents.append(adjacent)
        return adjacents

    def add_wire(self, path, gate1_id, gate2_id, wire_id):
        """ Connects two gates with a wire

        Given a path found through A* instantiates a CircuitBoardWire class,
        connects the two gates and adds it to the CircuitBoard board.
        """
        # Instantiating the wire
        wire = CircuitBoardWire(path, wire_id, self.gates[gate1_id],
                                self.gates[gate2_id])

        # Adding the wire to the board
        for coord in path:
            self.board[coord] = wire
        self.wires.append(wire)

    def sort_netlist_by_distances(self):
        """ Returns an ordered netlist

        Sorts the board netlist by the manhattan distances between the pairs.
        """
        distances = {}
        for index, pair in enumerate(self.netlist_pairs):
            g1 = self.gates[pair[0]-1].coord
            g2 = self.gates[pair[1]-1].coord
            distances[index] = manhattan_distance(g1, g2)
        order = sorted(distances, key=distances.get)
        return order

    def sort_netlist_by_connections(self):
        """ Returns an ordered netlist

        Sorts a netlist based on the sum of connections between the two gates
        in each netlist pair.
        """
        pairs = self.netlist_pairs
        unique, counts = np.unique(pairs.flatten(), return_counts=True)
        counts = dict(zip(unique, counts))
        order = [counts[pair[0]] + counts[pair[1]] for pair in pairs]
        order = list(np.argsort(order))
        return order[::-1]

    def visualize_layer(self, board_layer, layer_id, add_axis=False):
        """ Returns a string

        Parses a board layer and builds a string with proper Betchy format.
        If the bool add_axis is set to True, axis are added to the string for
        easier inspection.
        """
        layer = f"### LAYER {layer_id} ###\n"
        for x, row in enumerate(board_layer):
            line = ""
            for column in row:
                if isinstance(column, CircuitBoardGate):
                    line += f"  GA"
                elif isinstance(column, CircuitBoardWire):
                    line += f"  {column.id:02}"
                else:
                    line += f"  __"

            if add_axis:
                line += f"  {x}"

            layer += line[2:] + "\n"

        if add_axis:
            y_axis = list(range(board_layer.shape[1]))
            last = ""
            for y in y_axis:
                last += f"  {y:02}"
            last = last[2:]
            last += "\n"
            layer += last
        return layer

    def visualize_board(self, filename):
        """ Writes to a .txt

        Given a file name, uses the visualize layer function to visualze each
        layer then patches them together and writes them to a file with the
        file name.
        """
        layers = ""
        for id, layer in enumerate(self.board):
            layers += self.visualize_layer(layer, id+1) + "\n"
        layers = layers[:-2]

        text_file = open(filename, "w")
        text_file.write(layers)
        text_file.close()

    def tighten_wires(self):
        """ Runs A*

        Tightens all the wires placed in the board with A*. This is useful if
        the wires have been placed with weights and they aren't all necessarily
        the shortest paths possible between the gate pairs.
        """
        for wire in self.wires:
            self.remove_wire(wire)
            path = A_star(self, wire.start, wire.end, wire.id, True)
            self.add_wire(path, wire.start.id-1, wire.end.id-1, wire.id)

    def remove_wire(self, wire):
        """ Removes a wire

        Traverses the path throug the coordinates in a wire and removes all
        traces of it from the board.
        """
        self.wires.remove(wire)
        for coordinate in wire.wire:
            self.board[coordinate] = 0

    def reset_board(self):
        """ Resets the CircuitBoard

        Resets the CircuitBoard instance by rereading the circuit board file.
        """
        self.read_circuit_file()
