import pygame as pg
from pygame.locals import *
from random import choice

FPS = 60

class Racket(pg.sprite.Sprite):
    pictures = 'racket_horizontal.png'
    speed = 10
    lives = 3

    def __init__(self, x=355, y=580):
        self.x = x
        self.y = y

        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = self.rect.w
        self.h = self.rect.h
        
    def go_left(self):
        self.rect.x = max(0, self.rect.x - self.speed) #haces la resta y de entre el resultado y 0, me coges el mayor
        
    def go_right(self):
        self.rect.x = min(self.rect.x + self.speed, 800-self.w)  #haces la resta y de entre el resultado y 800, me coges el menor
        
class Ball(pg.sprite.Sprite):
    pictures = 'ball.png'
    dx = 1 #variacion de x derecha
    dy = 1
    speed = 5

    def __init__(self, x=400, y=300):
        self.x = x
        self.y = y
    
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('resources/{}'.format(self.pictures)).convert_alpha()
    
        self.rect = self.image.get_rect()
        self.w = self.rect.w
        self.h = self.rect.h

        self.start()

    def start(self):
        self.rect.x = self.x
        self.rect.y = self.y 
        self.speed = 5
        self.dy = 1
        self.dx = choice([-1, 1])

    def update(self, dt):
        self.rect.x = self.rect.x + self.speed * self.dx #la imgagen se mueve +velocidad por variacion derecha
        self.rect.y = self.rect.y + self.speed * self.dy #la imgagen se mueve +velocidad por variacion abajo

        if self.rect.y >=600 - self.h: #si es mayor de 600
            #self.dy = self.dy * -1 #inviertes la direccion y ahora seguirá hacia la derecha pero arriba, al haber llegado al limite, pierde vida
            self.speed = 0

        if self.rect.y <=0: #si es menor de 0
            self.dy = self.dy * -1

        if self.rect.x <=0: #si es menor de 0
            self.dx = self.dx * -1
        
        if self.rect.x >=775: #si es mayor de 600
            self.dx = self.dx * -1

    def test_collision(self, group):
        candidates = pg.sprite.spritecollide(self, group, False) #esto está en la documentacion pygame
        if len(candidates) > 0:
            self.dy *= -1


