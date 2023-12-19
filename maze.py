import random


def _generate_iterator(start, stop, n):
    num = 0
    if start < stop:
        while num < n:
            yield num
            num += 1
    else:
        while -1 * num < n:
            yield num
            num -= 1


class Maze:
    class Point:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def get_pos(self):
            return (self.x, self.y)

    class Position:
        def __init__(self, x, y, sensor):
            self.x = x
            self.y = y
            self.sensor = []
            self.xy = []

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

    def __init__(self, size):
        self.size = size
        self.maze = [[0] * size for i in range(size)]
        self.goal = self.Point()
        self.start = self.Point()
        self.last_moves = []
        self.last_distance = 1000000

    def len_to_point(self, p1, p2):
        """Calcualte distance between p1 and p2"""
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def generate_maze(self, p):
        if p.y - 1 == self.start.y and p.x == self.start.x:
            return
        x_h = p.x + 1 if p.x < self.size - 1 else p.x
        x_l = p.x - 1 if p.x > 0 else p.x
        y_h = p.y + 1 if p.y < self.size - 1 else p.y
        y_l = p.y - 1 if p.y > 0 else p.y
        possible_moves = [
            self.Point(x_h, p.y),
            self.Point(x_l, p.y),
            self.Point(p.x, y_l),
            self.Point(p.x, y_h),
        ]
        remove_moves = []
        add_moves = []
        for move in possible_moves:
            if self.maze[move.y][move.x] == 2:
                remove_moves.append(move)
            elif self.maze[move.y][move.x] == 3:
                remove_moves.append(move)
            elif move in self.last_moves:
                remove_moves.append(move)
            elif self.len_to_point(move, self.start) <= self.last_distance:
                add_moves.append(move)
        possible_moves.extend(add_moves)
        possible_moves = [move for move in possible_moves if move not in remove_moves]
        if possible_moves == []:
            possible_moves = self.last_moves[0:2]
        choice = random.choice(possible_moves)
        self.maze[choice.y][choice.x] = 1
        self.last_distance = self.len_to_point(choice, self.start)
        self.last_moves.append(choice)
        if len(self.last_moves) > 5:
            self.last_moves = self.last_moves[1:]
        self.generate_maze(choice)

    def generate(self):
        """Create random maze with size 'size'."""

        def gen_rand():
            return random.choice(range(self.size))

        # Generate start:
        self.start.x = gen_rand()
        self.maze[0][self.start.x] = 2  # "S"

        # Generate goal:
        self.goal = self.Point(gen_rand(), gen_rand())
        while (
            self.start == self.goal
            or self.len_to_point(self.start, self.goal) < self.size
            or self.len_to_point(self.start, self.goal) > self.size * 1.5
        ):
            self.goal = self.Point(gen_rand(), gen_rand())
        self.maze[self.goal.y][self.goal.x] = 3  # "G"
        self.generate_maze(self.goal)

    def generate_walls(self):
        possible_walls = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 0:
                    possible_walls.append((i, j))
        possible_walls = random.sample(possible_walls, k=len(possible_walls))
        for i in range((int(self.size * self.size / 2 + self.size * self.size / 13))):
            y, x = possible_walls[i]
            self.maze[y][x] = 1

    def get_view(self, x, y):
        sensor = [0, 0, 0, 0]  # top , right, down, left
        xy = []
        if x < self.size - 1:
            sensor[1] = self.maze[y][x + 1]
        if x > 0:
            sensor[3] = self.maze[y][x - 1]
        if y < self.size - 1:
            sensor[2] = self.maze[y + 1][x]
        if y > 0:
            sensor[0] = self.maze[y - 1][x]
        if sensor[0] not in [0, 5, 2]:
            if sensor[0] == 3:
                return [(x, y - 1)]
            xy.append((x, y - 1))
        if sensor[1] not in [0, 5, 2]:
            if sensor[1] == 3:
                return [(x + 1, y)]
            xy.append((x + 1, y))
        if sensor[2] not in [0, 5, 2]:
            if sensor[2] == 3:
                return [(x, y + 1)]
            xy.append((x, y + 1))
        if sensor[3] not in [0, 5, 2]:
            if sensor[3] == 3:
                return [(x - 1, y)]
            xy.append((x - 1, y))
        xy = random.sample(xy, k=len(xy))
        return xy

    def display(self):
        print(f"Start: {(self.start.x, self.start.y)}")
        print(f"Goal: {(self.goal.x, self.goal.y)}")
        print(f"---- Maze ----")
        for i in range(len(self.maze)):
            print(self.maze[i])


def get_maze():
    maze = Maze(100)
    maze.generate()
    maze.generate_walls()
    return maze
