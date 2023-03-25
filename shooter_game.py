from pygame import *
import random
from time import time as timer



class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)
               
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
            bullets.add(bullet)        

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Meteorit(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
             
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fireSound = mixer.Sound('fire.ogg')



font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render('ТЫ ВЫИГРАЛ!', True, (0, 255, 0))
lose = font1.render('ТЫ ПРОИГРАЛ!', True, (255, 0, 0))
font2 = font.SysFont('Arial', 36)


img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_meteorit = 'asteroid.png'

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back),(win_width, win_height))


lost = 0
score = 0
life = 3
life_color = ''
ship = Player(img_hero, 5, win_height - 110, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, random.randint(80, win_width-80), -40, 80, 40, random.randint(1,5))
    monsters.add(monster)
meteorits = sprite.Group()
for i in range(2):
    meteorit = Meteorit(img_meteorit, random.randint(80, win_width-80), -40, 40, 40, random.randint(5,10))
    meteorits.add(meteorit)

bullets = sprite.Group()

run = True
finish = False

rel_time = 0
# ! подчет выпущенных пуль
num_fire = 0

clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    #fireSound.play()
                    ship.fire()

                    if num_fire >= 5 and rel_time == False:
                        # ! засечь время после того как было произведенно 5 выстрелов
                        last_time = timer()
                        # начинать перезарядку
                        rel_time = True

        
    if finish != True:
        window.blit(background, (0,0))

        text = font2.render('Счет:' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (20,50))

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        meteorits.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score += 1
            monster = Enemy(img_enemy, random.randint(80, win_width-80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)

        ship.update()
        monsters.update()
        bullets.update()
        meteorits.update()

        if rel_time == True:
            #! засекаем время от начала перезарядки
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Ждите, идет прерзарядка...', 1, (200,0,0))
                window.blit(reload, (250, 450))
            else:
                #! сбросить счетчик потронов и отменить перезарядку
                num_fire = 0
                rel_time = False    



        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, meteorits, True):
            life -= 1

        if lost >= 10 or life == 0:
            finish = True
            window.blit(lose, (win_width//3, win_height//2))

        if score >= 10:
            finish = True
            window.blit(win, (win_width//3, win_height//2))

        if life == 3:
            life_color = (0,255,0)
        elif life == 2:
            life_color = (255,238,0)
        else:
            life_color == (255,0,0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    else:
        finish = False
        lost = 0
        score = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for ufo in monsters:
            ufo.kill()

        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, random.randint(80, win_width-80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)
        for i in range(2):
            meteorit = Enemy(img_enemy, random.randint(80, win_width-80), -40, 80, 40, random.randint(1,5))
            meteorits.add(meteorit)       
    time.delay(50)
