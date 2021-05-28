# Imports
import pygame
import random
import math



# Window settings
WIDTH = 1560
HEIGHT = 975
TITLE = "SPACE WARS"
FPS = 60


#Game Stages
START = 0
PLAYING = 1
END = 2

# Create window
pygame.init()
pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (252, 244, 3)
GREEN = (52, 235, 82)
RED = (250, 10, 10)

# Load fonts
title_font = pygame.font.Font('assets/fonts/recharge bd.ttf', 80)
FONT_LG = pygame.font.Font("assets/fonts/Gameplay.ttf", 48)
default_font = pygame.font.Font(None, 40)

# Load images
ship_img = pygame.image.load('assets/images/playerShip.png').convert_alpha()
ship_img2 = pygame.image.load('assets/images/playerShip2.png').convert_alpha()
ship_img3 = pygame.image.load('assets/images/playerShip3.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyPurple.png').convert_alpha()
enemy2_img = pygame.image.load('assets/images/enemyBlack.png').convert_alpha()
enemy3_img = pygame.image.load('assets/images/enemyWhite.png').convert_alpha()
enemy4_img = pygame.image.load('assets/images/enemyGreen.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserBlue.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/powerupYellow_bolt.png').convert_alpha()
background_img = pygame.image.load('assets/images/planet.png').convert_alpha()
background1_img = pygame.image.load('assets/images/back.png').convert_alpha()
coin_img = pygame.image.load('assets/images/coin 2.png').convert_alpha()



# Load sounds
laser_snd = pygame.mixer.Sound('assets/sounds/laser.ogg')
explosion_snd = pygame.mixer.Sound('assets/sounds/explosion.ogg')
die_snd = pygame.mixer.Sound('assets/music/death.ogg')
over_snd = pygame.mixer.Sound('assets/music/gameover.ogg')
double_snd = pygame.mixer.Sound('assets/sounds/doubleshotpow.ogg')
powerup_snd = pygame.mixer.Sound('assets/sounds/powwerup.ogg')
bomb_snd = pygame.mixer.Sound('assets/sounds/bomb.ogg')
deadship_snd = pygame.mixer.Sound('assets/sounds/exploship.ogg')
level_snd = pygame.mixer.Sound('assets/sounds/levelup.ogg')
hit_snd = pygame.mixer.Sound('assets/sounds/hit.ogg')
blow_snd = pygame.mixer.Sound('assets/sounds/blowship.ogg')

#Music
start_music = ('assets/music/onemusic.ogg')
main_theme = ('assets/music/thememusic.ogg')


# Game classes
class Ship(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5
        self.shield = 5
        self.max_shield = 5
        self.shoots_double = False
        self.invincibility_time = 0

    def move_left(self):
        self.rect.x -= self.speed

        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def move_up(self):
        self.rect.y -= self.speed

        if self.rect.top < 0:
            self.rect.top = 0


    def move_down(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        
    def shoot(self):
        if self.shoots_double:
            x = self.rect.left + 3
            y = self.rect.centery 
            lasers.add( Laser(x, y, laser_img) )

            x = self.rect.right - 3
            y = self.rect.centery
            lasers.add( Laser(x, y, laser_img) )
        else:
            x = self.rect.centerx
            y = self.rect.top
            lasers.add( Laser(x, y, laser_img) )

        laser_snd.play()

    def check_bombs(self):
        if self.invincibility_time == 0:
            hits = pygame.sprite.spritecollide(self, bombs, True)

            for hit in hits:
                bomb_snd.play()
                self.shield-=1
                self.shoots_double = False

                if self.shield <= 0:
                      deadship_snd.play()
                      self.kill()
                    
        else:
            self.invincibility_time -= 1
 
    def check_powerups(self):
        hits = pygame.sprite.spritecollide(self, powerups, True)

        for hit in hits:
            hit.apply(self)
            print('yay!')
        
    def update(self):
        self.check_bombs()
        self.check_powerups()
     
class Laser(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 7

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
            laser_snd.play()

class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 4

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            laser_snd.play()
 
class ShieldPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

        
    def apply(self, ship):
        if ship.shield < 5:
            powerup_snd.play()
            ship.shield += 1
        else:
            ship.shield == 5

        player.score += 5
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            laser_snd.play()

class DoubleShotPowerup(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5

        
    def apply(self, ship):
        double_snd.play()
        ship.shoots_double = True
        player.score += 100
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            laser_snd.play()

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, image, shield, value):
        super(). __init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.sheild = shield
        self.value = value

    
    def drop_bomb(self):
        x = self.rect.centerx
        y = self.rect.bottom

      
        bombs.add( Bomb(x, y, bomb_img) )

        

    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
            hit_snd.play()
            self.sheild -= 1

        if self.sheild <= 0:
            blow_snd.play()
            self.kill()
            player.score += self.value

 
class Fleet(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.speed = 2
        self.bomb_rate = 2


    def move(self):
        reverse = False

        for sprite in self.sprites():
            sprite.rect.x += self.speed

            if sprite.rect.right > WIDTH or sprite.rect.left < 0:
                reverse = True

        if reverse:
            self.speed *= -1

    def select_bomber(self):

        sprites = self.sprites()

        if len(sprites) > 0:
            r = random.randrange(0,120)

            
            if r < self.bomb_rate + player.level:
                bomber = random.choice(sprites)
                bomber.drop_bomb()
            
        

    def update(self, *args):
        super().update(*args)

        self.move()

        if len(player) > 0:
            self.select_bomber()
        


# Setup
def new_game():
    global ship, player
    
    start_x = WIDTH /2
    start_y = HEIGHT - 100
    ship = Ship(start_x, start_y, ship_img)

    player = pygame.sprite.GroupSingle(ship)
    player.score = 0
    player.level = 1

    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)

def start_level():
   
    global enemies, lasers, bombs, powerups
    if player.level == 1:
            
            ship.shield = 5
            e1 = Enemy(150, 250, enemy_img, 1, 12)
            e2 = Enemy(300, 250, enemy4_img, 1, 12)
            e3 = Enemy(450, 250, enemy_img, 1,12)
            e4 = Enemy(300, 100, enemy_img, 3, 20)
            e5 = Enemy(300, 400, enemy_img, 3, 20)
            e6 = Enemy(150, 400, enemy4_img, 2, 15)
            e7 = Enemy(450, 400, enemy4_img, 2, 15)
            e8 = Enemy(300, 50, enemy_img, 1, 25)
            e9 = Enemy(220, 250, enemy4_img, 1, 25)
            e10 = Enemy(445, 250, enemy_img, 1, 25)
            e11 = Enemy(300, 400, enemy_img, 1, 25)
            e12 = Enemy(225, 400, enemy_img, 1, 25)
            e13 = Enemy(60, 250, enemy_img, 3, 25)
            e14 = Enemy(530, 250, enemy_img, 3, 25)
            e15 = Enemy(300, 600, enemy4_img, 2, 15)
            e16 = Enemy(225, 600, enemy_img,1, 25)
            e17 = Enemy(370, 600, enemy_img, 1, 25)
            e18 = Enemy(165, 600, enemy4_img, 1, 12)
            e19 = Enemy(430, 600, enemy_img, 1, 12)
            e20 = Enemy(70, 600, enemy4_img, 1, 12)
            e21 = Enemy(520, 600, enemy_img, 1, 12)
            e22 = Enemy(60, 400, enemy4_img, 1, 12)
            e23 = Enemy(545, 400, enemy4_img, 1, 12)
            e24 = Enemy(562, 700, enemy2_img, 3, 20)
            e25 = Enemy(40, 700, enemy2_img, 3, 20)
            enemies = Fleet(e1, e2, e4, e10, e11)

    if player.level == 2:
            level_snd.play()
            ship.shield = 5
            e1 = Enemy(150, 250, enemy_img, 1, 12)
            e2 = Enemy(300, 250, enemy4_img, 2, 12)
            e3 = Enemy(450, 250, enemy_img, 1,12)
            e4 = Enemy(300, 100, enemy_img, 1, 20)
            e5 = Enemy(300, 400, enemy_img, 3, 20)
            e6 = Enemy(150, 400, enemy4_img, 2, 15)
            e7 = Enemy(450, 400, enemy4_img, 2, 15)
            e8 = Enemy(300, 50, enemy_img, 1, 25)
            e9 = Enemy(220, 250, enemy4_img, 1, 25)
            e10 = Enemy(445, 250, enemy_img, 1, 25)
            e11 = Enemy(380, 400, enemy_img, 1, 25)
            e12 = Enemy(225, 400, enemy_img, 1, 25)
            e13 = Enemy(60, 250, enemy_img, 1, 25)
            e14 = Enemy(530, 250, enemy_img, 1, 25)
            e15 = Enemy(300, 600, enemy4_img, 2, 15)
            e16 = Enemy(225, 600, enemy_img,1, 25)
            e17 = Enemy(370, 600, enemy_img, 1, 25)
            e18 = Enemy(165, 600, enemy4_img, 1, 12)
            e19 = Enemy(430, 600, enemy_img, 1, 12)
            e20 = Enemy(70, 600, enemy4_img, 1, 12)
            e21 = Enemy(520, 600, enemy_img, 1, 12)
            e22 = Enemy(60, 400, enemy4_img, 1, 12)
            e23 = Enemy(545, 400, enemy4_img, 1, 12)
            e24 = Enemy(562, 700, enemy2_img, 3, 20)
            e25 = Enemy(40, 700, enemy2_img, 3, 20)
            enemies = Fleet(e1, e2, e4, e10, e11, e12, e13, e14)

    if player.level == 3:
            level_snd.play()
            ship.shield = 5
            e1 = Enemy(150, 250, enemy_img, 1, 12)
            e2 = Enemy(300, 250, enemy4_img, 1, 12)
            e3 = Enemy(450, 250, enemy_img, 1,12)
            e4 = Enemy(300, 100, enemy_img, 3, 20)
            e5 = Enemy(300, 400, enemy_img, 3, 20)
            e6 = Enemy(150, 400, enemy4_img, 2, 15)
            e7 = Enemy(450, 400, enemy4_img, 2, 15)
            e8 = Enemy(300, 50, enemy_img, 1, 25)
            e9 = Enemy(220, 250, enemy4_img, 1, 25)
            e10 = Enemy(445, 250, enemy_img, 1, 25)
            e11 = Enemy(380, 400, enemy_img, 1, 25)
            e12 = Enemy(225, 400, enemy_img, 1, 25)
            e13 = Enemy(80, 250, enemy3_img, 3, 25)
            e14 = Enemy(510, 250, enemy3_img, 3, 25)
            e15 = Enemy(300, 600, enemy4_img, 2, 15)
            e16 = Enemy(225, 600, enemy_img,1, 25)
            e17 = Enemy(370, 600, enemy_img, 1, 25)
            e18 = Enemy(165, 600, enemy4_img, 1, 12)
            e19 = Enemy(430, 600, enemy_img, 1, 12)
            e20 = Enemy(70, 600, enemy4_img, 1, 12)
            e21 = Enemy(520, 600, enemy_img, 1, 12)
            e22 = Enemy(60, 400, enemy4_img, 1, 12)
            e23 = Enemy(545, 400, enemy4_img, 1, 12)
            e24 = Enemy(562, 700, enemy2_img, 3, 20)
            e25 = Enemy(40, 700, enemy2_img, 3, 20)
            enemies = Fleet( e2, e4, e11, e12, e13, e14)



    if player.level == 4:
            level_snd.play()
            ship.shield = 5
            e1 = Enemy(150, 250, enemy_img, 1, 12)
            e2 = Enemy(300, 250, enemy4_img, 1, 12)
            e3 = Enemy(450, 250, enemy_img, 1,12)
            e4 = Enemy(300, 100, enemy_img, 3, 20)
            e5 = Enemy(300, 400, enemy3_img, 3, 20)
            e6 = Enemy(150, 400, enemy4_img, 2, 15)
            e7 = Enemy(450, 400, enemy4_img, 2, 15)
            e8 = Enemy(300, 80, enemy3_img, 1, 25)
            enemies = Fleet(e1, e2, e3, e5, e6, e7, e8)

    if player.level == 5:
            level_snd.play()
            ship.shield = 5
            e1 = Enemy(150, 250, enemy_img, 1, 12)
            e2 = Enemy(300, 250, enemy4_img, 1, 12)
            e3 = Enemy(450, 250, enemy_img, 1,12)
            e4 = Enemy(300, 100, enemy_img, 3, 20)
            e5 = Enemy(300, 400, enemy_img, 3, 20)
            e6 = Enemy(150, 400, enemy4_img, 2, 15)
            e7 = Enemy(450, 400, enemy4_img, 2, 15)
            e8 = Enemy(300, 50, enemy_img, 1, 25)
            e9 = Enemy(220, 250, enemy4_img, 1, 25)
            e10 = Enemy(445, 250, enemy_img, 1, 25)
            e11 = Enemy(360, 250, enemy4_img, 1, 25)
        
            enemies = Fleet( e1, e2, e4, e5, e6, e7, e9, e10, e11)

        
            
               
    elif player.level == 6:
                level_snd.play()
                ship.shield = 5
                e1 = Enemy(150, 250, enemy_img, 1, 12)
                e2 = Enemy(300, 250, enemy_img, 1, 12)
                e3 = Enemy(450, 250, enemy_img, 1,12)
                e4 = Enemy(300, 100, enemy3_img, 3, 20)
                e5 = Enemy(300, 400, enemy3_img, 3, 20)
                e6 = Enemy(150, 400, enemy3_img, 2, 15)
                e7 = Enemy(450, 400, enemy3_img, 2, 15)
                e8 = Enemy(300, 50, enemy4_img, 1, 25)
                e9 = Enemy(220, 250, enemy4_img, 1, 25)
                e10 = Enemy(380, 250, enemy4_img, 1, 25)
                e11 = Enemy(380, 400, enemy4_img, 1, 25)
                e12 = Enemy(225, 400, enemy4_img, 1, 25)
                e13 = Enemy(60, 250, enemy4_img, 3, 25)
                e14 = Enemy(525, 250, enemy4_img, 3, 25)
                e15 = Enemy(300, 600, enemy3_img, 2, 15)
                e16 = Enemy(225, 600, enemy4_img,1, 25)
                e17 = Enemy(370, 600, enemy4_img, 1, 25)
                e18 = Enemy(165, 600, enemy_img, 1, 12)
                e19 = Enemy(430, 600, enemy_img, 1, 12)
                e20 = Enemy(70, 600, enemy_img, 1, 12)
                e21 = Enemy(520, 600, enemy_img, 1, 12)
                e22 = Enemy(60, 400, enemy_img, 1, 12)
                e23 = Enemy(545, 400, enemy_img, 1, 12)
                e24 = Enemy(562, 700, enemy2_img, 3, 20)
                e25 = Enemy(40, 700, enemy2_img, 3, 20)
                enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e9, e10, e11, e12)
         
       
                
    elif player.level == 7:
                            level_snd.play()
                            ship.shield = 5
                            e1 = Enemy(150, 250, enemy_img, 1, 12)
                            e2 = Enemy(300, 250, enemy_img, 1, 12)
                            e3 = Enemy(450, 250, enemy_img, 1,12)
                            e4 = Enemy(300, 100, enemy2_img, 3, 20)
                            e5 = Enemy(300, 400, enemy2_img, 3, 20)
                            e6 = Enemy(150, 400, enemy3_img, 2, 15)
                            e7 = Enemy(450, 400, enemy3_img, 2, 15)
                            e8 = Enemy(300, 50, enemy4_img, 1, 25)
                            e9 = Enemy(220, 250, enemy4_img, 1, 25)
                            e10 = Enemy(380, 250, enemy4_img, 1, 25)
                            e11 = Enemy(380, 400, enemy4_img, 1, 25)
                            e12 = Enemy(225, 400, enemy4_img, 1, 25)
                            e13 = Enemy(60, 250, enemy4_img, 3, 25)
                            e14 = Enemy(525, 250, enemy4_img, 3, 25)
                            e15 = Enemy(300, 600, enemy3_img, 2, 15)
                            e16 = Enemy(225, 600, enemy4_img,1, 25)
                            e17 = Enemy(370, 600, enemy4_img, 1, 25)
                            e18 = Enemy(165, 600, enemy_img, 1, 12)
                            e19 = Enemy(430, 600, enemy_img, 1, 12)
                            e20 = Enemy(70, 600, enemy_img, 1, 12)
                            e21 = Enemy(520, 600, enemy_img, 1, 12)
                            e22 = Enemy(60, 400, enemy_img, 1, 12)
                            e23 = Enemy(545, 400, enemy_img, 1, 12)
                            e24 = Enemy(562, 700, enemy2_img, 3, 20)
                            e25 = Enemy(40, 700, enemy2_img, 3, 20)
                            enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e9, e10, e11, e12, e13, e14)




    elif player.level == 8:
                            level_snd.play()
                            ship.shield = 5
                            e1 = Enemy(150, 250, enemy_img, 1, 12)
                            e2 = Enemy(300, 250, enemy_img, 1, 12)
                            e3 = Enemy(450, 250, enemy_img, 1,12)
                            e4 = Enemy(300, 100, enemy2_img, 3, 20)
                            e5 = Enemy(300, 400, enemy2_img, 3, 20)
                            e6 = Enemy(150, 400, enemy3_img, 2, 15)
                            e7 = Enemy(450, 400, enemy3_img, 2, 15)
                            e8 = Enemy(300, 50, enemy4_img, 1, 25)
                            e9 = Enemy(220, 250, enemy4_img, 1, 25)
                            e10 = Enemy(380, 250, enemy4_img, 1, 25)
                            e11 = Enemy(380, 400, enemy4_img, 1, 25)
                            e12 = Enemy(225, 400, enemy4_img, 1, 25)
                            e13 = Enemy(60, 250, enemy4_img, 3, 25)
                            e14 = Enemy(525, 250, enemy4_img, 3, 25)
                            e15 = Enemy(300, 600, enemy3_img, 2, 15)
                            e16 = Enemy(225, 600, enemy4_img,1, 25)
                            e17 = Enemy(370, 600, enemy4_img, 1, 25)
                            e18 = Enemy(165, 600, enemy_img, 1, 12)
                            e19 = Enemy(430, 600, enemy_img, 1, 12)
                            e20 = Enemy(70, 600, enemy_img, 1, 12)
                            e21 = Enemy(520, 600, enemy_img, 1, 12)
                            e22 = Enemy(60, 400, enemy_img, 1, 12)
                            e23 = Enemy(545, 400, enemy_img, 1, 12)
                            e24 = Enemy(562, 700, enemy2_img, 3, 20)
                            e25 = Enemy(40, 700, enemy2_img, 3, 20)
                            enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14)

                    

                            

    elif player.level == 9:
                            level_snd.play()
                            ship.shield = 5
                            e1 = Enemy(150, 250, enemy_img, 1, 12)
                            e2 = Enemy(300, 250, enemy_img, 1, 12)
                            e3 = Enemy(450, 250, enemy_img, 1,12)
                            e4 = Enemy(300, 100, enemy2_img, 3, 20)
                            e5 = Enemy(300, 400, enemy2_img, 3, 20)
                            e6 = Enemy(150, 400, enemy3_img, 2, 15)
                            e7 = Enemy(450, 400, enemy3_img, 2, 15)
                            e8 = Enemy(300, 50, enemy4_img, 1, 25)
                            e9 = Enemy(220, 250, enemy4_img, 1, 25)
                            e10 = Enemy(380, 250, enemy4_img, 1, 25)
                            e11 = Enemy(380, 400, enemy4_img, 1, 25)
                            e12 = Enemy(225, 400, enemy4_img, 1, 25)
                            e13 = Enemy(60, 250, enemy4_img, 3, 25)
                            e14 = Enemy(525, 250, enemy4_img, 3, 25)
                            e15 = Enemy(300, 600, enemy3_img, 2, 15)
                            e16 = Enemy(225, 600, enemy4_img,1, 25)
                            e17 = Enemy(370, 600, enemy4_img, 1, 25)
                            e18 = Enemy(165, 600, enemy_img, 1, 12)
                            e19 = Enemy(430, 600, enemy_img, 1, 12)
                            e20 = Enemy(70, 600, enemy_img, 1, 12)
                            e21 = Enemy(520, 600, enemy_img, 1, 12)
                            e22 = Enemy(60, 400, enemy_img, 1, 12)
                            e23 = Enemy(545, 400, enemy_img, 1, 12)
                            e24 = Enemy(562, 700, enemy2_img, 3, 20)
                            e25 = Enemy(40, 700, enemy2_img, 3, 20)
                            enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25)


                    







    elif player.level == 10:
                            level_snd.play()
                            ship.shield = 5
                            e1 = Enemy(150, 250, enemy_img, 1, 12)
                            e2 = Enemy(300, 250, enemy_img, 1, 12)
                            e3 = Enemy(450, 250, enemy_img, 1,12)
                            e4 = Enemy(300, 100, enemy2_img, 3, 20)
                            e5 = Enemy(300, 400, enemy2_img, 3, 20)
                            e6 = Enemy(150, 400, enemy3_img, 2, 15)
                            e7 = Enemy(450, 400, enemy3_img, 2, 15)
                            e8 = Enemy(300, 50, enemy4_img, 1, 25)
                            e9 = Enemy(220, 250, enemy4_img, 1, 25)
                            e10 = Enemy(380, 250, enemy4_img, 1, 25)
                            e11 = Enemy(380, 400, enemy4_img, 1, 25)
                            e12 = Enemy(225, 400, enemy4_img, 1, 25)
                            e13 = Enemy(60, 250, enemy4_img, 3, 25)
                            e14 = Enemy(525, 250, enemy4_img, 3, 25)
                            e15 = Enemy(300, 600, enemy3_img, 2, 15)
                            e16 = Enemy(225, 600, enemy4_img,1, 25)
                            e17 = Enemy(370, 600, enemy4_img, 1, 25)
                            e18 = Enemy(165, 600, enemy_img, 1, 12)
                            e19 = Enemy(430, 600, enemy_img, 1, 12)
                            e20 = Enemy(70, 600, enemy_img, 1, 12)
                            e21 = Enemy(520, 600, enemy_img, 1, 12)
                            e22 = Enemy(60, 400, enemy_img, 1, 12)
                            e23 = Enemy(545, 400, enemy_img, 1, 12)
                            e24 = Enemy(562, 700, enemy2_img, 3, 20)
                            e25 = Enemy(40, 700, enemy2_img, 3, 20)
                            enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25)

                    

                            

                    

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()



    x = random.randint(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p1 = ShieldPowerup(x, y, powerup_img)


    x = random.randint(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p2 = DoubleShotPowerup(x, y, coin_img)

    x = random.randint(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p3 = ShieldPowerup(x, y, powerup_img)

    x = random.randint(0, WIDTH)
    y = random.randrange(-3000, -1000)
    p4 = ShieldPowerup(x, y, powerup_img)

    powerups = pygame.sprite.Group(p1, p2, p3, p4)

   
    
def display_stats():
    score_text = default_font.render("Score: " + str(player.score), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.left = 20
    screen.blit(score_text, rect)

    level_text = default_font.render("Level: " + str(player.level), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.right = WIDTH - 20
    screen.blit(level_text, rect)

   



   





def draw_shield():

    if ship.shield is 1:

        pygame.draw.rect(screen, RED, [120, 930, 50, 25])


    if ship.shield is 2:

    
        pygame.draw.rect(screen, YELLOW, [120, 930, 100, 25])

 
    if ship.shield is 3:
      
     
        pygame.draw.rect(screen, YELLOW, [120, 930, 200, 25])


    if ship.shield is 4:

      
        pygame.draw.rect(screen, GREEN, [120, 930, 300, 25])


    if ship.shield is 5:
       
        pygame.draw.rect(screen, GREEN, [120, 930, 400, 25])

    

 


       

       




def start_screen():

    screen.fill(YELLOW)
    screen.blit(background1_img, [0,0])
    title_text = title_font.render(TITLE, True, WHITE)
    rect = title_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.bottom = HEIGHT // 2
    screen.blit(title_text, rect)

    sub_text = default_font.render("Press any key to start", True, WHITE)
    rect = sub_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.top = HEIGHT // 2
    screen.blit(sub_text, rect)


def end_screen():
    end_text = default_font.render("Game Over", True, WHITE)
    rect = end_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.centery = HEIGHT // 2
    screen.blit(end_text, rect)
  


# Game loop
new_game()
start_level()
stage = START
                    
running = True

while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if stage == START:
                stage = PLAYING
                pygame.mixer.music.load(main_theme)
                pygame.mixer.music.play(-1)


            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == END:
                if event.key == pygame.K_r:
                    new_game()
                    start_level()
                    stage = START
    
    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

    
    # Game logic
    if stage != START:
        lasers.update()
        bombs.update()
        enemies.update()
        player.update()
        powerups.update()
        
    
    if len (enemies) == 0:
        player.level += 1
        start_level()
    elif len(player) == 0:
        stage = END
    
    # Drawing code
    
    screen.fill(YELLOW)
    screen.blit(background_img, [0,0])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    powerups.draw(screen)
    display_stats()
    draw_shield()

    if stage == START:
        start_screen()
    elif stage == END:
        end_screen()
        over_snd.play()


        

        
    # Update screen
    pygame.display.update()


    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()
    

