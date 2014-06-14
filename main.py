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
        self.init = [px, py, vx, vy, w ,h, colour]

        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

        self.w = w
        self.h = h

        self.colour = colour
        
        self.surface = pygame.Surface([self.w, self.h])
        self.rect = self.surface.get_rect(center =(px, py))
        self.surface.fill(self.colour)

        self.bounce = pygame.mixer.Sound("pad.wav")
        

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


    def reset(self):
        self.set_v(self.init[2], self.init[3])
        self.set_p(self.init[0], self.init[1])


    def set_p(self, px, py):
        self.px = px
        self.py = py


    def set_v(self, vx, vy):
        self.vx = vx
        self.vy = vy


    def touchPaddle(self, pad1, pad2):
        if self.rect.top <= pad1.rect.bottom and self.rect.right >= pad1.rect.left and self.rect.left <= pad1.rect.right:
            if self.rect.bottom >= pad1.rect.top:
                self.bounce.play()
                return 1

        elif self.rect.bottom >= pad2.rect.top and self.rect.right >= pad2.rect.left and self.rect.left <= pad2.rect.right:
            if self.rect.top <= pad2.rect.bottom:
                self.bounce.play()
                return 2

        else:
            return 0



    def move(self, pad1, pad2):
        self.rect = self.surface.get_rect(center =(self.px, self.py))
        self.surface.fill(self.colour)

        self.px += self.vx
        self.py += self.vy

        if self.px <= 0:
            self.sideReflect()
        elif self.px >= WH[0]:
            self.sideReflect()


        if self.touchPaddle(pad1, pad2) == 1:
            self.paddleReflect()
            self.py = pad1.rect.bottom + self.h/2.0 + 1
            

        if self.touchPaddle(pad1, pad2) == 2:
            self.paddleReflect()
            self.py = pad2.rect.top - self.h/2.0 - 1


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
        self.rect = self.surface.get_rect(center =(self.px, self.py))
        self.surface.fill(self.colour)


    def setPos(self, px, py):
        self.px = px
        self.py = py


    def update(self):
        mouseX = pygame.mouse.get_pos()[0]
        self.px = mouseX
        self.rect = self.surface.get_rect(center =(self.px, self.py))


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


def drawMidline(screen, WH, h, num, spacing = 20, colour = (255, 255, 255)):
    midpoint = WH[1]/2.0

    totalSpace = WH[0] - (num-1)*spacing
    width = totalSpace/float(num)

    myRect = pygame.Surface([width, h])
    myRect.fill(colour)

    startX = width/2.0

    for line in range(num):
        thisRect = myRect.get_rect(center =(startX, midpoint))
        screen.blit(myRect, thisRect)
        startX += spacing + width

    





ball = Ball(WH[0]/2.0, WH[1]/2.0, 0, -5, 10, 10)
pad1 = Paddle(WH[0]/2, 20, 100, 10)
pad2 = Paddle(WH[0]/2, WH[1] - 20, 100, 10)
score = Score(0, 0, 20, 20)

pygame.mouse.set_visible(False)


while True:
    windowSurface.fill((0, 0, 0))
    drawMidline(windowSurface, WH, 5, 20)

    ball.move(pad1, pad2)

    ball.draw(windowSurface)
    
    if ball.py <= 0:
        score.incScore(1)
        ball.reset()
    elif ball.py >= WH[1]:
        score.incScore(2)
        ball.reset()



    pad2.update()
    pad1.draw(windowSurface)
    pad2.draw(windowSurface)
    score.draw(windowSurface)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(60)


