import pygame
import random

# Initialize the pygame
pygame.init()

# creat the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('space-background.png')

# Title and Icon
pygame.display.set_caption('Space Invaders by Tye Garcia')
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = pygame.image.load('enemy-ship.png')
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 200)
enemy_x_change = 0.1
enemy_y_change = 40


# draw spaceship (player)
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Game Loop
running = True
while running:
    # RGB for screen
    screen.fill((80, 200, 120))
    # background for screen
    screen.blit(background, (0, 0))

    #
    for event in pygame.event.get():
        # Exit Game
        if event.type == pygame.QUIT:
            running = False

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -.2
            if event.key == pygame.K_RIGHT:
                player_x_change = .2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # draws player
    player_x += player_x_change

    # boundaries for player
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # enemy
    enemy_x += enemy_x_change

    # enemy boundaries
    if enemy_x <= 0:
        enemy_x_change = .1
        enemy_y += enemy_y_change
    elif enemy_x >= 736:
        enemy_x_change = -.1
        enemy_y += enemy_y_change

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    pygame.display.update()
