import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# creat the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('images/space-background.png')

# Background sound
mixer.music.load('sound/background.wav')
mixer.music.play(-1)  # plays music in loop
pygame.mixer.music.set_volume(0.1)

# Title and Icon
pygame.display.set_caption('Space Invaders by Tye Garcia')
icon = pygame.image.load('images/alien.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('images/spaceship.png')
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
    enemy_img.append(pygame.image.load('images/enemy-ship.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.1)
    enemy_y_change.append(40)

# laser
laser_img = pygame.image.load('images/laser.png')
laser_x = 0
laser_y = 480
laser_x_change = 0
laser_y_change = .5
# Ready - laser not on screen
# Fire - laser is moving
laser_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game Over Message
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_message():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


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
                    laser_sound = mixer.Sound('sound/laser.wav')
                    laser_sound.play()
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

        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_message()
            break

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
            explosion_sound = mixer.Sound('sound/explosion.wav')
            explosion_sound.play()
            explosion_sound.set_volume(0.3)
            laser_y = 480
            laser_state = "ready"
            score_value += 1
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
    show_score(text_x, text_y)
    pygame.display.update()
