import math
import random

import pygame
from pygame import mixer

# initiate the pygame
pygame.init()

# create the game window
# 800 by 600 pixels
screen = pygame.display.set_mode((800, 600))

# background image
# haunted cemetery image
background = pygame.image.load('img.png')

# game window title and logo
# "CMPT 120: Marist Platformer
# red fox logo
pygame.display.set_caption("CMPT 120: Marist Platformer")
icon = pygame.image.load('redfox.png')
pygame.display.set_icon(icon)

# player image and location
playerImg = pygame.image.load('flashlight3.png')
playerX = 370
playerY = 480
playerX_change = 0

# ghost movement and number of ghosts at one time (7)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

# ghost image and spawn area
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(30)

# bullet image, bullet path, and bullet loaded state "ready"
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.25
bullet_state = "ready"

# score location on HUD, font of score, and initial score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# game over font and condition
over_font = pygame.font.Font('freesansbold.ttf', 64)

game_over = False

# score value and color
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# game over condition for it to be displayed and to restart game to be displayed
def game_over_text():
    global game_over
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    display_restart = font.render("press SPACE to restart", True, (255, 255, 255))
    screen.blit(display_restart, (210, 320))
    game_over = True

# player function
def player(x, y):
    screen.blit(playerImg, (x, y))

# ghost function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# shooting function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# collision between bullet and ghost function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    # background color
    # rbg - red, blue, green
    screen.fill((0, 0, 0))
    # background image of haunted cementary
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check
        # key left = accelerate left
        # key right = accelerate right
        # key space = shoot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        # if keystroke button release check
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE and game_over:
                playerX = 370
                playerY = 480
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                game_over = False

    # player movement boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # ghost movement
    for i in range(num_of_enemies):

        # game over initiated
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_over = True
            break

        # enemy path
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # collision funtion to be triggered
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet path
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # bullet reload
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # game consistently runs
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()