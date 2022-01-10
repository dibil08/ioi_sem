from abc import ABC, abstractmethod
from copy import copy

class State(ABC):
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def apply_rules(self, rules, max_size):
        pass

    @abstractmethod
    def equals(self, other):
        pass

    @abstractmethod
    def get_neighbours(self, elem, max_size):
        pass


class SparseSetState(State):
    def __init__(self, grid,lifePoints):
        self.grid = grid
        self.lifePoints=lifePoints

    def copy(self):
        return SparseSetState(copy(self.grid))

    def add_point(self,point):
        if(len(point)<3):
            point=point+(self.lifePoints,)
        self.grid[(point[0],point[1])]=self.lifePoints
        
    def add_points(self,points):
        map(self.add_points,points)
        
    def remove_point(self,point):
        self.grid.pop((point[0],point[1]),None)

    def clear_all(self):
        self.grid={}

    def get_neighbours(self, elem, max_size):
        # Returns the neighbours of a live cell if they lie within the bounds of the grid specified by max_size
        l = []
        if elem[0]-1 >= 0:
            l.append((elem[0]-1, elem[1]))
        if elem[0]-1 >= 0 and elem[1]-1 >= 0:
            l.append((elem[0]-1, elem[1]-1))
        if elem[0]-1 >= 0 and elem[1]+1 < max_size:
            l.append((elem[0]-1, elem[1]+1))
        if elem[1]-1 >= 0:
            l.append((elem[0], elem[1]-1))
        if elem[1]-1 >= 0 and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]-1))
        if elem[1]+1 < max_size:
            l.append((elem[0], elem[1]+1))
        if elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]))
        if elem[1]+1 < max_size and elem[0]+1 < max_size:
            l.append((elem[0]+1, elem[1]+1))
        return l

    def get_neighbours_withoutBorder(self, elem, max_size):
        # Returns the neighbours of a live cell if they lie within the bounds of the grid specified by max_size
        l = []
        l.append(((elem[0]-1)%max_size, (elem[1])%max_size))
        l.append(((elem[0]-1)%max_size, (elem[1]-1)%max_size))
        l.append(((elem[0]-1)%max_size, (elem[1]+1)%max_size))
        l.append(((elem[0])%max_size, (elem[1]-1)%max_size))
        l.append(((elem[0]+1)%max_size, (elem[1]-1)%max_size))
        l.append(((elem[0])%max_size, (elem[1]+1)%max_size))
        l.append(((elem[0]+1)%max_size, (elem[1])%max_size))
        l.append(((elem[0]+1)%max_size, (elem[1]+1)%max_size))
        return l

    def equals(self, other):
        if other is None:
            return False
        return self.grid == other.grid

    def apply_rules(self, rules, max_size):
        # Calls the actual rules and provides them with the grid and the neighbour function
        self.grid = rules.apply_rules(self.grid, max_size, self.get_neighbours_withoutBorder)
        return self