import pygame as pg
import random as rd
import math as m

from pygame import mixer

# initialize the game
pg.init()

# score
score_value = 0
font = pg.font.Font("ARCADECLASSIC.TTF", 32)

textX = 10
textY = 10

# game over text
over_font = pg.font.Font("ARCADECLASSIC.TTF", 64)

# create the screen (width, high)
screen = pg.display.set_mode((800, 600))

# background
background = pg.image.load("background.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Tittle and Icon
pg.display.set_caption("Space Invaders")
icon = pg.image.load("ufo.png")
pg.display.set_icon(icon)

# Player
playerImg = pg.image.load("player.png")
playerX = 470
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pg.image.load("enemy.png"))
    enemyX.append(rd.randint(0, 735))
    enemyY.append(rd.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pg.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
# ready - you cant see the bullet on the screen, fire - the bullet is currenctly moving
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(ex, ey, bx, by):
    distance = m.sqrt(m.pow((ex - bx), 2) + m.pow((ey - by), 2))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over!", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))


def check_boundaries(x, y):
    if x >= 736:
        x = 736
    elif x <= 0:
        x = 0
    if y >= 536:
        y = 536
    elif y <= 0:
        y = 0
    return x, y


# Game loop
running = True
while running:
    # RGB Red, Green, Blue
    screen.fill((128, 128, 128))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                playerX_change = -3
            if event.key == pg.K_RIGHT:
                playerX_change = 3
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            '''if event.key == pg.K_UP:
                playerY_change = -0.3
            if event.key == pg.K_DOWN:
                playerY_change = 0.3'''
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                playerX_change = 0
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                playerY_change = 0
    playerX += playerX_change
    # playerY += playerY_change
    playerX, playerY = check_boundaries(playerX, playerY)
    for i in range(num_of_enemies):

        # game over
        #collision_
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        enemyX[i], enemyY[i] = check_boundaries(enemyX[i], enemyY[i])
        if enemyX[i] == 736 or enemyX[i] == 0:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]
            # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = rd.randint(0, 735)
            enemyY[i] = rd.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pg.display.update()

pg.quit()
