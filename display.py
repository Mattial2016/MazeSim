import os
import time
import math
import copy

os.environ["SDL_AUDIODRIVER"] = "dsp"

import pygame as pg
import maze
import player


def current_millis():
    return round(time.time() * 1000)


class Display:
    def __init__(self, maze):
        self.maze = maze
        pg.init()
        self.screen_size = 1000
        self.size = self.screen_size / len(self.maze[0])
        self.screen = pg.display.set_mode((self.screen_size, self.screen_size))
        pg.display.set_caption("Maze")
        self.p = p_dfs
        self.exit = False
        self.first = False
        self.nbr_painted = 0
        self.n = 0

    def start(self):
        while not self.exit:
            self.run()

    def run(self):
        def animate():
            if self.p.visited_order != []:
                x, y = self.p.visited_order[0]
                self.p.visited_order = (
                    [] if len(self.p.visited_order) <= 1 else self.p.visited_order[1:]
                )
                if self.maze[y][x] in [2, 3]:
                    return
                rect = pg.Rect(self.size * x, self.size * y, self.size, self.size)
                pg.draw.rect(
                    self.screen,
                    pg.Color(
                        self.nbr_painted,
                        255 - self.nbr_painted,
                        255 - int(self.nbr_painted / 2),
                    ),
                    rect,
                )
                self.n += 1
                if self.n % int(math.ceil(self.p.nbr_moves / 255)) == 0:
                    self.nbr_painted += 1
                    self.n = 0
                if self.nbr_painted == 255:
                    self.nbr_painted = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit = True
        if not self.first:
            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    rect = pg.Rect(self.size * j, self.size * i, self.size, self.size)
                    if self.maze[i][j] == 0:
                        pg.draw.rect(self.screen, pg.Color(100, 40, 150), rect)
                    if self.maze[i][j] == 1:
                        pg.draw.rect(self.screen, pg.Color(0, 0, 0), rect)
                    if self.maze[i][j] == 2:
                        pg.draw.rect(self.screen, pg.Color(150, 0, 0), rect)
                    if self.maze[i][j] == 3:
                        pg.draw.rect(self.screen, pg.Color(0, 255, 0), rect)
            self.first = True
        last = current_millis()
        current = last
        while current - last < 5:
            current = current_millis()
        animate()

        def reset_display():
            self.first = False
            self.n = 0
            self.nbr_painted = 0
            self.screen.fill((0, 0, 0))

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.exit = True
        if keys[pg.K_a]:  # Breadth First
            self.p = p_bfs
            self.p.visited_order = p_visited_backup_bfs
            reset_display()
        if keys[pg.K_d]:  # Depth First
            self.p = p_dfs
            self.p.visited_order = p_visited_backup_dfs
            reset_display()
        pg.display.update()


maze_dfs = maze.get_maze()
maze_bfs = copy.deepcopy(maze_dfs)

pl_dfs = player.Player(maze_dfs.start.x, maze_dfs.start.y, maze_dfs)
pl_bfs = player.Player(maze_bfs.start.x, maze_bfs.start.y, maze_bfs)

p_dfs = player.DepthFirst(pl_dfs)
p_bfs = player.BreadthFirst(pl_bfs)

p_dfs.init()
p_bfs.init()

p_visited_backup_dfs = [p for p in p_dfs.visited_order]
p_visited_backup_bfs = [p for p in p_bfs.visited_order]

display = Display(maze_dfs.maze)
display.start()
