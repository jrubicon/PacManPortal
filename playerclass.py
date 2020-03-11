import pygame as pg
from settings import *
vect = pg.math.Vector2


class Player:
    def __init__(self, game, pos):
        self.game = game
        self.grid_pos = pos
        self.pixel_pos = self.get_pix_pos()
        self.direction = vect(0, 0)
        self.saveddirection = None
        self.nowallblock = True
        self.score = 0
        self.highscore = 0
        self.lives = 1
        self.starting_pos = [pos.x, pos.y]

    def update(self):
        if self.nowallblock:
            self.pixel_pos += self.direction * SPEED
        if self.moveset():
            if self.saveddirection != None:
                self.direction = self.saveddirection
            self.nowallblock = self.pathavailable()
            self.teleport()
            self.checkforportal
            #self.fire_portal()

        print(self.grid_pos, self.pixel_pos);

        self.grid_pos[0] = (self.pixel_pos[0]-55+self.game.cellwidth//2)//self.game.cellwidth+1
        self.grid_pos[1] = (self.pixel_pos[1]-55+self.game.cellheight//2)//self.game.cellheight+1

        self.eatcoin()


    def draw(self):
        #pacman
        pg.draw.circle(self.game.screen, PLAYERCOLOR, (int(self.pixel_pos.x), int(self.pixel_pos.y)), self.game.cellwidth//2-1)

        for x in range(self.lives):
            pg.draw.circle(self.game.screen, PLAYERCOLOR, (80 + 30*x, HEIGHT+20), 10)
        #pg.draw.rect(self.game.screen, RED, (self.grid_pos[0]*self.game.cellwidth+50//2,
        #self.grid_pos[1]*self.game.cellheight+50//2, self.game.cellwidth, self.game.cellheight), 1)

    def move(self, direction):
        pg.mixer.music.load('sounds/Pacman_Waka_Waka.wav')
        pg.mixer.music.play(-1)
        self.saveddirection = direction

    def get_pix_pos(self):
        return vect((self.grid_pos[0] * self.game.cellwidth) + 50 // 2 + self.game.cellwidth // 2,
                    (self.grid_pos[1] * self.game.cellheight) + 50 // 2 + self.game.cellheight // 2)

    def moveset(self):
        if int(self.pixel_pos.x+50//2) % self.game.cellwidth == 0:
            if self.direction == vect(1,0) or self.direction == vect(-1,0) or self.direction == vect(0,0):
                return True
        if int(self.pixel_pos.y+50//2) % self.game.cellheight == 0:
            if self.direction == vect(0,1) or self.direction == vect(0,-1) or self.direction == vect(0,0):
                return True

    def pathavailable(self):
        for wall in self.game.walls:
            if vect(self.grid_pos+self.direction) == wall:
                return False
        return True

    def teleport(self):
        for port in self.game.edgeportal:
            if vect(self.grid_pos) == port:
                #print("TELEPORT")
                if vect(self.grid_pos) == (0,14):
                    pg.mixer.music.load('sounds/pacman-portal.wav')
                    pg.mixer.music.play()
                    self.pixel_pos = vect((27 * self.game.cellwidth) + 50 // 2 + self.game.cellwidth // 2,
                        (14 * self.game.cellheight) + 50 // 2 + self.game.cellheight // 2)
                if vect(self.grid_pos) == (27,14):
                    pg.mixer.music.load('sounds/pacman-portal.wav')
                    pg.mixer.music.play()
                    self.pixel_pos = vect((0 * self.game.cellwidth) + 50 // 2 + self.game.cellwidth // 2,
                        (14 * self.game.cellheight) + 50 // 2 + self.game.cellheight // 2)

    def eatcoin(self):
        if self.grid_pos in self.game.coins:
            self.game.coins.remove(self.grid_pos)
            self.score += 10
            pg.mixer.music.load('sounds/pacman-pellet-eat.wav')
            pg.mixer.music.play()
        #for coin in self.game.coins:
         #   if vect(self.grid_pos) == coin:
          #      self.game.coins.remove(coin)

    def fire_portal(self):
        if (self.game.openblue == False):
            self.rp = pg.draw.circle(self.game.background, BLUE, (int(self.pixel_pos.x - 50// 2), int(self.pixel_pos.y -50// 2)), 15, 2)
            self.game.blueportal = self.get_pix_pos()
            self.game.blueportalgrid = vect(int(self.grid_pos.x),int(self.grid_pos.y))
            self.game.openblue = True
            return
        elif (self.game.openred == False and self.game.openblue == True):
            self.rp = pg.draw.circle(self.game.background, RED, (int(self.pixel_pos.x - 50// 2), int(self.pixel_pos.y -50// 2)), 15, 2)
            self.grid_pos = self.game.blueportalgrid
            self.pixel_pos = self.game.blueportal
            pg.mixer.music.load('sounds/portal-travel.wav')
            pg.mixer.music.play()
            self.direction *= 0
            self.game.openred = True
            return
        else:
            print("close portals")



    def checkforportal(self):
        pass
