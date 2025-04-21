import pygame as pg
import random
import psycopg2 as psg

conn = psg.connect(host="localhost", dbname="snake", user="postgres", password="Aa12340987.", port=5432)

cur = conn.cursor()

# Create Table
cur.execute(""" CREATE TABLE IF NOT EXISTS snake(
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
);
""")

cur.execute(""" CREATE TABLE IF NOT EXISTS snake_level(
            id SERIAL PRIMARY KEY,
            score INT NOT NULL,
            level INT NOT NULL,
            speed INT NOT NULL,
            name VARCHAR(50) NOT NULL
);
""")

pg.init()

def get_name(name):
    cur.execute("SELECT id FROM snake WHERE name=%s", (name,))
    exists = cur.fetchone()

    if exists:
        return exists[0]
    else:
        cur.execute("INSERT INTO snake (name) VALUES (%s) RETURNING id", (name,))
        conn.commit()
        return cur.fetchone()[0]

def get_level(id):
    cur.execute("SELECT level FROM snake_level WHERE id=%s LIMIT 1", (id,))
    row = cur.fetchone()
    return row[0] if row else 0

def get_score(id):
    cur.execute("SELECT score FROM snake_level WHERE id=%s LIMIT 1", (id,))
    row = cur.fetchone()
    return row[0] if row else 0

def get_speed(id):
    cur.execute("SELECT speed FROM snake_level WHERE id=%s LIMIT 1", (id,))
    row = cur.fetchone()
    return row[0] if row else 5

def save_all(score, level, speed, name):
    cur.execute("INSERT INTO snake_level (score, level, speed, name) VALUES (%s, %s, %s, %s)", (score, level, speed, name))
    conn.commit()
def update_all(score, level, speed, name, id):
    cur.execute("UPDATE snake_level SET score = %s, level = %s, speed = %s, name = %s WHERE id = %s", (score, level, speed, name, id))
    conn.commit()


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
user_name = ''


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


    def isdead(self):
        # Is Snake Dead?
        for i in self.body:
            if self.head.x not in range(0, W) or self.head.y not in range(0, H):
                self.dead = True
            if self.head.x == i.x and self.head.y == i.y:
                self.dead = True

    def restart(self):
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



    def move(self):
        # Movement of snake
        if not (self.xdir == 0 and self.ydir == 0):
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
score = 0

def start_menu():
    pg.draw.rect(screen, (21, 27, 35), (0, 0, W, H))

# Snake's head's angles
sides = [0, 25, 0, 25]
show_menu = 1

pouse = False
run = True
while run:
    #is dead
    snake.isdead()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if pouse:
                    pouse = False
                else:
                    snake.xdir = 0
                    snake.ydir = 0
                    pouse = True
            if not show_menu and not pouse:
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
            else:
                if event.key == pg.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    user_name += event.unicode
                if len(user_name) > 0 and event.key == pg.K_RETURN:
                    show_menu = 0
                    user_name = user_name[:-1]
                    user_id = get_name(user_name)
                    snake.score = get_score(user_id)
                    snake.level = get_level(user_id)
                    
            if snake.dead and event.key == pg.K_r:
                show_menu = 1
                cur.execute("SELECT id FROM snake WHERE name = %s", (user_name,))
                exists = cur.fetchone()
                cur.execute("SELECT id FROM snake_level WHERE name = %s", (user_name,))
                row = cur.fetchone()

                if not exists:
                    cur.execute("INSERT INTO snake (name) VALUES (%s)", (user_name))
                if not row:
                    save_all(snake.score, snake.level, FPS + snake.level - 1, user_name)
                elif exists[0] == row[0]:
                    update_all(snake.score, snake.level, FPS + snake.level - 1, user_name, row[0])
                
                snake.restart()
                
    
    # Fill Display with color
    screen.fill((13, 17, 23))
    

    if show_menu:
        start_menu()
        text_surface = font.render(user_name, True, (255, 255, 255))
        name_surface = font.render("Enter you name:", True, (255, 255, 255))
        screen.blit(text_surface, (250, 350))
        screen.blit(name_surface, (250, 300))
        pg.display.update()
        clock.tick(FPS + snake.level - 1)
        continue

    if snake.dead:
        sides = [0, 25, 0, 25]
        pg.draw.rect(screen, (21, 27, 35), (0, 0, W, H))
        you_dead = font.render("You Dead! (press R to restart)", True, 'red')
        your_score = font.render(f"Your score: {snake.score}", True, 'red')
        screen.blit(you_dead, (150, 300))
        screen.blit(your_score, (230, 330))
        pg.display.update()
        clock.tick(FPS + snake.level - 1)
        continue

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
    

conn.commit()

cur.close()
conn.close()
pg.quit()
exit()