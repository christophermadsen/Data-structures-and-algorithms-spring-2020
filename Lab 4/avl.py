from bst import BST


class AVL(BST):
    def __init__(self, key_list=[]):
        """Create a new AVL Tree, set its attributes, and insert all the keys in
           the key_list into the AVL."""
        BST.__init__(self, key_list)

    def insert(self, key, value=None):
        """Create a new node for this key and value, and insert it into the AVL
           using the BST insert operation. In addition, it ensures that the AVL
           tree is still balanced after this operation is performed.

           Return the new inserted node, or None if the key and value could not
           be inserted."""
        pass

    def delete(self, key):
        """Remove the Node object containing the key if the key exists in
           the AVL using the BST delete operation. In addition, it ensures that
           the AVL tree is still balanced after this operation is performed.

           Return the node that actually got removed from the AVL, which might
           be successor of the removed key."""
        pass

    @staticmethod
    def left_rotate(node):
        """Performs a left rotation of the specified node."""
        pass

    @staticmethod
    def right_rotate(node):
        """Performs a right rotation of the specified node."""
        pass

    def fix_balance(self, node):
        """Performs a sequence of rotations to fix the balance of a node and
           all its parent nodes if needed to maintain the AVL property."""
        pass
