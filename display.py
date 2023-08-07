import os
import time
import math

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
        self.size = 1000
        self.screen = pg.display.set_mode((self.size, self.size))
        pg.display.set_caption("Maze")
        self.exit = False
        self.first = False
        self.nbr_painted = 0
        self.n = 0

    def start(self, p):
        self.nbr_moves = int(math.ceil(p.nbr_moves / 255))
        while not self.exit:
            self.run(p)

    def run(self, p):
        def animate():
            if p.visited_order != []:
                x, y = p.visited_order[0]
                if len(p.visited_order) > 1:
                    p.visited_order = p.visited_order[1:]
                else:
                    p.visited_order = []
                if self.maze[y][x] != 2 and self.maze[y][x] != 3:
                    self.maze[y][x] = 6
                    size = self.size / len(self.maze[y])
                    rect = pg.Rect(size * x, size * y, size, size)
                    pg.draw.rect(
                        self.screen,
                        pg.Color(
                            self.nbr_painted, 255 - self.nbr_painted, 255-int(self.nbr_painted/2)
                        ),
                        rect,
                    )
                    self.n += 1
                    if self.n >= self.nbr_moves:
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
                    size = self.size / len(self.maze[j])
                    rect = pg.Rect(size * j, size * i, size, size)
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
        while current - last < 15:
            current = current_millis()
        animate()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.exit = True
        # if keys[pg.K_s]:
        #    last = current_millis()
        #    current = last
        #    while current - last < 40:
        #        current = current_millis()
        #    animate()
        pg.display.update()


_maze = maze.get_maze()
display = Display(_maze.maze)
pl = player.Player(_maze.start.x, _maze.start.y, _maze)
p = player.DepthFirst(pl)
p.init()
display.start(p)
