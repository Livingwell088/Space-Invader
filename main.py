'''Adaptation of the old arcade game
"Space Invaders". It is a game where the player
controls a space ship in space and the objective to
kill all the enemies/aliens before they reach a
certain spot and you lose
You can control your ship to go left or right
using the left and right arrow keys and also
shoot a bullet to kill the enemies by pressing the space bar.
Have Fun and Don't Die!!!!!!!!!!!!'''

# By Nicholas Li


#Imports
import pygame
import random
import math


# Initialize Pygame
pygame.init()



# Creating a game window
screen = pygame.display.set_mode((800, 600))    # Screen window 800 pixels wide by 600 pixels tall


#Background
background = pygame.image.load("background.jpg")    # A cool background image that looks like space
background = pygame.transform.scale(background, (800, 600))
# Changing Title, Background Color, and Logo

#Title
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.jpg")
pygame.display.set_icon(icon)


# Player
# A spaceship 64 pixels wide
playerImg = pygame.image.load("ship.png")
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 380
playerY = 470
playerX_change = 0


# Enemy/Alien
# An alien is also 62 pixels wide and there are 6 of them spawned in at once.
# The alien can spawn anywhere in a set boundary
# Everytime that one is killed, one more spawn in its place so there are always 6
# Every one killed is one point

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    alien = pygame.image.load("alien.png")
    alien = pygame.transform.scale(alien, (64, 64))
    enemyImg.append(alien)
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(  0.15)
    enemyY_change.append(  40)


# Bullet
# An energy blast that the ship uses to kill the enemy.
# It is a one hit kill , however you only have one charge until it either hits or goes off the screen

# Ready - You cannot see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load("bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (32, 32))
bulletX = 0
bulletY = 470
bulletX_change = 0
bulletY_change = 0.75
bullet_state = "ready"

# Score
score_value = 0

#Font
font = pygame.font.Font("Metal Lady - Personal Use.otf", 64)
textX = 10
textY = 10

# game_over_text

over_text = pygame.font.Font("Metal Lady - Personal Use.otf", 100)



# Functions

# Game Over Text, Text that will be displayed when you lose
def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

# A text on screen that will show your score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Player Function
def player(x, y):
    screen.blit(playerImg, (x, y))

#Enemy Function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Shoots bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 18, y + 10))

# Detects whether a bullet is close enough to an enemy, if it is
# the player gets one point and that specific enemy dies/despawns
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

running = True
while running:

    # RGB Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # If the x is press, the program exits and closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if keystroke is pressed, check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        # If the key is unpressed, the player stops
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Player Boundary Making sure the ship will not leave the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy Boundary Making sure the aliens will not leave the screen
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.15
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)


    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

