# Name: Nargis Habibi
# OSU Email: habibin@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 5
# Due Date: Nov 16, 2021
# Description: Implement the AVL class by completing the provided skeleton code.


import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True

    # --------------------------ADD METHOD---------------------------------------------

    def getHeight(self, root):
        """HELPER FUNCTION: returns the height of the given node.
        If None, returns -1"""
        if root is None:
            return -1
        return root.height

    def getBalance(self, root):
        """HELPER FUNCTION:returns the factor balance of a node."""
        if root is None:
            return -1
        return self.getHeight(root.left) - self.getHeight(root.right)

    def leftRotate(self, node):
        """HELPER FUNCTION: Left rotation for ADD method"""
        child = node.right
        node.right = child.left
        if child.left != None:
            child.left.parent = node
        child.left = node
        child.parent = node.parent
        node.parent = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right))
        return child

    def rightRotate(self, node):
        """HELPER FUNCTION: Right rotation for ADD method"""
        child = node.left
        node.left = child.right
        if child.right != None:
            child.right.parent = node
        child.right = node
        child.parent = node.parent
        node.parent = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right))
        return child

    def add(self, value: object) -> None:
        """
        TODO: adds a new value to the tree while maintaining its AVL property. Duplicate
        TODO: values are not allowed.
        """

        root = self.root
        self.root = self.insert(root, value)

    def insert(self, root, key):
        """HELPER FUNCTION: Inserts nodes into BST tree recursively
        and checks if the subtree with inserted node needs rebalancing"""

        #inserts new node into empty leaf
        if root is None:
            return TreeNode(key)

        #Prevents duplicates
        if key == root.value:
            return root

        # recursively find empty leaf, updates child and parent pointer
        elif key > root.value:
            rightchild = self.insert(root.right, key)
            root.right = rightchild
            rightchild.parent = root

        # recursively find empty leaf, updates child and parent pointer
        else:
            leftchild = self.insert(root.left, key)
            root.left = leftchild
            leftchild.parent = root

        #updates height and finds factor balance
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        """If the node is unbalanced, then tries out the 4 cases"""
        # LL
        if balance > 1 and key < root.left.value:
            return self.rightRotate(root)

        # RR
        if balance < -1 and key > root.right.value:
            return self.leftRotate(root)

        # LR
        if balance > 1 and key > root.left.value:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # RL
        if balance < -1 and key < root.right.value:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root


#------------------------REMOVE METHOD-----------------------------------------------


    def find_loc(self, key):
        """HELPER FUNCTION: finds the value and returns it's node"""

        node = self.root
        while node is not None:
            if node.value == key:
                return node
            elif key < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def findSuccessor(self, node):
        """HELPER FUNCTION: finds inorder successor of a node"""
        if node.right != None:
            currentnode = node.right
            while currentnode.left:
                currentnode = currentnode.left
            return currentnode

    def BST_removal(self, value):
        """HELPER FUNCTION: if node is removed, returns True or False"""

        # finds the node
        node = self.find_loc(value)

        # returns False if the node was not found
        if node is False:
            return False

        # checks if node has no children.
        # If true, updates PN to point to None instead of node
        elif node.right is None and node.left is None:
            # if there is single node in tree, empties tree
            if node == self.root:
                self.make_empty()
            elif node == node.parent.right:
                node.parent.right = None
            else:
                node.parent.left = None
            return node.parent

        # checks if node has 1 child
        # If true, updates PN to point to node's child instead of node.
        elif node.right and node.left is None or node.right is None and node.left:

            if node == self.root:
                if node.right:
                    self.root = node.right
                    node = self.root
                    node.parent = None
                else:
                    self.root = node.left
                    node = self.root
                    node.parent = None

            elif node == node.parent.right:
                if node.right:
                    node.parent.right = node.right
                    node.right.parent = node.parent
                    node = node.right
                else:  # if node.left:
                    node.parent.right = node.left
                    node.left.parent = node.parent
                    node = node.left

            elif node == node.parent.left:
                if node.left:
                    node.parent.left = node.left
                    node.left.parent = node.parent
                    node = node.left
                else:  # if node.right:
                    node.parent.left = node.right
                    node.right.parent = node.parent
                    node = node.right
            return node

        # if node has 2 children
        else:
            succ = self.findSuccessor(node)
            succ.left = node.left
            node.left.parent = succ
            if succ is not node.right:
                succ.parent.left = succ.right
                if succ.right:
                    succ.right.parent = succ.parent
                succ.right = node.right
                node.right.parent = succ
            if node.parent != None:
                if node.parent.value > succ.value:
                    node.parent.left = succ
                    succ.parent = node.parent
                else:
                    node.parent.right = succ
                    succ.parent = node.parent
            if node.parent == None:
                self.root = succ
                succ.parent = None
            if succ.right:
                return self.findSuccessor(succ)
            else:
                return succ

        return False

    def rem_rightrotation(self, root):
        """HELPER FUNCTION: right rotation for remove method"""
        child = root.left
        T3 = child.right

        #updates the pointer
        if child.right != None:
            child.right.parent = root

        # Perform rotation
        child.right = root
        root.left = T3

        child.parent = root.parent
        if child.parent != None:
            if child.parent.value < child.value:
                child.parent.right = child
            else:
                child.parent.left = child
        else:
            self.root = child
        root.parent = child

        # Update heights
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right))

        return child

    def rem_leftrotation(self,root):
        """HELPER FUNCTION: left rotation for remove method"""

        child = root.right
        T2 = child.left

        # updates the pointer
        if child.left != None:
            child.left.parent = root

        # Perform rotation
        root.right = T2
        child.left = root

        child.parent = root.parent
        if child.parent != None:
            if child.parent.value < child.value:
                child.parent.right = child
            else:
                child.parent.left = child
        else:
            self.root = child
        root.parent = child

        # Update heights
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        child.height = 1 + max(self.getHeight(child.left), self.getHeight(child.right))

        return child

    def remove(self, value: object) -> bool:
        """
        TODO: Remove the value from the AVL tree.
        TODO: Returns True if value is removed from AVL Tree; otherwise return False.
        """

        """If node is properly removed, BST_removal method returns inorder successor node for height
         and balance factor to be properly updated, else it returns False."""
        root = self.BST_removal(value)

        #If BST_removal returns false, remove method returns False
        if root == False:
            return False

        #Else, height is updated and Balance factor is checked
        while root:
            root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
            balance = self.getBalance(root)

            """If the node is unbalanced, then try out the 4 cases"""
            # LL
            if balance > 1 and self.getBalance(root.left) >= 0:
                self.rem_rightrotation(root)

            # RR
            elif balance < -1 and self.getBalance(root.right) <= 0:
                self.rem_leftrotation(root)

            # LR
            elif balance > 1 and self.getBalance(root.left) < 0:
                root.left = self.rem_leftrotation(root.left)
                self.rem_rightrotation(root)

            # RL
            elif balance < -1 and self.getBalance(root.right) > 0:
                root.right = self.rem_rightrotation(root.right)
                self.rem_leftrotation(root)

            root = root.parent

        return True






    def contains(self, value: object) -> bool:
        """
        TODO: Returns True if the value parameter is in the tree or False if it is not. If the tree
        TODO: is empty, the method returns False.
        """

        currentnode = self.root
        while currentnode:
            if currentnode.value == value:
                return True
            elif currentnode.value < value:
                currentnode = currentnode.right
            else:
                currentnode = currentnode.left
        return False

    def inorder_traversal(self) -> Queue:
        """
        TODO: Returns queue of inorder traversal of the tree.
        TODO: If the tree is empty, the methods returns an empty Queue.
        """

        root = self.root
        queue = Queue()                 #creates empty queue

        self.inorder(root, queue)       #passes root and queue to helper function
        return queue

    def inorder(self, root, queue):
        """HELPER FUNCTION: Visits the nodes inorder traversal,
        and adds the nodes to the queue recursively."""

        if root:
            self.inorder(root.left, queue)
            queue.enqueue(root.value)
            self.inorder(root.right, queue)

    def find_min(self) -> object:
        """
        TODO: Returns lowest value in the tree. If the tree is empty the method
        TODO: returns None.
        """
        if self.root == None:
            return None

        currentnode = self.root
        while currentnode.left:
            currentnode = currentnode.left
        return currentnode.value

    def find_max(self) -> object:
        """
        TODO: Returns highest value in the tree. If the tree is empty the method
        TODO: returns None.
        """

        if self.root == None:
            return None

        currentnode = self.root
        while currentnode.right:
            currentnode = currentnode.right
        return currentnode.value

    def is_empty(self) -> bool:
        """
        TODO: Returns True if the tree is empty, otherwise returns False.
        """
        if self.root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        TODO: Removes all of the nodes from the tree.
        """
        self.root = None


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    """print("\nPDF - method remove() nargis ex")
    print("-------------------------------")
    case = ([-61, 70, -88, -51])
    avl = AVL([-61, -92, 70, -58, -88, 75, -51, 15, 86, -8])
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)"""


    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        avl = AVL(case)
        print(avl)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        avl = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', avl)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL()
        for value in case:
            avl.add(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)
    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)
    for _ in case[:-2]:
        print('INPUT  :', avl, avl.root.value)
        avl.remove(avl.root.value)
        print('RESULT :', avl)


    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        for value in case[::2]:
            avl.remove(value)
        if not avl.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
