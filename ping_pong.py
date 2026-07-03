from pygame import *
from random import shuffle
w, h = 1400, 965
window = display.set_mode((w, h))
rand_speed = [-1,1]
display.set_caption('Warhammer 40k ping_pong')
background = transform.scale(image.load('image.jpeg'),(w, h))
mixer.init()
mixer.music.load('backmusic.mp3')
mixer.music.play()
mixer.music.set_volume(0.2)
font.init()
score_left = 0
score_right = 0
font1 = font.SysFont('Arial', 40)
font2 = font.SysFont('Arial', 100)
finish = False
class GameSprite(sprite.Sprite):
    def __init__(self, plr_image, plr_x, plr_y, plr_speed, plr_width, plr_height):
        super ().__init__()
        self.image = transform.scale(image.load(plr_image), (plr_width, plr_height))
        self.speed = plr_speed
        self.rect = self.image.get_rect()
        self.rect.x = plr_x
        self.rect.y = plr_y
        self.width = plr_width
        self.height = plr_height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < h-self.height: 
            self.rect.y +=  self.speed

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < h-self.height: 
            self.rect.y +=  self.speed

class Ball(GameSprite):
    def __init__(self, plr_image, plr_x, plr_y, plr_speed, plr_width, plr_height):
        super().__init__(plr_image, plr_x, plr_y, plr_speed, plr_width, plr_height)
        shuffle(rand_speed)
        self.speed_x = self.speed*rand_speed[0]
        shuffle(rand_speed)
        self.speed_y = self.speed*rand_speed[0]
    def update(self):
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y <= 0 or self.rect.y >= h-self.height:
            self.speed_y *= -1
        if sprite.collide_rect(self, mag):
            self.speed_x = -self.speed
        if sprite.collide_rect(self, mechanikus):
            self.speed_x = self.speed


mag = Player('koldun.png', 50, 440, 12, 100, 245)
mechanikus = Player('mechanikus.png', 1225, 440, 12, 120,245)
ball = Ball('ball.png', 650, 432, 12, 100, 100)
game = True
while game:
    window.blit(background, (0,0))
    
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        mag.reset()
        mag.update()
        mechanikus.reset()
        mechanikus.update2()
        ball.reset()
        ball.update()
    text_left = font1.render('Счет:' + str(score_left), 1, (255, 255, 255))
    text_right = font1.render('Счет:' + str(score_right), 1, (255, 255, 255))
    window.blit(text_left, (10,20))
    window.blit(text_right, (1280,20))
    if ball.rect.x < 0:
        score_right += 1
        ball.rect.x = 650
        ball.rect.y = 432
    if ball.rect.x > 1300:
        score_left += 1
        ball.rect.x = 650
        ball.rect.y = 432
    if score_right >= 5:
        finish_text = font2.render('Победа за Механикусом', 1,  (255, 0, 0))
        window.blit(finish_text, (255,360))
        finish = True
    if score_left >= 5:
        finish_text2 = font2.render('Победа за Магом', 1,  (0, 255, 0))
        window.blit(finish_text2, (375,360))
        finish = True
    
    display.update()
    time.delay(30)
