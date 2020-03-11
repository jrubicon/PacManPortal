import pygame as pg
import sys
import copy
from settings import *
from playerclass import *
from enemyclass import *
import os

pg.init()
vect = pg.math.Vector2


class Main:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT+50))
        self.clock = pg.time.Clock()
        self.running = True
        self.state = 'startscreen'
        self.cellwidth = PM_WIDTH // COLS
        self.cellheight = PM_HEIGHT // ROWS

        self.walls = []
        self.edgeportal = []
        self.coins = []
        self.enemies = []
        self.enemypos = []
        self.playerpos = None
        self.powerups = []

        self.blueportal = None
        self.blueportalgrid = None
        self.redportal = None
        self.openred = False
        self.openblue = False
        self.highSC = []

        self.load()
        #self.loadanimations()

        self.player = Player(self, vect(self.playerpos))
        self.loadHS()
        self.create_enemies()
        self.intro_buttons()
        pg.mixer.music.load('sounds/bg-music.wav')
        pg.mixer.music.play(-1)

    def run(self):
        while self.running:
            if self.state == 'startscreen':
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            elif self.state == 'play':
                self.play_events()
                self.play_update()
                self.play_draw()
            elif self.state == 'highscore':
                self.high_events()
                self.high_update()
                self.high_draw()
            elif self.state == 'game over':
                self.gameover_events()
                self.gameover_update()
                self.gameover_draw()
            else:
                self.running = False
            pg.display.update()
            self.clock.tick(FPS)
        pg.quit()
        sys.exit()

    @staticmethod
    def draw_text(text, screen, pos, size, color, fontname, centered=False):
        font = pg.font.SysFont(fontname, size)
        scrtext = font.render(text, False, color)
        text_size = scrtext.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(scrtext, pos)

    def draw_grid(self):
        for x in range(WIDTH // self.cellwidth):
            pg.draw.line(self.background, GRAY, (x * self.cellwidth, 0), (x * self.cellwidth, HEIGHT))
        for x in range(HEIGHT // self.cellheight):
            pg.draw.line(self.background, GRAY, (0, x * self.cellheight), (WIDTH, x * self.cellheight))
            # wall visualization
        for wall in self.walls:
            pg.draw.rect(self.background, (132,55,164), (wall.x*self.cellwidth, wall.y*self.cellheight, self.cellwidth, self.cellheight))
            # coin visualization
        for cc in self.coins:
            pg.draw.rect(self.background, (100,55,164), (cc.x*self.cellwidth, cc.y*self.cellheight, self.cellwidth, self.cellheight))

    def write_toHS(self):
        print(*self.highSC)
        with open(HS_FILE, 'a') as file:
            file.write(str(self.player.highscore)+'\n')
        file.close()

    def loadanimations(self):
        pass
        # image = pg.image.load("images/pacman-vert.png")
        # image = image.convert_alpha()
        # thisSprite = newSprite(image, 5)

    def loadHS(self):
        with open(HS_FILE, 'r') as filehandle:
            filecontents = filehandle.readlines()

            for line in filecontents:
                current_place = line

                # add item to the list
                self.highSC.append(current_place)
                self.highSC.sort(reverse=True)
                self.player.highscore = self.highSC[0]
            #test
            print(*self.highSC)

    def load(self):
        self.background = pg.image.load('background.png')
        self.background = pg.transform.scale(self.background, (PM_WIDTH, PM_HEIGHT))
        with open("maze.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vect(xidx, yidx))
                    if char == "T":
                        self.edgeportal.append(vect(xidx, yidx))
                    if char == "*":
                        self.coins.append(vect(xidx, yidx))
                    if char == "P":
                        self.powerups.append(vect(xidx, yidx))
                    if char == "S":
                        self.playerpos = [xidx, yidx]
                    if char in ["2", "3", "4", "5"]:
                        self.enemypos.append([xidx, yidx])
                    #if char == "8":
                     #  pg.draw.rect(self.background, BLACK, (xidx*self.cellwidth, yidx*self.cellheight), self.cellwidth, self.cellheight)

    def create_enemies(self):
        for idx, pos in enumerate(self.enemypos):
            self.enemies.append(Enemy(self, vect(pos), idx))

    # INTRO

    def intro_events(self):
        for event in pg.event.get():
            self.playoption = self.playfont.render(('PLAY GAME'), True, ORANGE)
            self.hsoption = self.hsfont.render(('HIGHSCORES'), True, ORANGE)

            if event.type == pg.QUIT:
                self.running = False
            elif self.hs_r.collidepoint(pg.mouse.get_pos()):
                print('detectedHS')
                self.hsoption = self.hsfont.render(('HIGHSCORES'), True, WHITE)
                if event.type == pg.MOUSEBUTTONDOWN:
                    print('engagedHS')
                    self.state = 'highscore'
            elif self.play_r.collidepoint(pg.mouse.get_pos()):
                print('detectedPLAY')
                self.playoption = self.playfont.render(('PLAY GAME'), True, WHITE)
                if event.type == pg.MOUSEBUTTONDOWN:
                    pg.mixer.music.stop()
                    pg.mixer.music.load('sounds/pacman-beginning.wav')
                    pg.mixer.music.play()
                    print('engagedPLAY')
                    self.state = 'play'

    def intro_update(self):
        pass

    def intro_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.playoption, PLAYBUTTON)
        self.screen.blit(self.hsoption, HIGHSCORESBUTTON)
        self.plogo = pg.image.load('pacmanlogo.png')
        self.plogo = pg.transform.scale(self.plogo, (500, 160))

        self.screen.blit(self.plogo, (50,50) )
        #self.draw_text('PACMAN PORTAL', self.screen, [WIDTH // 2, HEIGHT // 2 - 250],
              #         LOGO, ORANGE, LOGO_FONT, centered=True)

    def intro_buttons(self):
        # play
        self.playfont = pg.font.SysFont(INTRO_FONT, INTRO_TEXT_SIZE, 16)
        self.playoption = self.playfont.render(('PLAY GAME'), True, ORANGE)
        self.play_r = self.playoption.get_rect()
        self.play_r.x, self.play_r.y = (WIDTH//2-50), (HEIGHT//2+170)
        # highscores
        self.hsfont = pg.font.SysFont(INTRO_FONT, INTRO_TEXT_SIZE, 16)
        self.hsoption = self.hsfont.render(('HIGHSCORES'), True, ORANGE)
        self.hs_r = self.hsoption.get_rect()
        self.hs_r.x, self.hs_r.y = (WIDTH//2-88), (HEIGHT//2+220)

    # HIGH SCORE

    def high_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSLASH:
                self.state = 'startscreen'

    def high_update(self):
        pass

    def high_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('EXIT (\) ', self.screen, [WIDTH // 2+200, 100],
                       INTRO_TEXT_SIZE, ORANGE, INTRO_FONT, centered=True)
        self.draw_text('HIGH SCORES', self.screen, [WIDTH // 2, HEIGHT // 2 - 250],
                       INTRO_TEXT_SIZE, ORANGE, INTRO_FONT, centered=True)
        #self.highSC.sort(reverse=True)
        for x in range(len(self.highSC)):
            self.draw_text('{}'.format(self.highSC[x]), self.screen, [WIDTH//2-40,HEIGHT//2 -200 + 50*x], 40, WHITE, INTRO_FONT, centered=False)



    # PLAYING

    def play_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(vect(-1, 0))
                if event.key == pg.K_RIGHT:
                    self.player.move(vect(1, 0))
                if event.key == pg.K_UP:
                    self.player.move(vect(0, -1))
                if event.key == pg.K_DOWN:
                    self.player.move(vect(0, 1))
                if event.key == pg.K_q:
                    print("FIRE PORTAL")
                    pg.mixer.music.load('sounds/portal-open.wav')
                    pg.mixer.music.play()
                    self.player.fire_portal()

    def play_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                pg.mixer.music.load('sounds/pacman-killed.wav')
                pg.mixer.music.play()
                self.removelife()

    def play_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (50//2, 50//2))
        self.coin_draw()
        self.powerup_draw()
        # self.draw_grid()
        self.draw_text('SCORE: {}'.format(self.player.score), self.screen, [WIDTH//2-240,650], 30, WHITE, INTRO_FONT, centered=False)
        self.draw_text('HIGHSCORE: {}'.format(self.player.highscore), self.screen, [WIDTH//2+100,650], 30, WHITE, INTRO_FONT, centered=False)
        self.draw_text('Portal(Q)', self.screen, [WIDTH//2+100,680], 30, PURPLE, INTRO_FONT, centered=False)

        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

    def removelife(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vect(self.player.starting_pos)
            self.player.pixel_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vect(enemy.starting_pos)
                enemy.pixel_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def coin_draw(self):
        for coin in self.coins:
            pg.draw.circle(self.screen, COIN, (int(coin.x *self.cellwidth)+self.cellwidth//2+50//2,
                           int(coin.y*self.cellheight)+self.cellheight//2+50//2), 2)
    def powerup_draw(self):
        for powerup in self.powerups:
            pg.draw.circle(self.screen, POWERUP, (int(powerup.x *self.cellwidth)+self.cellwidth//2+50//2,
                           int(powerup.y*self.cellheight)+self.cellheight//2+50//2), 6)

    def gameover_events(self):
        self.end_buttons()
        if self.player.score > int(self.player.highscore):
            self.player.highscore = self.player.score
            self.highSC.append(self.player.highscore)

        for event in pg.event.get():
            self.restartoption = self.playfont.render(('RESTART'), True, ORANGE)
            self.endoption = self.endfont.render(('QUIT'), True, ORANGE)

            if self.res_r.collidepoint(pg.mouse.get_pos()):
                print('detectedRES')
                self.restartoption = self.resfont.render(('RESTART'), True, WHITE)
                if event.type == pg.MOUSEBUTTONDOWN:
                    print('engagedRES')
                    self.reset()
            elif self.end_r.collidepoint(pg.mouse.get_pos()):
                print('detectedQUIT')
                self.endoption = self.endfont.render(('QUIT'), True, WHITE)
                if event.type == pg.MOUSEBUTTONDOWN:
                    print('engagedQUIT')
                    self.state = 'quit'
                    self.write_toHS()
            elif event.type == pg.QUIT:
                 self.running = False

    def gameover_update(self):
        pass
    def gameover_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.screen, [WIDTH//2-190, 200], 90, WHITE, INTRO_FONT, centered=False)
        self.screen.blit(self.restartoption, RESTARTBUTTON)
        self.screen.blit(self.endoption, QUITBUTTON)

    def end_buttons(self):
        # restart
        self.resfont = pg.font.SysFont(INTRO_FONT, INTRO_TEXT_SIZE, 16)
        self.restartoption = self.resfont.render(('RESTART'), True, ORANGE)
        self.res_r = self.restartoption.get_rect()
        self.res_r.x, self.res_r.y = (WIDTH//2-88), (HEIGHT//2+10)

        # exit
        self.endfont = pg.font.SysFont(INTRO_FONT, INTRO_TEXT_SIZE, 16)
        self.endoption = self.endfont.render(('QUIT'), True, ORANGE)
        self.end_r = self.endoption.get_rect()
        self.end_r.x, self.end_r.y = (WIDTH // 2 - 88), (HEIGHT // 2 + 70)

    def reset(self):
        self.player.lives = 3
        self.coins = []
        self.player.score = 0
        self.player.grid_pos = vect(self.player.starting_pos)
        self.player.pixel_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vect(enemy.starting_pos)
            enemy.pixel_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        with open("maze.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '*':
                        self.coins.append(vect(xidx, yidx))
                    if char == "P":
                        self.powerups.append(vect(xidx, yidx))
        self.state = 'play'
        pg.mixer.music.load('sounds/pacman-beginning.wav')
        pg.mixer.music.play()