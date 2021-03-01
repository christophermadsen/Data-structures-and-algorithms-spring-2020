from node import Node


class BST(object):
    def __init__(self, key_list=[]):
        """Create a new BST, set its attributes, and insert all the keys in
           the key_list into the BST."""
        self.key_list = key_list
        self.root = None

        # Builds the tree
        for key in self.key_list:
            self.insert(key)

    def get_root(self):
        """Return the root of the BST."""
        return self.root

    def is_empty(self):
        """Return True if the BST is empty."""
        if not self.root:
            return True

    def find_max(self):
        """Return the node with the maximum key in the BST."""
        # Continue right until right-most is reached.
        max = self.root
        while max.get_right_child():
            max = max.get_right_child()
        return max

    def find_min(self):
        """Return the node with the minimum key in the BST."""
        # Continue left until left-most is reached.
        min = self.root
        while min.get_left_child():
            min = min.get_left_child()
        return min

    def search(self, key):
        """Return the Node object containing the key if the key exists in
           the BST, else return None."""
        node = self.root
        if not node:
            return None

        # While not equal traverse left/right comparing keys less/greater than.
        while node:
            if node.__eq__(key):
                return node

            if node.__lt__(key):
                node = node.get_right_child()
            else:
                node = node.get_left_child()
        return None

    def contains(self, key):
        """ Return True if the key exists in the BST, else return False."""
        if self.search(key):
            return True
        else:
            return False

    def insert(self, key, value=None):
        """Create a new node for this key and value, and insert it into the
           BST.

           Return the new inserted node, or None if the key and value could not
           be inserted."""
        if self.is_empty():
            self.root = Node(key, value)
            return self.root

        if self.contains(key):
            return None

        """ Traverses the tree by comparing left/right and moving accordingly
            When an empty child is reached, inserts the new node and updates
            child and height for the parent, and parent for the new node. """
        node = self.root
        while node:
            if node.__gt__(key):
                child = node.get_left_child()
                if child:
                    node = child
                else:
                    new_node = Node(key, value)
                    new_node.parent = node
                    node.left_child = new_node
                    self.update_heights(new_node)
                    return new_node
            else:
                child = node.get_right_child()
                if child:
                    node = child
                else:
                    new_node = Node(key, value)
                    new_node.parent = node
                    node.right_child = new_node
                    self.update_heights(new_node)
                    return new_node

    def delete(self, key):
        """Remove the Node object containing the key if the key exists in
           the BST and return the removed node, else return None.

           The returned node is the actual Node object that got removed
           from the BST, and so might be successor of the removed key."""

        # Get node to be deleted
        node = self.search(key)
        if not node:
            return None

        # Children of node to be deleted
        left_child = node.get_left_child()
        right_child = node.get_right_child()

        """ In the case where the node has 2 children, go to the right child's
            subtree and get the left-most node to replace it """
        if left_child and right_child:
            substitute = right_child
            while substitute.get_left_child():
                substitute = substitute.get_left_child()

            # Reconnect where replacement was taken from in the tree.
            if substitute.get_right_child():
                substitute.get_right_child().parent = substitute.get_parent()
                substitute.get_parent().left_child =substitute.get_right_child()
                self.update_heights(substitute.get_right_child())

            # Connect substitute to where node currently is
            substitute.left_child = left_child
            substitute.right_child = right_child
            substitute.parent = node.get_parent()
            # substitute.get_left_child().parent = substitute
            # substitute.get_right_child().parent = substitute
            self.update_heights(substitute)

            # Disconnect node
            node.parent = None
            node.left_child = None
            node.right_child = None
            return Node

        # Case where node has only a left child.
        elif left_child:
            parent = self.detach_from_parent(node, left_child)
            if parent:
                self.update_heights(parent)
            node.parent = None
            return node

        # Case where node has only a right child.
        elif right_child:
            parent = self.detach_from_parent(node, right_child)
            if parent:
                self.update_heights(parent)
            node.parent = None
            return node

        else:
            parent = self.detach_from_parent(node)
            if parent:
                self.update_heights(parent)
            node.parent = None
            return node

        return None

    def in_order_traversal(self):
        """Return a list of the Nodes in the tree in sorted order."""
        start = self.root
        node_list = []
        # Helper function for recursively traversing the tree
        return self.in_order_recursion(start, node_list)

    # Performs in_order_traversal by recursively visiting nodes in order
    def in_order_recursion(self, node, node_list):
        if node:
            left = node.get_left_child()
            right = node.get_right_child()

            # If node has a left child node
            if left:
                self.in_order_recursion(left, node_list)

            # Append the left node to list of visited nodes
            node_list.append(node)

            # If node has a right child node (and not a left)
            if right:
                self.in_order_recursion(right, node_list)

        return node_list

    def breadth_first_traversal(self):
        """Return a list of lists, where each inner lists contains the elements
           of one layer in the tree. Layers are filled in breadth-first-order,
           and contain contain all elements linked in the BST, including the
           None elements.
           >> BST([5, 8]).breadth_first_traversal()
           [[Node(5)], [None, Node(8)], [None, None]]"""

        level = [self.root]
        node_list = [level]

        # While a level is not exclusively None, add the nodes in the level.
        while not self.level_only_none(level):
            level = []
            for node in node_list[-1]:
                if node:
                    level += [node.get_left_child(), node.get_right_child()]
            node_list.append(level)
        return node_list

    # Breadth first helper function to check if a level only consists of Nones.
    def level_only_none(self, tree_level):
        for node in tree_level:
            if node:
                return False
        return True

    # Updates the height of all parent nodes from a node to the tree root.
    def update_heights(self, node):
        while node:
            node.update_height()
            node = node.get_parent()

    # Detaches a node from it's parent and patches the hole
    def detach_from_parent(self, node, replacement=None):
        parent = node.get_parent()
        if parent:
            if node.__eq__(parent.get_left_child()):
                if replacement:
                    parent.left_child = replacement
                    replacement.parent = parent
                else:
                    parent.left_child = None
            else:
                if replacement:
                    parent.right_child = replacement
                    replacement.parent = parent
                else:
                    parent.right_child = None
        return parent

    def __str__(self):
        """Return a string containing the elements of the tree in breadth-first
           order, with each on a new line, and None elements as `_`, and
           finally a single line containing all the nodes in sorted order.
           >>> print(BST([5, 8, 3]))
           5
           3 8
           _ _ _ _
           3 5 8
           """
        bft = self.breadth_first_traversal()
        iot = self.in_order_traversal()
        output = ""
        for level in bft:
            line = ""
            for node in level:
                if node:
                    line += f"{node} "
                else:
                    line += f"_ "
            output += f"{line[:-1]}\n"

        final = ""
        for node in iot:
            final += f"{node} "
        output += final[:-1]
        return output
