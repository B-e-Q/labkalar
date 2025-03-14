import pygame as pg

pg.init()

W = 600
H = 600


clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))

pg.display.set_caption("Ball!")


def drawcircle(x = 0, y = 0):
    pg.draw.circle(screen, (255, 0, 0), (x, y), 25)


bx, by = 25, 25
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    

    screen.fill((255, 255, 255))

    SPEED = 20
    drawcircle(bx, by)
    key = pg.key.get_pressed()
    if key[pg.K_w]  and by > 25 :
        by += -SPEED
    if key[pg.K_s] and by < 575:
        by += SPEED
    if key[pg.K_d] and bx < 575:
        bx += SPEED
    if key[pg.K_a] and bx > 25:
        bx += -SPEED

        
    



    pg.display.update()
    clock.tick(60)