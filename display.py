import os

os.environ["SDL_AUDIODRIVER"] = "dsp"

import pygame as pg
import maze


class Display:
    def __init__(self, maze):
        self.maze = maze
        pg.init()
        self.size = 1000
        self.screen = pg.display.set_mode((self.size, self.size))
        pg.display.set_caption("Maze")
        self.exit = False

    def start(self):
        while not self.exit:
            self.run()

    def run(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit = True
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                size = self.size / len(self.maze[j])
                rect = pg.Rect(size * j, size * i, size, size)
                if self.maze[i][j] == 0:
                    pg.draw.rect(self.screen, pg.Color(100, 40, 150), rect)
                if self.maze[i][j] == 2:
                    pg.draw.rect(self.screen, pg.Color(255, 0, 0), rect)
                if self.maze[i][j] == 3:
                    pg.draw.rect(self.screen, pg.Color(0, 255, 0), rect)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.exit = True
        pg.display.update()


display = Display(maze.get_maze())
display.start()
