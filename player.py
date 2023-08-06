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

    def run2(self):
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
                    win = self.pl.check_win()
                    if not win:
                        win = self.run2()
                        self.visited.append(pos)
                        if win:
                            return True
                    else:
                        print("win")
                        return True
        return self.pl.check_win()
    def init2(self):
        self.stack = []
        self.visited = []
        current = (self.pl.x, self.pl.y)
        self.visited.append(current)
        self.stack.append(current)
        self.run2()
