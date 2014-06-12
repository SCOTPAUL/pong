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


    def touchPaddle(self, pad1, pad2):
        if self.rect.top <= pad1.rect.bottom and self.rect.right >= pad1.rect.left and self.rect.left <= pad1.rect.right:
            if self.rect.bottom >= pad1.rect.top:
                return 1

        elif self.rect.bottom >= pad2.rect.top and self.rect.right >= pad2.rect.left and self.rect.left <= pad2.rect.right:
            if self.rect.top <= pad2.rect.bottom:
                return 2

        else:
            return 0



    def move(self, pad1, pad2):
        self.rect = self.surface.get_rect(center =(self.px, self.py))
        self.surface.fill(self.colour)

        self.px += self.vx
        self.py += self.vy

        if self.touchPaddle(pad1, pad2) == 1:
            self.paddleReflect()
            self.py = 31

        if self.touchPaddle(pad1, pad2) == 2:
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


ball = Ball(WH[0]/2, WH[1]/2, 0, -5, 10, 10)
pad1 = Paddle(WH[0]/2, 20, 50, 10)
pad2 = Paddle(WH[0]/2, WH[1] - 20, 50, 10)

pygame.mouse.set_visible(False)


while True:
    windowSurface.fill((0, 0, 0))

    ball.move(pad1, pad2)
    ball.draw(windowSurface)
    pad2.update()
    pad1.draw(windowSurface)
    pad2.draw(windowSurface)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(60)


