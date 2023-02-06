import pygame as pg
import random
#from figclass import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 1000
HEIGHT = 600



class Asteroid(pg.sprite.Sprite): #creamos clase asteroide, la cual será subclase de la clase sprite
    def __init__(self): #inicalizamos clase
        super().__init__() #inicializamos superclase
        self.image = pg.image.load("sprites/Steroid3.png").convert() #elegimos imagen
        self.image.set_colorkey(WHITE) #con esto quitamos el borde negro de las imágenes
        self.rect = self.image.get_rect() #con esto obtenemos las coordenadas para poder posicionar nuestro sprite

    def update(self): #para el movimiento
        self.rect.x -= 4
        if self.rect.x < -100: #así parece que se vayan perdiendo por la izquierda
            self.rect.x = 1100 #así parece que se vayan creando por la derecha
            self.rect.y = random.randrange(HEIGHT)

        

class Navy(pg.sprite.Sprite): #creamos clase navy, la cual será subclase de la clase sprite
    def __init__(self): #inicalizamos clase
        super().__init__() #inicializamos superclase
        self.image = pg.image.load("images/navydef2.png").convert() #elegimos imagen
        self.image.set_colorkey(WHITE) #con esto quitamos el borde negro de las imágenes
        self.rect = self.image.get_rect() #con esto obtenemos las coordenadas para poder posicionar nuestro sprite
        self.rect.y = 250; self.rect.x = 15

    def update(self, ymax = 600, ymin = 0): #para el movimiento
        if pg.key.get_pressed()[pg.K_UP] and self.rect.y > ymin: #para que no se salga por arriba
            self.rect.y -= 5
            if pg.key.get_pressed()[pg.K_SPACE]:#gana velocidad apretando espacio
                    self.rect.y -= 7
        if pg.key.get_pressed()[pg.K_DOWN] and self.rect.y < ymax: #retocar, se sale por abajo
            self.rect.y += 5
            if pg.key.get_pressed()[pg.K_SPACE]:#gana velocidad apretando espacio
                    self.rect.y += 7

class Music():
    pass


pg.init()
pg.mixer.init() #para la música


def draw_text(surface, text, size, x = 40, y = 40): #para la puntuación (MIRAR PQ NO SUBE)
    font = pg.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("THE QUEST")
clock = pg.time.Clock() #para controlar los fps
score = 0
textscore = ("SCORE: ")


asteroid_list = pg.sprite.Group() #lista en la cual almacenamos los asteorides
all_sprite_list = pg.sprite.Group() #lista para almacenaer todos los sprites



for i in range(4): #número de asteroides
    asteroid = Asteroid()
    asteroid.rect.x = random.randrange(1000) #se posicionan aleatoriamente en todo el eje X
    asteroid.rect.y = random.randrange(600)  #se posicionan aleatoriamente en todo el eje Y

    asteroid_list.add(asteroid) #añadimos los asteorides a la lista
    all_sprite_list.add(asteroid) #añadimos los asteorides a la lista de todos los sprites


navy = Navy()
all_sprite_list.add(navy)




running = True
while running:
    clock.tick(60) #controlamos fps
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False 

    
    all_sprite_list.update() #con este método TODOS los cambios que hagamos en las clases se activan automaticmanete
    background = pg.image.load("images/backgroundstg1.jpg").convert()

    hits = pg.sprite.spritecollide(navy, asteroid_list, True)
    if hits:
        running = False

    screen.blit(background,[0, 0]) #coordenadas dnd queremos el fondo
    
    all_sprite_list.draw(screen) #dibujamos los sprites en pantalla
    draw_text(screen, str(score), 35, 180, 10)
    draw_text(screen, str(textscore), 35, 80, 10)


    pg.time.get_ticks()
    pg.display.flip()

pg.quit()