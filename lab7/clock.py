import pygame as pg
import datetime as dt
from sys import exit

pg.init()

W = 800
H = 600

clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))
bg = pg.image.load("img/clock.png")

min_hand = pg.image.load("img/min_hand.png")
sec_hand = pg.image.load("img/sec_hand.png")

def rotate(surf, img, times):
    rot_img = pg.transform.rotate(img, -(times % 60) * 6)
    new_img = rot_img.get_rect(center = img.get_rect(center = (400, 300)).center)
    print(new_img)
    surf.blit(rot_img, new_img)


pg.display.set_caption("Clock!")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    

    
    curtime = dt.datetime.now()
    minuts = curtime.minute
    seconds = curtime.second

    screen.fill("BLACK")


    screen.blit(bg, (0,0))
    
    rotate(screen, sec_hand, seconds)
    rotate(screen, min_hand, minuts)

    pg.display.update()
    clock.tick(60)