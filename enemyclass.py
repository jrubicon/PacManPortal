import pygame as pg
from settings import *
import random
vect = pg.math.Vector2


class Enemy:
    def __init__(self, game, pos, num):
        self.game = game
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pixel_pos = self.get_pix_pos()
        self.num = num
        #self.radius = self.game.cellwidth//2-1
        self.color = self.set_color()
        self.direction = vect(0,0)
        self.ghosttype = self.set_personality()
        self.target = None
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pixel_pos += self.direction * self.speed
            if self.move_time():
                self.move()
        #set grid in ref to pixel pos
        self.grid_pos[0] = (self.pixel_pos[0]-55+self.game.cellwidth//2)//self.game.cellwidth+1
        self.grid_pos[1] = (self.pixel_pos[1]-55+self.game.cellheight//2)//self.game.cellheight+1

    def set_speed(self):
        if self.ghosttype in ["speedy", "scared"]:
            speed = 4
        else:
            speed = 5
        return speed

    def set_target(self):
        if self.ghosttype == "speedy" or self.ghosttype == "slow":
            return self.game.player.grid_pos
        else:
            if self.game.player.grid_pos[0] > COLS//2 and self.game.player.grid_pos[1] > ROWS//2:
                return vect(1, 1)
            if self.game.player.grid_pos[0]> COLS//2 and self.game.player.grid_pos[1] < ROWS//2:
                return vect(1, ROWS-2)
            if self.game.player.grid_pos[0] < COLS//2 and self.game.player.grid_pos[1] > ROWS//2:
                return vect(COLS-2, 1)
            else:
                return vect(COLS-2, ROWS-2)

    def draw(self):
        pg.draw.circle(self.game.screen, self.color,(int(self.pixel_pos.x), int(self.pixel_pos.y)), self.game.cellwidth//2-1)

    def get_pix_pos(self):
        return vect((self.grid_pos[0] * self.game.cellwidth) + 50 // 2 + self.game.cellwidth // 2,
                    (self.grid_pos[1] * self.game.cellheight) + 50 // 2 + self.game.cellheight // 2)

    def set_color(self):
        if self.num == 0:
            return (43, 78, 203)
        if self.num == 1:
            return (197, 200, 27)
        if self.num == 2:
            return (189, 29, 29)
        if self.num == 3:
            return (215, 159, 33)

    def set_personality(self):
        if self.num == 0:
            return "speedy"
        if self.num == 1:
            return "slow"
        if self.num == 2:
            return "random"
        if self.num == 3:
            return "scared"

    def move_time(self):
        if int(self.pixel_pos.x+50//2) % self.game.cellwidth == 0:
            if self.direction == vect(1,0) or self.direction == vect(-1,0) or self.direction == vect(0,0) or self.direction == vect(0,0):
                return True
        if int(self.pixel_pos.y+50//2) % self.game.cellheight == 0:
            if self.direction == vect(0,1) or self.direction == vect(0,-1) or self.direction == vect(0,0) or self.direction == vect(0,0):
                return True
        return False

    def move(self):
        if self.ghosttype == "random":
            self.direction = self.get_random_direction()
        if self.ghosttype == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.ghosttype == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.ghosttype == "scared":
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vect(xdir, ydir)

    def find_next(self, target):
        path = self.breathfs([int(self.grid_pos.x), int(self.grid_pos.y)],
                             [int(target[0]), int(target[1])])
        return path[1]

    def breathfs(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.game.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1],[1,0],[0,1],[-1,0]]
                for neighbor in neighbors:
                    if neighbor[0]+current[0] >= 0 and neighbor[0] + current[0] < len(grid[0]):
                        if neighbor[1]+current[1] >= 0 and neighbor[1] + current[1] < len(grid):
                            next_cell = [neighbor[0] + current[0], neighbor[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next":next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2,1)
            if number == -2:
                xdir, ydir = 1, 0
            elif number == -1:
                xdir, ydir = 0, 1
            elif number == 0:
                xdir, ydir = -1, 0
            else:
                xdir, ydir = 0, -1
            next_pos = vect(self.grid_pos.x + xdir, self.grid_pos.y +ydir)
            if next_pos not in self.game.walls:
                break
        return vect(xdir, ydir)
