import pygame
import random
import math

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
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for enemy in range(num_enemies):
    enemy_img.append(pygame.image.load('enemy-ship.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.1)
    enemy_y_change.append(40)


# laser
laser_img = pygame.image.load('laser.png')
laser_x = 0
laser_y = 480
laser_x_change = 0
laser_y_change = .5
# Ready - laser not on screen
# Fire - laser is moving
laser_state = "ready"

score = 0

# draw spaceship (player)
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, laser_x, laser_y):
    distance = math.sqrt((math.pow(enemy_x - laser_x, 2)) + (math.pow(enemy_y - laser_y, 2)))
    if distance < 27:
        return True
    return False


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
            if event.key == pygame.K_SPACE:
                # fire one laser at a time
                if laser_state == "ready":
                    # Gets current x coordinate of player
                    laser_x = player_x
                    fire_laser(laser_x, laser_y)

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
    for i in range(num_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = .1
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -.1
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], laser_x, laser_y)
        if collision:
            laser_y = 480
            laser_state = "ready"
            score += 1
            print(score)
            # kill and create new enemy
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)


    # Laser Movement
    if laser_y <= 0:
        laser_y = 480
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laser_x, laser_y)
        laser_y -= laser_y_change


    player(player_x, player_y)
    pygame.display.update()
