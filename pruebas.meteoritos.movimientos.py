import pygame as pg
import random
pg.init()

white = (255, 255, 255)
red = (255, 0, 0)
size = (800, 600)
screen = pg.display.set_mode(size)
clock = pg.time.Clock()



coord_list = []
c = 0
for i in range (10):
    x = random.randint(0,800)
    y = random.randint(0,600)
    coord_list.append([x, y])

running = True
while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False 
    screen.fill(white)
    
    
    #pg.draw.rect(screen, red, (xx, yy, 100, 50))

    

    for coord in coord_list:
        x = coord [0]
        y = coord [1]
        pg.draw.circle(screen, red, (x, y), 5) 
        #AHORA PARA Q SE MUEVAN Y SIEMPRE SALGAN OTRA VEZ:
        coord [0] -= random.randint(1,4)
        if coord [0] < 0:
           coord [0] = 800
           c += 10
           print(c)


    pg.display.flip()



