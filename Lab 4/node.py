class Node(object):
    def __init__(self, key, value=None):
        """Store the key and value in the node and set the other attributes."""
        self.key = key
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0

    def get_key(self):
        """Return the key of this node."""
        return self.key

    def get_value(self):
        """Return the value of this node."""
        return self.value

    def get_parent(self):
        """Return the parent node of this node."""
        return self.parent

    def get_left_child(self):
        """Return the left child node of this node."""
        return self.left_child

    def get_right_child(self):
        """Return the right child node of this node."""
        return self.right_child

    def get_height(self):
        """Return the height of this node."""
        return self.height

    def update_height(self):
        """Update the height based on the height of the left and right
           nodes."""
        l = self.get_left_child()
        r = self.get_right_child()
        if l and r:
           self.height = max(l.get_height(), r.get_height()) + 1
        elif l:
           self.height = l.get_height() + 1
        elif r:
           self.height = r.get_height() + 1


    #
    # You can add any additional node functions you might need here
    #

    def __eq__(self, other):
        """Returns True if the node key is equal to other, which can be
           another node or a number."""
        if type(self) == type(other):
            return self.get_key() == other.get_key()
        else:
            return self.get_key() == other

    def __neq__(self, other):
        """Returns True if the node key is not equal to other, which can be
           another node or a number."""
        if type(self) == type(other):
            return not (self.get_key() == other.get_key())
        else:
            return not (self.get_key() == other)

    def __lt__(self, other):
        """Returns True if the node key is less than other, which can be
           another node or a number."""
        if type(self) == type(other):
            return self.get_key() < other.get_key()
        else:
            return self.get_key() < other

    def __le__(self, other):
        """Returns True if the node key is less than or equal to other, which
           can be another node or a number."""
        if type(self) == type(other):
            return self.get_key() <= other.get_key()
        else:
            return self.get_key() <= other

    def __gt__(self, other):
        """Returns True if the node key is greater than other, which can be
           another node or a number."""
        if type(self) == type(other):
            return self.get_key() > other.get_key()
        else:
            return self.get_key() > other

    def __ge__(self, other):
        """Returns True if the node key is greater than or equal to other,
           which can be another node or a number."""
        if type(self) == type(other):
            return self.get_key() >= other.get_key()
        else:
            return self.get_key() >= other

    def __str__(self):
        """Returns the string representation of the node in format: 'key/value'.
           If no value is stored, the representation is just: 'key'."""
        if self.get_value():
           return f"{self.get_key()}/{self.get_value()}"
        else:
           return f"{self.get_key()}"
