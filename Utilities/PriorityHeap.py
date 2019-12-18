class Node:
    """
    Node definition should not be changed in any way
    """
    __slots__ = ['_key', '_value']

    def __init__(self, k, v):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self._key = k
        self._value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False if otherwise
        """
        return self._key < other.get_key() or (self._key == other.get_key() and self._value < other.get_value())

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False if otherwise
        """
        return self._key > other.get_key() or (self._key == other.get_key() and self._value > other.get_value())

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False if otherwise
        """
        return self._key == other.get_key() and self._value == other.get_value()

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0},{1})'.format(self._key, self._value)

    __repr__ = __str__

    def get_key(self):
        """
        Key getter function
        :return: key value of the node
        """
        return self._key

    def set_key(self, new_key):
        """
        Key setter function
        :param new_key: the value the key is to be changed to
        """
        self._key = new_key

    def get_value(self):
        """
        Value getter function
        :return: value of the node
        """
        return self._value


class PriorityHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = '_data'

    def __init__(self):
        """
        Initializes the priority heap
        """
        self._data = []

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self._data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self._data)

    __repr__ = __str__


    def all_mins(self):
        """

        :return:
        """
        num_mins = 0
        priority = self.__data[0].get_key()

        for i in range(len(self)):
            if self._data[i].get_key() != priority:
                break
            num_mins += 1

        return num_mins


    def empty(self):
        """
        Finds if heap is empty
        :return: True if empty and False if not
        """
        return True if len(self) == 0 else False

    def top(self):
        """
        Minimum value in the min heap
        :return: value of the top element of the heap
        """
        # if not empty
        if not self.empty():
            return self._data[0].get_value()
        # if empty
        return None

    def push(self, key, val):
        """
        Adds an element to the heap
        :param key: key of node
        :param val: value of node
        :return: None
        """
        # create new node and add to data
        new_ele = Node(key, val)
        self._data.append(new_ele)
        # percolate number into correct place
        self.percolate_up(len(self)-1)

    def pop(self):
        """
        Removes minimum element of the heap
        :return: returns Node of removed element
        """
        # if not empty
        if not self.empty():
            # swap min element with last and pop from data
            popped = self._data[0]
            self.swap(0, len(self)-1)  # swap elements
            self._data.pop()
            # move swapped node to correct place
            self.percolate_down(0)

            return popped.get_value()
        # if empty
        return None

    def min_child(self, index):
        """
        Finds the minimum child of the index
        :param index: index within the heap array
        :return: index of the minimum element
        """
        # left and right child
        left = self._data[(index*2)+1] if (index*2)+1 < len(self) else None
        right = self._data[(index*2)+2] if (index*2)+2 < len(self) else None

        # if has both children
        if left and right:
            if left > right:
                return (index*2)+2
            return (index*2)+1

        # if only has left child
        elif left and right is None:
            return (index*2)+1

        # if only has right child
        elif right and left is None:
            return (index*2)+2

        # no children
        return None


    def percolate_up(self, index):
        """
        Moves node at index up to correct position in it's branch
        :param index: index of node to percolate up
        :return: None
        """
        # reached root
        if index == 0:
            return

        p_ind = (index-1)//2
        # swap if parent is larger than current and continue percolating
        if self._data[p_ind] > self._data[index]:
            self.swap(p_ind, index)
            self.percolate_up(p_ind)


    def percolate_down(self, index):
        """
        Moves node down to correct position in tree
        :param index: index of node to percolate down
        :return: None
        """
        child = self.min_child(index)

        # swap if child is less than current and continue percolating
        if child and self._data[child] < self._data[index]:
            self.swap(child, index)
            self.percolate_down(child)

    def change_priority(self, index, new_key):
        """
        Changes the key of the node at index
        :param index: node to change key of
        :param new_key: new key to change to
        :return: None
        """
        # if index is within array
        if index < len(self):
            old_key = self._data[index].get_key()
            self._data[index].set_key(new_key)

            # if new key is greater than old key
            if new_key > old_key:
                self.percolate_down(index)
            # if new key is less than old key
            elif new_key < old_key:
                self.percolate_up(index)


    def swap(self, x, y):
        """
        Swapping item at index x and y
        :param x: first argument to swap
        :param y: second argument to swap
        :return:
        """
        self._data[x], self._data[y] = self._data[y], self._data[x]

    def find_index(self, vertex):
        for i in range(len(self._data)):
            if self._data[i].get_value() == vertex:
                return i

    def remove_top(self):
        """

        """
        popped = self.pop()
        # remove in edge incident from out edge destination
        for ele in popped.all_out_edges():
            dest = ele.get_dest()
            # dest.delete_in_edge(popped)
            #
            # self.change_priority()
            #
        return popped.get_value()
