#https://github.com/Joseph94m/The-game-of-life/blob/master/The%20game%20of%20life.ipynb
import time
class Game:
    def __init__(self, initial_state, rules,max_size):
        self.initial_state = initial_state
        self.rules = rules
        self.max_size = max_size
    def run_game(self, it):
        state = self.initial_state
        previous_state = None
        progression = []
        i = 0
        while (not state.equals(previous_state) and i < it):
            curr = time.time()
            i += 1
            previous_state = state.copy()
            progression.append(previous_state.grid)
            state = state.apply_rules(self.rules,self.max_size)
            print("iter:{} Time needed: {}".format(i,time.time()-curr))
        progression.append(state.grid)
        return progression