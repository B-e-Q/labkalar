import pygame as pg
import random

pg.init()

W = 800
H = 800

clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))

pg.display.set_caption("Snake!")

BS = 50


FPS = 10

font = pg.font.Font('fonts/MICKEY.TTF',30)
int_font = pg.font.Font('fonts/MICKEY.TTF',30)

def drawField():
    for i in range(0, W, BS):
        for j in range(0, H, BS):
            rect = pg.Rect(i, j, BS, BS)
            pg.draw.rect(screen, (21, 27, 35), rect, 1)


def drawtext(score, level):
    score_text = font.render(f"Score: {score}  Level: {level}", True, "WHITE")
    screen.blit(score_text, (10, 10))

class Snake:
    def __init__(self):
        self.x, self.y = BS, BS
        self.xdir = 1
        self.ydir = 0
        self.head = pg.Rect(self.x, self.y, BS, BS)
        self.body = [pg.Rect(self.x - BS, self.y, BS, BS)]
        self.dead = False
        self.score = 0
        self.level = 1

    def move(self):
        for i in self.body:
            if self.head.x not in range(0, W) or self.head.y not in range(0, H):
                self.dead = True
            if self.head.x == i.x and self.head.y == i.y:
                self.dead = True
        
        if self.dead:
            self.score = 0
            self.level = 1
            self.x, self.y = BS, BS
            self.xdir = 1
            self.ydir = 0
            self.head = pg.Rect(self.x, self.y, BS, BS)
            self.body = [pg.Rect(self.x - BS, self.y, BS, BS)]
            self.dead = False

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BS
        self.head.y += self.ydir * BS
        self.body.remove(self.head)
    

    

    def draw(self, surf, side = [0, 0, 0, 0]):
        pg.draw.rect(surf, (0, 255, 0), (self.head.x, self.head.y, BS, BS), 0, 0, side[0], side[1], side[2], side[3])

        for i in self.body:
            pg.draw.rect(surf, "green", i)


class Apple:
    def __init__(self):
        self.x = random.randint(0, W)// BS * BS
        self.y = random.randint(0, H)// BS * BS
    
    def draw(self, screen):
        pg.draw.circle(screen, "red", (self.x+25, self.y+25), 25)

snake = Snake()
apple = Apple()


sides = [0, 25, 0, 25]

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                snake.xdir = -1
                snake.ydir = 0
                sides = [25, 0, 25, 0]
            elif event.key == pg.K_s:
                snake.xdir = 0
                snake.ydir = 1
                sides = [0, 0, 25, 25]
            elif event.key == pg.K_d:
                snake.xdir = 1
                snake.ydir = 0
                sides = [0, 25, 0, 25]
            elif event.key == pg.K_w:
                snake.xdir = 0
                snake.ydir = -1
                sides = [25, 25, 0, 0]
    

    screen.fill((13, 17, 23))
    

    
    apple.draw(screen)
    snake.move()
    snake.draw(screen, sides)

    key = pg.key.get_pressed()

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pg.Rect(snake.body[-1].x, snake.body[-1].y, BS, BS))
        apple = Apple()
        snake.score += 1
        snake.level = snake.score // 5 + 1
    

    drawField()
    drawtext(snake.score, snake.level)
    
    pg.display.update()
    clock.tick(FPS + snake.level - 1)
pg.quit()
exit()