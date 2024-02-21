avl.py:
Complete the AVL tree implementation to improve on the binary search tree by always guaranteeing the tree is height balanced, which allows for more efficient operations.  

hash_map.py:
Architecture: Use a dynamic array (provided as DynamicArray class) to store the hash table and a singly linked list (provided as LinkedList class) for chaining collisions. Chains of key/value pairs will be stored in linked list nodes.

DynamicArray and LinkedList: Utilize objects of the provided DynamicArray and LinkedList classes in your HashMap implementation. The DynamicArray stores the hash table, and LinkedList stores chains of key/value pairs.

Functionality: Review the docstrings in the provided classes to understand available methods, their usage, and input/output parameters. The provided classes may have different functionality from prior assignments or lectures.

HashMap Size: The number of objects stored in the HashMap will range between 0 and 1,000,000 inclusive.

Hash Functions: Test your code with two pre-written hash functions provided in the skeleton code. These functions will be used in testing your implementation.

Restrictions: You are not allowed to use any built-in Python data structures or their methods. Direct access to variables of the DynamicArray or LinkedList classes is prohibited. All operations must be performed using class methods. Variables in the HashMap and SLNode classes are not private and can be accessed and modified directly. No additional imports beyond those provided in the assignment source code are permitted.
