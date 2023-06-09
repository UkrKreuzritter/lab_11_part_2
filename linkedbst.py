"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import time
import random

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find_1(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)






    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        current = self._root
        while current:
            if item == current.data:
                return item
            elif item < current.data:
                current = current.left
            else:
                current = current.right
        return None
     










    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0
    
    
    def add(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
        # Otherwise, search for the item's spot
        else:
            current = self._root
            while current:
                # print(item)
                if item < current.data:
                    if current.left == None:
                        current.left = BSTNode(item)
                        self._size += 1
                        return
                    else:
                        current = current.left
                # New item is greater or equal,
                # go right until spot is found
                elif current.right == None:
                    current.right = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.right
                    # End of recurse
        
        
        

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def root_height(top):
            if not top or (not top.left and not top.right):
                return 0
            return 1 + max(root_height(top.right), root_height(top.left))
        return root_height(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height()< 2 * int(log(self._size+1, 2)) -1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = self.inorder()
        res = [i for i in res]
        i = 0
        while i<len(res) and res[i]<low:
            i+=1
        if i==len(res):
            return None
        j = len(res)-1
        while j>=0 and res[j]>high:
            j-=1
        if j==-1:
            return None
        return res[i:j+1]

    def rebalance(self, res = None):
        '''
        Rebalances the tree.
        :return:
        '''
        def rebalance_node(res):
            if len(res)==0:
                return None
            if len(res)==1:
                return BSTNode(res[0])
            iter = (len(res))//2
            current = BSTNode(res[iter])
            current.left = rebalance_node(res[:iter])
            if iter+1<len(res):
                current.right = rebalance_node(res[iter+1:])
            return current
        if not res:
            res = self.inorder()
            res = [i for i in res]
        self._root = rebalance_node(res)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = self.inorder()
        res = [i for i in res]
        i = 0
        while i<len(res) and res[i]<=item:
            i+=1
        if i==len(res):
            return None
        return res[i]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        res = self.inorder()
        res = [i for i in res]
        i = len(res)-1
        while i>=0 and res[i]>=item:
            i-=1
        if i==-1:
            return None
        return res[i]
    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words = open(path, 'r', encoding = 'utf-8')
        word_list = []
        for line in words:
            word_list.append(line.strip())
        words_to_create = [random.choice(word_list) for i in range(100000)]
        words_to_create.sort()

        start = time.time()
        for i in range(10000):
            word = random.choice(word_list)
            word in words_to_create
        print("List time:",time.time() - start)

        test_tree = LinkedBST(words_to_create)

        start = time.time()
        for i in range(10000):
            word = random.choice(word_list)
            test_tree.find(word)
        print("Alphabet BST time:",time.time() - start)

        test_tree = LinkedBST([random.choice(word_list) for i in range(len(words_to_create))])

        start = time.time()
        for i in range(10000):
            word = random.choice(word_list)
            test_tree.find(word)
        print("Random BST time:", time.time() - start)

        test_tree.rebalance()

        start = time.time()
        for i in range(10000):
            word = random.choice(word_list)
            test_tree.find(word)
        print("Balanced BST time:", time.time() - start)
LinkedBST.demo_bst("words.txt")
