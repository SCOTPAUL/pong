#!/usr/bin/python

import pygame, sys
from pygame.locals import *

WH = (640, 480)

pygame.init()
fpsClock = pygame.time.Clock()

windowSurface = pygame.display.set_mode(WH)
pygame.display.set_caption("Pong")

class Ball(object):

    def __init__(self, px, py, vx, vy, w ,h, colour = (255, 255, 255)):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

        self.colour = colour
        
        self.surface = pygame.Surface([w, h])
        self.rect = self.surface.get_rect(center =(px, py))
        self.surface.fill(self.colour)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


    def destroy(self):
        del self


    def set_p(self, px, py):
        self.px = px
        self.py = py


    def set_v(self, vx, vy):
        self.vx = vx
        self.vy = vy


    def move(self, pad1, pad2):
        self.rect = self.surface.get_rect(center =(self.px, self.py))
        self.surface.fill(self.colour)

        self.px += self.vx
        self.py += self.vy

        if self.rect.top <= pad1.rect.bottom and self.rect.right >= pad1.rect.left and self.rect.left <= pad1.rect.right:
            print self.rect.top, pad1.rect.bottom
            self.paddleReflect()
            self.py = 31
            

        if self.rect.bottom >= pad2.rect.top and self.rect.right >= pad2.rect.left and self.rect.left <= pad2.rect.right:
            self.paddleReflect()
            self.py = WH[1] - 31


    def sideReflect(self):
        self.vx = -self.vx


    def paddleReflect(self):
        self.vy = -self.vy


class Paddle(object):

    def __init__(self, px, py, w, h, colour = (255,255,255)):
        self.px = px
        self.py = py

        self.colour = colour
        
        self.surface = pygame.Surface([w, h])
        self.rect = self.surface.get_rect(center =(px, py))
        self.surface.fill(self.colour)


    def move(self, dx, dy):
        self.px += dx
        self.py += dy


    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Score(object):

    def __init__(self, score1, score2, px, py, colour = (255, 255, 255), font = "Lucida Console", size = 30):
        self.score1 = score1
        self.score2 = score2
        self.colour = colour
        self.font = font
        self.size = size
        self.px = px
        self.py = py

        self.myfont = pygame.font.SysFont(self.font, self.size, bold = True)

    def resetScore(self, val = 0):
        self.score1 = val
        self.score2 = val

    def incScore(self, whichScore, val = 1):
        if whichScore == 1:
            self.score1 += val
        elif whichScore == 2:
            self.score2 += val


    def draw(self, screen):
        score1text = self.myfont.render(str(self.score1), True, self.colour)
        score2text = self.myfont.render(str(self.score2), True, self.colour)

        screen.blit(score1text, (self.px, self.py))
        screen.blit(score2text, (WH[0]-self.px-self.size/2.0, self.py))

ball = Ball(10, WH[1]/2, 0, 5, 10, 10)
pad1 = Paddle(WH[0]/2, 20, 50, 10)
pad2 = Paddle(WH[0]/2, WH[1] - 20, 50, 10)
score = Score(0, 0, 20, WH[1]/2.0-30)


while True:
    windowSurface.fill((0, 0, 0))

    ball.move(pad1, pad2)

    ball.draw(windowSurface)
    
    if ball.py <= 0:
        score.incScore(1)
        pygame.time.delay(1000)
        ball.set_p(WH[0]/2.0, WH[1]/2.0)
    elif ball.py >= WH[1]:
        score.incScore(2)
        pygame.time.delay(1000)
        ball.set_p(WH[0]/2.0, WH[1]/2.0)

    pad1.draw(windowSurface)
    pad2.draw(windowSurface)
    score.draw(windowSurface)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(60)


