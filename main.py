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


    def move(self):
        self.rect = self.surface.get_rect(center =(self.px, self.py))
        self.surface.fill(self.colour)

        self.px += self.vx
        self.py += self.vy


    def sideReflect(self):
        self.vx = -self.vx


    def paddleReflect(self):
        self.vy = -self.vy


class Paddle(object):

    def __init__(self, px, py):
        self.px = px
        self.py = py


    def move(self, dx, dy):
        self.px += dx
        self.py += dy

ball = Ball(WH[0]/2, WH[1]/2, 0, 5, 5, 5)
WHITE = (255, 255, 255)


while True:
    windowSurface.fill((0, 0, 0))

    if ball.py <= 0 or ball.py >= WH[1]:
        ball.paddleReflect()

    ball.move()
    ball.draw(windowSurface)

    print ball.py

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(60)


