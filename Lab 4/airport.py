import argparse

from avl import AVL


# # NOTE: Incase you did not get AVL working, use this:
# from bst import BST
# class Airport(BST):
#    def __init__(self, wait_time=300000, simple=False):
#        BST.__init__(self)

class Airport(AVL):
    def __init__(self, wait_time=300000, simple=False):
        """Creates a new Airport instance and sets its basic attributes."""
        AVL.__init__(self)

        self.wait_time = wait_time
        self.simple = simple

    def find_conflict(self, time):
        """Return the first node in the tree that conflicts with the specified
           time and wait_time attribute set for the Airport.

           Returns None if no such conflict is found."""
        pass

    def bounded_insert(self, time, tailnumber):
        """Inserts a airplane with a time and tailnumber into the schedule.
           If the difference between the proposed time and an existing node
           in schedule is less then the wait_time, the airplane cannot be
           scheduled at that time.

           If the simple flag is set to True, conflict are not inserted
           and otherwise the program will try to insert in the next
           possible timeslot.

           Returns the node if successfully inserted and None otherwise."""
        pass

    def __str__(self):
        """Return the airplanes in the schedule in sorted order."""
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sort a list of elements.')
    parser.add_argument('elements', nargs='+',
                        help='The elements of a list')
    parser.add_argument("-t", "--timestep", type=int,
                        help="set the minimum timestep (default=300000)",
                        default=300000)
    parser.add_argument("-s", "--simple", action="store_true",
                        help="either become simple or not")
    args = parser.parse_args()

    cs_airport = Airport(args.timestep, args.simple)
    for elem in args.elements:
        try:
            s = elem.split('/')
            time, tail = int(s[0]), s[1]
            cs_airport.bounded_insert(time, tail)
        except (ValueError, IndexError):
            print("Invalid airplane format: " + elem)

    print(cs_airport)
