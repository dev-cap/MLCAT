"""
    This module is an implementation of the Union Find algorithm with path compression.
    The union-find data structure is also called a disjoint-set data structure.
    Union with path compression approach:
    Each node visited on the way to a root node may as well be attached
    directly to the root node.
    attach the smaller tree to the root of the larger tree
    Time Complexity  :  O(a(n)), where a(n) is the inverse of the function
    n=f(x)=A(x,x) and A is the extremely fast-growing Ackermann function
    
    .. note:: Source: https://github.com/nryoung/algorithms/blob/master/algorithms/data_structures/union_find_with_path_compression.py
"""


class UnionFind:
    def __init__(self, N):
        if type(N) != int:
            raise TypeError("size must be integer")
        if N < 0:
            raise ValueError("N cannot be a negative integer")
        self.__parent = []
        self.__rank = []
        self.__N = N
        for i in range(0, N):
            self.__parent.append(i)
            self.__rank.append(0)

    def make_set(self, x):
        """
        Create a set with x as the only element.

        :param x: An  integer that would be the singleton element of the newly created set
        """
        if type(x) != int:
            raise TypeError("x must be integer")
        if x != self.__N:
            raise ValueError(
                "a new element must have index {0}".format(self.__N))
        self.__parent.append(x)
        self.__rank.append(0)
        self.__N = self.__N + 1

    def union(self, x, y):
        """
        Merge x's set with y's set

        :param x: An integer whose set you want to merge
        :param y: Another integer whose set you want to merge        
        """
        self.__validate_ele(x)
        self.__validate_ele(y)
        x_root = self.__find(x)
        y_root = self.__find(y)
        if x_root == y_root:
            return
        # x and y are not already in same set. Merge them
        if self.__rank[x_root] < self.__rank[y_root]:
            self.__parent[x_root] = y_root
        elif self.__rank[x_root] > self.__rank[y_root]:
            self.__parent[y_root] = x_root
        else:
            self.__parent[y_root] = x_root
            self.__rank[x_root] = self.__rank[x_root] + 1

    def __find(self, x):
        """
        Find which set x belongs to

        :param x: An integer whose set you want to merge
        :return: The outermost parent set to which x belongs       
        """
        if self.__parent[x] != x:
            self.__parent[x] = self.__find(self.__parent[x])
        return self.__parent[x]

    def find(self, x):
        """
        Helper function to find which set x belongs to

        :param x: An integer whose set you want to merge
        :return: The outermost parent set to which x belongs       
        """
        self.__validate_ele(x)
        if self.__parent[x] == x:
            return x
        else:
            return self.find(self.__parent[x])

    def is_connected(self, x, y):
        """
        Check if the sets of x and y are connected in the disjoint set data structure

        :return: True if if x and y are connected     
        """
        self.__validate_ele(x)
        self.__validate_ele(y)
        return self.find(x) == self.find(y)

    def parent(self, x):
        """
        Used for unit testing check if the path is compressed
        """
        return self.__parent[x]

    def __validate_ele(self, x):
        """
        Checks if x is an Integer in the range of 0 to N, N not inclusive
        """
        if type(x) != int:
            raise TypeError("{0} is not an integer".format(x))
        if x < 0 or x >= self.__N:
            raise ValueError("{0} is not in [0,{1})".format(x, self.__N))