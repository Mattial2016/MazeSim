import time
import sys

sys.setrecursionlimit(10**6)

def current_millis():
    return round(time.time() * 1000)


class Player:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze

    def get_view(self):
        return self.maze.get_view(self.x, self.y)

    def check_win(self):
        return self.x == self.maze.goal.x and self.y == self.maze.goal.y


class DepthFirst:
    def __init__(self, pl):
        self.pl = pl
        self.nbr_moves = 0
        self.pos = []
        self.visited = []
        self.visited_order = []

    def run(self):
        while self.stack != [] and not self.pl.check_win():
            xy = self.stack.pop()
            self.pl.x, self.pl.y = xy
            positions = self.pl.get_view()
            for pos in positions:
                if pos not in self.visited:
                    x, y = pos
                    if self.pl.maze.maze[y][x] != 2 and self.pl.maze.maze[y][x] != 3:
                        self.pl.maze.maze[y][x] = 5
                    self.stack.append(pos)
                    self.pl.x, self.pl.y = pos
                    self.nbr_moves += 1
                    self.visited_order.append(pos)
                    win = self.pl.check_win()
                    win = True if self.pl.check_win() else self.run()
                    self.visited.append(pos)
                    if win:
                        return True
        return self.pl.check_win()

    def init(self):
        start_time = current_millis()
        self.stack = []
        self.visited = []
        current = (self.pl.x, self.pl.y)
        self.visited.append(current)
        self.stack.append(current)
        self.run()
        finish_time = current_millis()
        print("---------Depth First ---------")
        print(f"Total time: {finish_time-start_time}")
        print(f"Total nbr of moves: {self.nbr_moves}")


class FloodGate:
    def __init__(self, pl):
        self.pl = pl
        self.pos = []
        self.nbr_moves = 0
        self.visited = []
        self.visited_order = []
        self.stack = [(pl.x, pl.y)]


    def _dist(self, p):
        x, y = p
        return abs(x-self.pl.maze.goal.x) + abs(y-self.pl.maze.goal.y)
        
    def run(self):
        while not self.pl.check_win():
            pos = self.stack.pop()
            while pos in self.visited:
                pos = self.stack.pop()
            self.pl.x, self.pl.y = pos
            self.visited.append(pos)
            self.visited_order.append(pos)
            self.nbr_moves += 1
            if self.pl.check_win():
                return True
            self.stack.extend(self.pl.get_view())
            self.stack = sorted(self.stack, reverse=True, key=self._dist)

    def init(self):
        start_time = current_millis()
        while self.stack != []:
            if self.run():
                break
        finish_time = current_millis()
        print("---------Flood Gate ---------")
        print(f"Total time: {finish_time-start_time}")
        print(f"Total nbr of moves: {self.nbr_moves}")


class BreadthFirst:
    def __init__(self, pl):
        self.pl = pl
        self.nbr_moves = 0
        self.pos = []
        self.visited = []
        self.visited_order = []
        self.stack = [(pl.x, pl.y)]

    def run(self):
        for pos in self.stack:
            if pos in self.visited:
                continue
            self.pl.x, self.pl.y = pos
            self.visited.append(pos)
            self.visited_order.append(pos)
            self.nbr_moves += 1
            if self.pl.check_win():
                return True
            self.stack.extend(self.pl.get_view())

    def init(self):
        start_time = current_millis()
        while self.stack != []:
            if self.run():
                break
        finish_time = current_millis()
        print("---------Breadth First ---------")
        print(f"Total time: {finish_time-start_time}")
        print(f"Total nbr of moves: {self.nbr_moves}")
