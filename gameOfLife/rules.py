
from abc import ABC, abstractmethod
import time
class Rule(ABC):
    @abstractmethod
    def apply_rules(self, grid, max_size, get_neighbours):
        pass


class DenseNumpyRules(Rule):
    def apply_rules(self, grid, max_size, get_neighbours):
        #copied_state = state.copy()
        #grid = state.grid

        grid_ret = copy(grid)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                nb = get_neighbours((i, j), max_size)
                counter = 0
                for n in nb:
                    if grid[n] == True:
                        counter += 1
                if (counter < 2 or counter > 3):
                    grid_ret[i][j] = False
                if (counter == 3):
                    grid_ret[i][j] = True
        return grid_ret


class SparseSetRules(Rule):
    def __init__(self,lifePoints):
        self.lifePoints=lifePoints
        
    def apply_rules(self, grid, max_size, get_neighbours):
        #grid = state.grid
        counter = {}
        for elem in grid:
            if elem not in counter:
                counter[elem] = 0
            nb = get_neighbours(elem, max_size)
            for n in nb:
                if n not in counter:
                    counter[n] = 1
                else:
                    counter[n] += 1
        for c in counter:
            point = (c[0],c[1])
            if (counter[c] < 2 or counter[c] > 3):                
                        grid.pop(point,None)
            if counter[c] == 3:
                grid[(c[0],c[1])]=self.lifePoints
        return grid
