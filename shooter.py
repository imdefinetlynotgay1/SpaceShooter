from pygame import *
from random import randint
from time import time as timer

img_ufo = "ufo.png"
img_galaxy = "galaxy.jpg"
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"
img_rocket = "rocket.png"

win_width = 500
win_height = 700

window = display.set_mode((win_width, win_height))
display.set_caption("Space Shooter")
background = transform.scale(image.load(img_galaxy), (win_width, win_height))

lost = 0
goals = [6, 12, 18, 24]
healths = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_img, player_x, player_y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_d] and self.rect.x < 450:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

    def fire(self):
        global num_fire, total_bullets
        if num_fire > 0:
            bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
            bullets.add(bullet)
            total_bullets += 1

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = -40
            lost += 1


class Bullet(GameSprite):
    def update(self):
        global bullet_missed
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
            bullet_missed += 1


player = Player(img_rocket, 5, win_height - 100, 80, 100, 10)

# asteroids = sprite.Group()
# for i in range(3):
#     asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
#     asteroids.add(asteroid)

ufos = sprite.Group()
def get_ufos(level):
    for i in range(6):
        ufo = Enemy(img_ufo, randint(80, win_width - 80), -40, 80, 50, randint(1,7 - level))
        ufos.add(ufo)

bullets = sprite.Group()

font.init()
font1 = font.SysFont(None, 50)
win = font1.render("YOU WIN!", True, (0, 255, 0))
lose = font1.render("YOU SUCK!", True, (255, 0, 0))
pause_text = font1.render("GAME PAUSED", True, (255, 0, 0))

font2 = font.SysFont(None, 36)


finish = False
game_over = True
num_fire = 0
FPS = 60
clock = time.Clock()
score = 0
level = 0
current_point = 0
new_level = True
checkpoint = 0
game_status = None
accuracy = 0
bullet_missed = 0
total_bullets = 0

def get_bullet(level):
    global num_fire
    num_fire = goals[level]
    return num_fire + 2

while game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and num_fire > 0:
                player.fire()
                num_fire -= 1

            if e.key == K_x and finish:
                game_over = False
            if e.key == K_r and finish:
                finish = False
                num_fire = 0
                score = 0
                level = 0
                current_point = 0
                new_level = True
                checkpoint = 0
                game_status = None
                accuracy = 0
                bullet_missed = 0
                total_bullets = 0
                lost = 0
            
            if e.key == K_p and game_status == None:
                game_status = "pause"
                finish = True

            elif e.key == K_p and game_status == "pause":
                game_status = None
                finish = False
        
    if not finish:
        window.blit(background, (0,0))
        player.update()
        ufos.update()
        # asteroids.update()
        bullets.update()

        player.reset()
        ufos.draw(window)
        # asteroids.draw(window)
        bullets.draw(window)

        score_text = font2.render("Score(s):" + str(score), True, (255, 255, 255))
        window.blit(score_text, (10, 20))

        if sprite.groupcollide(bullets, ufos, True, True):
            score += 1
            current_point += 1

        if len(ufos) == 0:
            get_ufos(level)

        if new_level == True and level < 3:   
            num_fire = get_bullet(level)
            checkpoint += goals[level]
            new_level = False

        if current_point == goals[level]:
            level += 1
            total_bullets += current_point
            current_point = 0
            new_level = True

        if current_point == goals[level] and level == 3:
            # window.blit(win, (150, 300))
            game_status = "win"
            finish = True

        if num_fire == 0 and len(ufos) != 0 and len(bullets) == 0 and current_point < goals[level]:
            # window.blit(lose, (150, 300))
            game_status = "lose"
            finish = True

        health_text = font2.render("Bullets: " + str(num_fire), True, (255, 255, 255))
        window.blit(health_text, (10, 50))

        level_text = font2.render("Level: " + str(level + 1), True, (255, 255, 255))
        window.blit(level_text, (10, 70))

        check_text = font2.render("Need to reach: " + str(checkpoint), True, (255, 255, 255))
        window.blit(check_text, (10, 90))

    if finish:
        
        window.blit(background, (0,0))

        if game_status == "win":
            window.blit(win, (120, 300))            
        elif game_status == "lose":
            window.blit(lose, (120, 300))
        elif game_status == "pause":
            window.blit(pause_text, (120, 300))
        try:    
            accuracy = round((score / total_bullets) * 100, 2)
            player.kill()

            for bullet in bullets:
                bullet.kill()

            for ufo in ufos:
                ufo.kill()
            acc_text = font2.render("YOUR ACCURACY: " + str(accuracy) + "%", True, (255, 255, 255))
            window.blit(acc_text, (120, 340))

            score_text = font2.render("YOUR SCORE: " + str(score), True, (255, 255, 255))
            window.blit(score_text, (120, 370))

            missed_text = font2.render("ENEMIES YOU MISSED: " + str(lost) , True, (255, 255, 255))
            window.blit(missed_text, (120, 400))
        except:
            pass

        restart_text = font1.render("Press 'R' to restart!", True, (0, 255, 0))
        window.blit(restart_text, (100, 500))

        stop_text = font1.render("Press 'X' to exit!", True, (0, 255, 0))
        window.blit(stop_text, (100, 540))
        display.update()
        clock.tick(FPS)

    display.update()
    clock.tick(FPS)
    