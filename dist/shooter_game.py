

from pygame import *
from random import randint
import time as when

clock = time.Clock()
FPS = 30

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#fonts and captions
font.init()
font2 = font.Font(None, 36)

#we need the following images:
img_back = "galaxy.jpg" # game background
img_hero = "rocket.png" # hero
img_enemy = "ufo.png" # enemy

score = 0 #ships destroyed
lost = 0 #ships missed

enemy_cooldown = 0
shot_speed = 30

class Bullet(sprite.Sprite):
    def __init__(self, bullet_image, bullet_x = 250, bullet_y = 250, bullet_size = 35):
        super().__init__()
        self.image = transform.scale(image.load(bullet_image), (bullet_size, bullet_size))
        self.rect = self.image.get_rect()
        self.rect.x = bullet_x
        self.rect.y = bullet_y
        
    def bliting(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def get_shot(self, who):
        x = who.rect.centerx
        y = who.rect.centery
        self.rect.x = x
        self.rect.y = y

    def update(self, direction):
        if direction == 'up':
            self.rect.y -= 10
        elif direction == 'down':
            self.rect.y += 10
        else:
            self.rect.x += randint(-10,10)



#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)

        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        #every sprite must have the rect property that represents the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def get_x(player_x):
        return player_x
    def get_y(player_y):
        return player_y

#main player class
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #method to "shoot" (use the player position to create a bullet there)


#enemy sprite class
class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            # self.speed = randint(1, 5)
        global enemy_cooldown
        if enemy_cooldown == 0:
            enemy_bullet = Bullet('recourcess/bullet.png')
            enemy_bullets.add(enemy_bullet)
            enemy_bullet.get_shot(self)
        enemy_bullets.update('down')
        enemy_bullets.draw(window)



#create a small window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

enemy_amount = 5

#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()

for i in range(enemy_amount):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()
enemy_bullets = sprite.Group()

#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False

#Main game loop:
run = True #the flag is reset by the window close button

while run:
    #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        #update the background
        window.blit(background,(0,0))

        #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))



    
        keys = key.get_pressed()
        if keys[K_SPACE]:
            bullet = Bullet('recourcess/bullet.png')
            bullets.add(bullet)
            bullet.get_shot(ship)

        bullets.update('up')
        bullets.draw(window)
        


        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #launch sprite movements
        ship.update()
        monsters.update()



        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)

        display.update()

        enemy_cooldown += 1
        if enemy_cooldown == shot_speed:
            enemy_cooldown = 0

    #the loop is executed each 0.05 sec
    clock.tick(FPS)

