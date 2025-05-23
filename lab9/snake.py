import pygame as pg
import random

pg.init()

# Height and Width of Display
W = 800
H = 800

clock = pg.time.Clock()
screen = pg.display.set_mode((W, H))


# Name of the game is Snake
pg.display.set_caption("Snake!")


# Block size
BS = 50

# Frame Per Second
FPS = 10

# Fonts
font = pg.font.Font('fonts/MICKEY.TTF',30)
int_font = pg.font.Font('fonts/MICKEY.TTF',30)


# Draw cells for Snake field
def drawField():
    for i in range(0, W, BS):
        for j in range(0, H, BS):
            rect = pg.Rect(i, j, BS, BS)
            pg.draw.rect(screen, (21, 27, 35), rect, 1)


# Text Writer
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

        # Is Snake Dead?
        for i in self.body:
            if self.head.x not in range(0, W) or self.head.y not in range(0, H):
                self.dead = True
            if self.head.x == i.x and self.head.y == i.y:
                self.dead = True
        

        # Restart snake's position and size
        if self.dead:
            self.score = 0
            self.level = 1
            self.x, self.y = BS, BS
            self.xdir = 1
            self.ydir = 0
            self.head = pg.Rect(self.x, self.y, BS, BS)
            self.body = [pg.Rect(self.x - BS, self.y, BS, BS)]
            self.dead = False

        # Movement of snake
        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BS
        self.head.y += self.ydir * BS
        self.body.remove(self.head)
    

    
    # Drawing the Snake
    def draw(self, surf, side = [0, 0, 0, 0]):
        pg.draw.rect(surf, (0, 255, 0), (self.head.x, self.head.y, BS, BS), 0, 0, side[0], side[1], side[2], side[3])

        for i in self.body:
            pg.draw.rect(surf, "green", i)


class Apple:
    def __init__(self):
        # Randomize the location of the apple and adjust it to fit in the cell perfectly
        self.x = random.randint(0, W)// BS * BS
        self.y = random.randint(0, H)// BS * BS
        self.disap_timer = 0
        self.color = ["red", "green", "blue"]
        self.i = random.randint(0,2)
    
    # Draw apple on display
    def draw(self, screen):
        pg.draw.circle(screen, self.color[self.i], (self.x+25, self.y+25), 25)

snake = Snake()
apple = Apple()

# Snake's head's angles
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
    
    # Fill Display with color
    screen.fill((13, 17, 23))
    

    # Generate apple and place on display
    apple.draw(screen)

    # Move snake 
    snake.move()

    # Draw snake's postion
    snake.draw(screen, sides)


    # Snake eating apple
    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pg.Rect(snake.body[-1].x, snake.body[-1].y, BS, BS))
        snake.score += apple.i + 1 # Get point if snake eats the apple
        apple = Apple() # Regenerate new postions for apple if snake eat it
        apple.disap_timer = pg.time.get_ticks()
        snake.level = snake.score // 5 + 1 # update level
    

    # Apple disappear in 3s
    if pg.time.get_ticks() - apple.disap_timer > 3000:
        apple = Apple() # Regenerate new postions for apple if it snake couldn't eat it in 3s
        apple.disap_timer = pg.time.get_ticks()


    # Draw cell 
    drawField()

    # Write level and score on display 
    drawtext(snake.score, snake.level)
    
    pg.display.update()
    clock.tick(FPS + snake.level - 1)
pg.quit()
exit()