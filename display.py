import os
import time

os.environ["SDL_AUDIODRIVER"] = "dsp"

import pygame as pg
import maze
import player


class Display:
    def __init__(self, maze):
        self.maze = maze
        pg.init()
        self.size = 1000
        self.screen = pg.display.set_mode((self.size, self.size))
        pg.display.set_caption("Maze")
        self.exit = False

    def start(self, df):
        while not self.exit:
            self.run(df)

    def run(self, df):
        def animate():
            if df.visited != []:
                x, y = df.visited.pop()
                if self.maze[y][x] !=2 and self.maze[y][x] !=3:
                    self.maze[y][x] = 6

        def current_millis():
            return round(time.time() * 1000)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit = True
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
                if self.maze[i][j] == 6:
                    pg.draw.rect(self.screen, pg.Color(255, 0, 100), rect)
        last = current_millis()
        current = last
        while current - last < 5:
            current = current_millis()
        animate()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.exit = True
        #if keys[pg.K_s]:
        #    last = current_millis()
        #    current = last
        #    while current - last < 40:
        #        current = current_millis()
        #    animate()
        pg.display.update()


_maze = maze.get_maze()
display = Display(_maze.maze)
pl = player.Player(_maze.start.x, _maze.start.y, _maze)
df = player.DepthFirst(pl)
df.init2()
display.start(df)
