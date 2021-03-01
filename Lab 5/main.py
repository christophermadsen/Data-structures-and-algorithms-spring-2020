"""Contains the main function

Author:
    Christopher Buch Madsen
    11306394

Description:
    Main initializes and executes the algorithm in the correct manner.
    It also features a "solving loop" for shuffling part of wiring order if the
    board is close to being solved.
"""
from board import CircuitBoard
from A_star_algorithm import manhattan_distance, A_star
import random


BOARD_NUM = 1
NETLIST_NUM = 3
MAX_RAND_ITER = 20
random.seed(int("".join([str(ord(c)) for c in "Thanks for the extension!"])))


def main(board_num, netlist_num, max_rand_iter):
    """ Executes all relevant code for the assignment.

    Executes all the code relevant to the entire program. It has a "solving
    loop". The order of the netlist is first sorted, then the A* algorithm is
    executed. For the netlists not completely solvable by A* and its
    heuristics, a failsafe is introduced where the 2nd half of the ordered
    netlist is randomly shuffled and the "solving loop", placing all the wires
    with A* is iterated again until a given max iterations is reached. If the
    algorithm didn't manage to solve the board the best order of wiring is
    printed and the best solution is still visualized even though incomplete.
    """
    # Instantiation of the board, and wire amount
    board = CircuitBoard(f"circuit_board_{board_num}.xlsx", netlist_num)
    n_wires = len(board.netlist_pairs)

    # Important for solving! Order of wiring
    order = board.sort_netlist_by_connections()
    best_order = order

    # Relevant to early stopping
    rand_iter = 0
    max_wires = 0

    # The try/except allows for KeyboardInterrupt and still getting a result.
    try:
        # Main algorithm loop
        complete = False
        while not complete:
            wire_n = 1
            # Looping over each pair in the ordered netlist
            for wire_id, ids in zip(order, board.netlist_pairs[order]):
                gate1 = board.gates[ids[0]-1]
                gate2 = board.gates[ids[1]-1]

                # If the gates are immediate neighbours they are already wired!
                if manhattan_distance(gate1.coord, gate2.coord) == 1:
                    continue

                # Getting the best path between two gates in the netlist
                path = A_star(board, gate1, gate2, wire_id)

                # If a path was found, add the path as a wire to the board.
                # Otherwise, visualize board for a better issue overview and
                # break the current solving loop.
                if path:
                    board.add_wire(path, ids[0]-1, ids[1]-1, wire_id)
                else:
                    for i in range(7):
                        print(board.visualize_layer(board.board[i], i+1,
                                                    add_axis=True))

                    # Printing the stats of the wire that couldn't be solved.
                    out_stats = (f"Got to wire {wire_n}/{n_wires}, {wire_id}: "
                                 f"{ids[0]}--{ids[1]}, {gate1.coord[1:]}, "
                                 f"{gate2.coord[1:]}")

                    print(out_stats)
                    break

                # Progress tracking
                wire_n += 1
                print(f"Currently wiring #{wire_n}", end='\r')

            # If the path was solved, end the solving loop. Otherwise, start
            # randomly shuffling 2nd half of the order and try again until
            # specified max iterations have been reached.
            if path:
                complete = True
                print("\nFinished solving the board")
            else:
                # Keep track of the better order
                if wire_n > max_wires:
                    max_wires = wire_n
                    best_order = order

                # Reset the board, shuffle 2nd half to try again
                board.reset_board()
                half = int(len(order)/2)
                copy = order[half:]
                random.shuffle(copy)
                order[half:] = copy

                # If the max iterations have been reached, run the best loop
                # one final time with the best found order to visualize it,
                # like you would a complete solution.
                print(f"Current random iteration: {rand_iter}/{max_rand_iter}")
                rand_iter += 1
                if rand_iter == max_rand_iter:
                    board.reset_board()
                    order = best_order
                    wire_n = 0
                    correct = 0
                    for wire_id, ids in zip(order, board.netlist_pairs[order]):
                        print(f"Currently at #{wire_n}", end='\r')
                        gate1 = board.gates[ids[0]-1]
                        gate2 = board.gates[ids[1]-1]
                        path = A_star(board, gate1, gate2, wire_id)
                        wire_n += 1
                        if not path:
                            continue
                        else:
                            board.add_wire(path, ids[0]-1, ids[1]-1, wire_id)
                            correct += 1
                    print(f"Managed to solve {correct}/{n_wires}")
                    print(f"Best order was: {best_order}")
                    break

        board.tighten_wires()
        board.visualize_board(f"board{board_num}_list{netlist_num}.txt")

    except KeyboardInterrupt:
        print("Early Exit, trying to print best order...")
        print(best_order)


if __name__ == '__main__':
    main(BOARD_NUM, NETLIST_NUM, MAX_RAND_ITER)
    print("Program has finished running.")
