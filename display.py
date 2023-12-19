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
        self.p_dfs = p_dfs
        self.p_bfs = p_bfs
        self.p_fg = p_fg
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
            self.draw_maze()
            self.first = True
        last = current_millis()
        current = last
        while current - last < 2:
            current = current_millis()
        animate()

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.exit = True
        if keys[pg.K_a]:  # Breadth First
            self.maze = self.backup_maze
            self.p = self.p_bfs
            self.p.visited_order = p_visited_backup_bfs
            self.reset_display()
        if keys[pg.K_d]:  # Depth First
            self.maze = self.backup_maze
            self.p = self.p_dfs
            self.p.visited_order = p_visited_backup_dfs
            self.reset_display()
        if keys[pg.K_s]:  # Flood Gate
            self.maze = self.backup_maze
            self.p = self.p_fg
            self.p.visited_order = p_visited_backup_fg
            self.reset_display()
        if keys[pg.K_f]:  # Draw Maze
            self.reset_display()
            (self.p_dfs, self.p_bfs, self.p_fg) = self.clean_display_for_drawing()
            self.p = self.p_dfs
            print(f"----------- Changed Maze -----------\n")
        pg.display.update()

    def reset_display(self):
        self.first = False
        self.n = 0
        self.nbr_painted = 0
        self.screen.fill((0, 0, 0))

    def draw_maze(self):
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

    def clean_display_for_drawing(self):
        self.backup_maze = self.maze
        sx, sy = maze_dfs.start.get_pos()
        gx, gy = maze_dfs.goal.get_pos()
        self.maze = [[1] * maze_dfs.size for i in range(maze_dfs.size)]
        self.maze[sy][sx] = 2
        self.maze[gy][gx] = 3
        self.draw_maze()
        pg.display.update()
        pg.event.get()
        m1, m2, m3 = pg.mouse.get_pressed()
        i = 0
        while not m3:
            pg.event.get()
            m1, m2, m3 = pg.mouse.get_pressed(num_buttons=3)
            x, y = pg.mouse.get_pos()
            # print(f"{(m1, m2, m3)}, {(x, y)}, {maze_dfs.size}, {(int(x/self.size), int(y/self.size))}, {(gx, gy)}")
            if m1:
                x = int(x / self.size)
                y = int(y / self.size)
                self.maze[y][x] = 0
                if x > 0:
                    self.maze[y][x - 1] = 0
                if y > 0:
                    self.maze[y - 1][x] = 0

            i = i + 1
            if i > 2000:
                i = 0
                self.draw_maze()
                pg.display.update()

        # Reset the players to the new maze:
        maze_dfs.maze = self.maze
        maze_bfs = copy.deepcopy(maze_dfs)
        maze_fg = copy.deepcopy(maze_dfs)

        pl_dfs = player.Player(maze_dfs.start.x, maze_dfs.start.y, maze_dfs)
        pl_bfs = player.Player(maze_bfs.start.x, maze_bfs.start.y, maze_bfs)
        pl_fg = player.Player(maze_fg.start.x, maze_fg.start.y, maze_fg)

        p_dfs = player.DepthFirst(pl_dfs)
        p_bfs = player.BreadthFirst(pl_bfs)
        p_fg = player.FloodGate(pl_fg)

        p_dfs.init()
        p_bfs.init()
        p_fg.init()

        p_visited_backup_dfs = p_dfs.visited_order
        p_visited_backup_bfs = p_bfs.visited_order
        p_visited_backup_fg = p_fg.visited_order
        return (p_dfs, p_bfs, p_fg)


maze_dfs = maze.get_maze()
maze_bfs = copy.deepcopy(maze_dfs)
maze_fg = copy.deepcopy(maze_dfs)

pl_dfs = player.Player(maze_dfs.start.x, maze_dfs.start.y, maze_dfs)
pl_bfs = player.Player(maze_bfs.start.x, maze_bfs.start.y, maze_bfs)
pl_fg = player.Player(maze_fg.start.x, maze_fg.start.y, maze_fg)

p_dfs = player.DepthFirst(pl_dfs)
p_bfs = player.BreadthFirst(pl_bfs)
p_fg = player.FloodGate(pl_fg)

p_dfs.init()
p_bfs.init()
p_fg.init()

p_visited_backup_dfs = p_dfs.visited_order
p_visited_backup_bfs = p_bfs.visited_order
p_visited_backup_fg = p_fg.visited_order

display = Display(maze_dfs.maze)
display.start()
