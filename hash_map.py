# Name: Nargis Habibi
# OSU Email: habibin@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: Dec 3, 2021
# Description: Used Dynamic array to store my hashtable and implemented chaining for collision resolution using a single
# linkedlist. Chains of key/value pairs are stored in linkedlist nodes.

# import random

# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

#--------------------------------------------------------------------------------------------------------------

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """

        # created a new hashtable
        new_hash = HashMap(self.capacity, self.hash_function)

        # sets the old hashtable date members to new hashtables data members
        self.buckets = new_hash.buckets
        self.size = new_hash.size

    def ll_index(self, key):
        """
        TODO: Helper function: finds the linkedlist at the index where given key is stored
        """
        # finds the location of the index where key/value pair would be stored
        hash = self.hash_function(key)
        index = hash % self.capacity
        # returns the linkedlist at this index
        return self.buckets.get_at_index(index)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """
        #finds the linkedlist at the index where given key is stored
        ll = self.ll_index(key)

        #If node with matching key in the list, "contains" method will
        #return pointer to that node else it returns None
        pointer = ll.contains(key)
        if pointer:
            return pointer.value
        return pointer

    def put(self, key: str, value: object) -> None:
        """
        TODO: Updates the key/value pair in the hash map.
        """
        #finds the linkedlist at the index where given key is stored
        ll = self.ll_index(key)

        #if the length of ll at this index is not empty, it will remove the key/value if key is found.
        if ll.length() > 0:
            if ll.remove(key):
                self.size -= 1

        #insert the key/value pair to the linkedlist
        ll.insert(key, value)
        self.size += 1

    def remove(self, key: str) -> None:
        """
        TODO: removes the given key and its associated value from the hash map. If a given
        Todo: key is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        #finds the linkedlist at the index where given key is stored
        ll = self.ll_index(key)

        #if key/value is found in the linkedlist, node will be removed
        if ll.remove(key):
            self.size -= 1



    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.
        An empty hash map does not contain any keys.
        """
        if self.get(key) != None:
            return True
        return False

    def empty_buckets(self) -> int:
        """
        TODO: Returns the number of empty buckets in the hash table.
        """
        counter = 0
        #loops through each index, if length of linkedlist is 0 (empty), counter increases by 1
        for index in range(self.capacity):
            ll = self.buckets.get_at_index(index)
            if ll.length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        TODO: Load factor = size of table/ capacity of table
        """
        return self.size/ self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map and all hash table links must be rehashed.
        """
        if new_capacity < 1:
            return

        #created a new hashtable with new capacity
        new_hash = HashMap(new_capacity, self.hash_function)

        #populates the new hashtable with old hashtable nodes
        for index in range(self.capacity):
            ll = self.buckets.get_at_index(index)
            if ll.length() > 0:
                for node in ll:
                    new_hash.put(node.key, node.value)

        #sets the old hashtable date members to new hashtables data members
        self.capacity = new_capacity
        self.buckets = new_hash.buckets
        self.size = new_hash.size

    def get_keys(self) -> DynamicArray:
        """
        TODO: Returns a DynamicArray that contains all keys stored in your hash map.
        TODO: The order of the keys in the DA does not matter.
        """
        #created new Dynamic array list
        da = DynamicArray()

        #outer loops: loops through the hash table
        for index in range(self.capacity):
            ll = self.buckets.get_at_index(index)
            #inner loop: if linklist is not empty, iterates through each node and appends the key to da
            if ll.length() != 0:
                for node in ll:
                    da.append(node.key)
        return da


# BASIC TESTING
if __name__ == "__main__":

    """# sam_list = random.sample(range(300),10)
    # print(sam_list)
    #
    # sam_list1 = random.sample(range(300), 10)
    # print(sam_list1)
    #
    # print("\nPDF - get Nargis's ex")
    # print("-------------------")
    # m = HashMap(150, hash_function_2)
    # for i in sam_list:
    #     m.put(str(i), i)
    # print(m.size, m.capacity)
    # for i in sam_list1:
    #     print(i, m.get(str(i)), m.get(str(i)) == i)


    # print("\nPDF - contains_key nargis ex")
    # print("----------------------------")
    # m = HashMap(2, hash_function_2)
    # #keys = random.sample(range(100),10)
    # keys = [61, 60]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(keys)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)


    # # print("\nPDF - contains_key nargis ex")
    # # print("----------------------------")
    # m = HashMap(3, hash_function_2)
    # keys = random.sample(range(10),10)
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m)
    #
    # checkkeys = random.sample(range(10), 10)
    # for key in checkkeys:
    #     print(m.get(str(key)))
    #     print(key, m.contains_key(str(key)), key in keys)
    #     print('-------------------------------------------------')


    # print("\nPDF - contains_key nargis ex")
    # print("----------------------------")
    # m = HashMap(3, hash_function_2)
    # keys = [0,3,6,9]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m)
    # 
    # checkkeys = range(1)
    # for key in checkkeys:
    #     print(m.get(str(key)))
    #     print(key, m.contains_key(str(key)), key in keys)
    #     print('-------------------------------------------------')"""



    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)


    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    print('new_cap, m.contains_key, m.size, m.capacity, m.table_load')

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)
        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
