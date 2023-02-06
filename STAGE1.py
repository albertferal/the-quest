import pygame as pg
import random


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 1000
HEIGHT = 600


pg.init()
pg.mixer.init()
FONT = pg.font.SysFont("Arial", 30)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("THE QUEST")
clock = pg.time.Clock() #para controlar los fps
pg.time.get_ticks()

asteroids_images = []
asteroids_list = ["sprites\Steroid4.png","sprites\Steroid2.png"]
for img in asteroids_list:
    asteroids_images.append(pg.image.load(img).convert())


crashsound = pg.mixer.Sound("music\colision.wav")


class Asteroid(pg.sprite.Sprite): #creamos clase asteroide, la cual será subclase de la clase sprite
    def __init__(self): #inicalizamos clase
        super().__init__() #inicializamos superclase
        self.image = random.choice(asteroids_images) #elegimos imagen
        self.image.set_colorkey(WHITE) #con esto quitamos el borde negro de las imágenes
        self.rect = self.image.get_rect() #con esto obtenemos las coordenadas para poder posicionar nuestro sprite
    
    def update(self): #para el movimiento
        self.rect.x -= 3
        if self.rect.x < -100 and STAGETIMER < 70: #así parece que se vayan perdiendo por la izquierda
                            #SI EL TIEMPO ES DE MÁS DE 20 SEG LOS ASTEROIDES YA NO APARECEN
                            #NOS SIRVE PARA HACER APARECER EL PLANETA
                self.rect.x = random.randrange(1200, 1500) #así parece que se vayan creando por la derecha
                self.rect.y = random.randrange(50, 550)



class Navy(pg.sprite.Sprite): #creamos clase navy, la cual será subclase de la clase sprite
    def __init__(self): #inicalizamos clase
        super().__init__() #inicializamos superclase
        self.image = pg.image.load("images/navydef2.png").convert() #elegimos imagen
        self.image.set_colorkey(WHITE) #con esto quitamos el borde negro de las imágenes
        self.rect = self.image.get_rect() #con esto obtenemos las coordenadas para poder posicionar nuestro sprite
        self.rect.y = 250; self.rect.x = 35
        self.hp = 90

    def update(self, ymax = 600, ymin = 0): #para el movimiento
        if STAGETIMER < 79:
            if pg.key.get_pressed()[pg.K_UP] and self.rect.y > ymin + 50: #para que no se salga por arriba
                self.rect.y -= 3
                if pg.key.get_pressed()[pg.K_SPACE]:#gana velocidad apretando espacio
                        self.rect.y -=5 
            if pg.key.get_pressed()[pg.K_DOWN] and self.rect.y < ymax - 70: #retocar, se sale por abajo
                self.rect.y += 3
                if pg.key.get_pressed()[pg.K_SPACE]:#gana velocidad apretando espacio
                        self.rect.y += 5
        else:
            if self.rect.y < 250:
                self.rect.y +=1
            if self.rect.y > 250:
                self.rect.y -=1        
            if self.rect.x < 300:
                self.rect.x += 1  
                if self.rect.x >= 300:
                    self.image = pg.transform.flip(self.image, True, True)
            if self.rect.x < 550:
                self.rect.x += 1
       


class Crashanim(pg.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = crash_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 60 #controla la velocidad de la explosion
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(crash_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = crash_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


crash_anim = []
for i in range (9):
    crash = "images/regularExplosion0{}.png".format(i)
    img = pg.image.load(crash).convert()
    img.set_colorkey(BLACK)
    img_scale = pg.transform.scale(img, (100, 100))
    crash_anim.append(img_scale)



def hpbar (surface, x, y, percentage):
    BAR_LENGHT = 130
    BAR_HEIGHT = 25
    fill = (percentage/100) * BAR_LENGHT 
    border = pg.Rect(x, y, BAR_LENGHT -10, BAR_HEIGHT) #resto 10 para que la barra se llene entera
    fill = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surface, RED, fill)
    pg.draw.rect(surface, WHITE, border, 3)


asteorid = Asteroid()
asteroid_list = pg.sprite.Group() #lista en la cual almacenamos los asteorides
all_sprite_list = pg.sprite.Group() #lista para almacenaer todos los sprites


for i in range(6): #número de asteroides
    asteroid = Asteroid()
    asteroid.rect.x = random.randrange(1000,2000) #se posicionan aleatoriamente en todo el eje X
                                        #pongo 1000-2000 para que al empezar salgan de la izq
    asteroid.rect.y = random.randrange(50, 550)  #se posicionan aleatoriamente en todo el eje Y
    asteroid_list.add(asteroid) #añadimos los asteorides a la lista
    all_sprite_list.add(asteroid) #añadimos los asteorides a la lista de todos los sprites


navy = Navy()
all_sprite_list.add(navy)


planet1 = pg.image.load("images\planetstg1.png").convert()
planet1.set_colorkey(BLACK)
pos_x = 1200
pos_y = -50
xmax = 700


running = True
while running:
    STAGETIMER = pg.time.get_ticks()/1000
    clock.tick(60) #controlamos fps
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False 


    all_sprite_list.update() #con este método TODOS los cambios que hagamos en las clases se activan automaticmanete
    background = pg.image.load("images/backgroundstg1.jpg").convert()

    hits = pg.sprite.spritecollide(navy, asteroid_list, True)
    for hit in hits:
        crashsound.play()
        navy.hp -= 30
        crash = Crashanim(hit.rect.center)
        all_sprite_list.add(crash)
        
        if navy.hp <= 0:
           for i in range (9):
            crash = "images/regularExplosion0{}.png".format(i)
            img = pg.image.load(crash).convert()
            img.set_colorkey(BLACK)
            img_scale = pg.transform.scale(img, (300, 300))
            crash_anim.append(img_scale)
            running = True


    screen.blit(background,[0, 0]) #coordenadas dnd queremos el fondo
    
    all_sprite_list.draw(screen) #dibujamos los sprites en pantalla

    screen.blit(planet1, (pos_x, pos_y))
    if STAGETIMER > 67:
        pos_x -= 1
        if pos_x == 600:
            pos_x += 1


    scorecount = FONT.render("SCORE: " + str(STAGETIMER), 0, (WHITE))
    screen.blit(scorecount,(5, 0))
    hpbar(screen, 870, 5, navy.hp)
  
    pg.display.flip()

pg.quit()