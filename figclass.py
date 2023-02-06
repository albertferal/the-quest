import pygame as pg

class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed_x, speed_y):
        self.image = pg.image.load("sprites/Asteroid Brown.png/").convert() #elegimos imagen
        #self.image.set_colorkey(BLACK) #con esto quitamos el borde blanco de las imágenes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed_x = speed_x
        self.speed_y = speed_y

class Navy:
    def __init__(self, pos_x, pos_y, vx, vy):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vx = vx
        self.vy = vy

