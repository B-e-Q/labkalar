import pygame as pg
import time
import random

pg.init()
pg.mixer.init()


# Play background music
pg.mixer.music.load('sounds/background.wav')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)


# Width and Height of the display
W = 400
H = 600

screen = pg.display.set_mode((W, H))

clock = pg.time.Clock()
FPS = 60

pg.display.set_caption("Racer!")


# Graphics
bg_img = pg.image.load("graphs/AnimatedStreet.png")
player_img = pg.image.load("graphs/Player.png")
enemy_img = pg.image.load("graphs/Enemy.png")
coin_img = [pg.transform.scale(pg.image.load("graphs/coin.png"), (30, 30)),
            pg.transform.scale(pg.image.load("graphs/red.png"), (40, 40)),
            pg.transform.scale(pg.image.load("graphs/pink.png"), (40, 40))
            ]


bgy = 0

# Sounds
sound_crash = pg.mixer.Sound('sounds/crash.wav')


# Fonts
font = pg.font.SysFont("Verdana", 60)
game_over = font.render("Game Over", True, "black")
game_over_rect = game_over.get_rect(center = (W // 2, H // 2))

def drawtext(score):
    score_text = font.render(f"Score: {score}", True, "WHITE")
    screen.blit(score_text, (10, 10))



# Player 
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = W // 2
        self.rect.bottom = H
        self.speed = 5

    # Move Left or Right
    def move(self):
        key = pg.key.get_pressed()
        
        # Pressed keys action
        if key[pg.K_d]:
            self.rect.move_ip(self.speed, 0)
        if key[pg.K_a]:
            self.rect.move_ip(-self.speed, 0)
        
        # Object outside of the display
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > W:
            self.rect.right = W

# Enemy
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.speed = 10
    
    # Generates Enemy 
    def gen_rect(self):
        self.rect.left = random.randint(0, W - self.rect.w)
        self.rect.bottom = 0
    
    # Move To The Bottom
    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > H:
            self.gen_rect()



# Coin
class Coin(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i = 0
        self.img = coin_img[self.i]
        self.rect = self.img.get_rect()
        self.speed = 7
        self.score = 0
    

    #generates coins
    def gen_coin(self):
        self.rect.left = random.randint(0, W - self.rect.w)
        self.rect.bottom = 0
        self.i = random.randint(0, 2)
        self.img = coin_img[self.i]
    
    # Move To The Bottom
    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > H:
            self.gen_coin()
        elif self.rect.colliderect(player.rect):
            self.score += (self.i+1) * 10
            self.gen_coin()
        else:
            screen.blit(self.img, self.rect)
        
        if self.score > 500:
            self.speed = 12
        elif self.score > 300:
            self.speed = 10


# Get every class
player = Player()
enemy = Enemy()
coin = Coin()


all_sprites = pg.sprite.Group()
enemy_sprites = pg.sprite.Group()

all_sprites.add(player, enemy)
enemy_sprites.add(enemy)


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
            exit()
    

    # Infinity Moving Back Ground
    screen.blit(bg_img, (0, bgy))
    screen.blit(bg_img, (0, bgy - H))

    # Make infinity Moving Background from Top to Bottom
    bgy += 5
    if bgy == H:
        bgy = 0

    player.move()

    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)
    
    # Activat coins actions
    coin.move()

    # Write text on display
    drawtext(coin.score)
    
    # Screen if car is crushed
    if pg.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        run = False
        screen.fill("red")
        screen.blit(game_over, game_over_rect)
        pg.display.flip()

        time.sleep(3)


    pg.display.update()
    clock.tick(FPS)