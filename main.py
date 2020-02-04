import pygame as pg
from pygame.locals import *
import sys

from entities import *

FPS = 60
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

level1 = ['XXXXXXXXXXXXXXXX',
           'XXXXXX---XXXXXXX',
           'XXXXXXX-XXXXXXXX',
           'XXXXXXXXXXXXXXXX',
           ]

class Game:
    clock = pg.time.Clock()
    score = 0

    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption('Mi Arcanoid')

        self.background_img = pg.image.load('resources/background.png').convert()

        self.fontGran = pg.font.Font('resources/fonts/PressStart2P.ttf', 40)
        self.font = pg.font.Font('resources/fonts/PressStart2P.ttf', 28) #de la libreria pygame el modulo font, y creamos el objeto tipo font, mirar en doc
        self.marcador = self.font.render('0', True, WHITE) #mirar render en doc, antialiased redondea los pixeles de las letras
        self.livescounter = self.font.render('0', True, WHITE)
        self.text_gameOver = self.fontGran.render("GAME OVER", True, YELLOW)
        self.text_insert_coin = self.font.render("<SPACE> - Insert Coin", True, WHITE)


        self.player = Racket()
        self.ball = Ball()
        self.tileGroup = pg.sprite.Group()

        self.playerGroup = pg.sprite.Group()
        self.allSprites = pg.sprite.Group()
        self.playerGroup.add(self.player)
              
        self.start_partida()

    
        

    def start_partida(self):
        self.player.lives = 3
        self.ball.start()
        self.tileGroup.empty() #esto vacia el grupo
        self.allSprites.empty()
        self.tileGroup = Mapa().bricks(level1, Tile)
        self.score = 0
        self.allSprites.add(self.tileGroup) #esto pinta los ladrillos
        self.allSprites.add(self.player) #esto pinta el jugador
        self.allSprites.add(self.ball) #esto pinta la bola

    def quitGame(self):
        pg.quit()
        sys.exit()

    def handleEventsGO(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitGame()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.start_partida()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quitGame()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.player.go_left()

                if event.key == K_RIGHT:
                    self.player.go_right()

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.player.go_left()

        if keys_pressed[K_RIGHT]:
            self.player.go_right()

    def mainloop(self):
        while True:
            dt = self.clock.tick(FPS)

            if self.player.lives > 0 and len(self.tileGroup) > 0:
                self.bucle_partida(dt)

            elif len(self.tileGroup) == 0:
                pass

            else:
                self.gameOver()

            pg.display.flip()

    def bucle_partida(self, dt):
        self.handleEvents()

        self.ball.test_collisions(self.playerGroup)
        self.score += self.ball.test_collisions(self.tileGroup, True)
        
        if self.ball.speed == 0: #se ha producido colision
            self.player.lives -= 1
            self.ball.start()
            

        self.livescounter = self.font.render(str(self.player.lives), True, WHITE)
        self.marcador = self.font.render(str(self.score), True, WHITE)

        self.screen.blit(self.background_img,(0,0)) #blit --> objeto pygame para representar imágenes

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen) #draw --> módulo de pygame para dibujar formas

        self.screen.blit(self.marcador, (750, 10))
        self.screen.blit(self.livescounter, (50, 10))

    def gameOver(self):
        self.handleEventsGO()

        rect = self.text_gameOver.get_rect()
        self.screen.blit(self.text_gameOver, ((800 - rect.w)//2, 300))
        rect = self.text_insert_coin.get_rect()
        self.screen.blit(self.text_insert_coin, ((800 - rect.w)//2, 380))


if __name__ == '__main__':
    pg.init()
    game = Game()
    game.mainloop()