import time


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
        print(f"Total time: {finish_time-start_time}")
        print(f"Total nbr of moves: {self.nbr_moves}")


class BreadthFirst:
    def __init__(self, pl):
        self.pl = pl
        self.nbr_moves = 0
        self.pos = []
        self.visited = []
        self.visited_order = []

    def run(self, depth):
        if depth == 0:
            return False
        positions = self.pl.get_view()
        self.stack.extend(positions)
        for pos in positions:
            x, y = pos
            if self.pl.maze.maze[y][x] not in [2, 3]:
                print(f"added {(x, y)}")
                self.pl.maze.maze[y][x] = 5
            self.nbr_moves += 1
            self.pl.x, self.pl.y = pos
            self.stack.remove(pos)
            if self.pl.check_win():
                return True
        self.visited.extend(positions)
        for pos in positions:
            if self.run(depth - 1):
                return True

    def init(self):
        start_time = current_millis()
        self.stack = []
        self.visited = []
        current = (self.pl.x, self.pl.y)
        self.visited.append(current)
        self.stack.append(current)
        depth = 0
        while self.stack != [] and not self.pl.check_win():
            self.run(depth)
            depth += 1
        finish_time = current_millis()
        print(f"Total time: {finish_time-start_time}")
        print(f"Total nbr of moves: {self.nbr_moves}")
