import pygame
from pygame import Vector2 as vtr 
import math
import random
import sys
import time

pygame.init()

# colours/images
background_col = (0, 0, 0)
player_col = (0, 255, 0)
objects_col = (255, 0, 0)
boundary_col = (255, 255, 255)
pop_col = (255, 255, 255)
small_ball_col = (169, 169, 169)

# parameters
window_width, window_height = 600, 600
position_x, position_y = 300, 300
radius = 5

# display 
pygame.display.set_caption("POP-POP")
window = pygame.display.set_mode((window_width, window_height))

# properties initialisation
position = vtr(position_x, position_y)

# List to store multiple falling objects
objects_list = []
pop_animations = []
small_balls = []

# Score and lives
score = 0
lives = 3
start_time = time.time()

# Fonts
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
retry_font = pygame.font.SysFont(None, 24)

# Load sounds
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Set volume for background music
pygame.mixer.music.play(-1)  # Play background music on a loop

pop_sound = pygame.mixer.Sound('pop_sound.wav')
pop_sound.set_volume(0.7)  # Set volume for pop sound

# Function to create a new falling object
def create_object():
    pos_x = random.randrange(0, window_width)
    pos_y = random.randrange(-100, -10)
    radius_obj = random.randrange(40, 60, 10)
    speed = random.randrange(1, 5)
    return [vtr(pos_x, pos_y), radius_obj, speed]

# Function to create small balls
def create_small_balls(position, original_radius):
    num_balls = original_radius // 10  # Number of small balls based on the size of the original object
    for _ in range(num_balls):
        speed = random.uniform(1, 3)
        small_balls.append([position, 5, speed])

# functions
def player(position, radius):
    pygame.draw.circle(window, player_col, (int(position.x), int(position.y)), radius, 0)

def draw_objects(objects_list):
    for obj in objects_list:
        pygame.draw.circle(window, boundary_col, (int(obj[0].x), int(obj[0].y)), obj[1] + 2, 0)  # Draw white boundary
        pygame.draw.circle(window, objects_col, (int(obj[0].x), int(obj[0].y)), obj[1], 0)  # Draw object

def update_objects(objects_list, elapsed_time):
    global score, lives
    for obj in objects_list:
        obj[0].y += obj[2] + elapsed_time * 0.01  # Increase speed over time
        if obj[0].y > window_height:
            objects_list.remove(obj)  # Remove object if it goes beyond the screen
            lives -= 1
        distance = math.sqrt((obj[0].x - position.x)**2 + (obj[0].y - position.y)**2)
        if distance <= radius + obj[1]:
            objects_list.remove(obj)  # Remove object if it collides with player
            score += 1
            pop_sound.play()  # Play pop sound
            pop_animations.append([obj[0], obj[1]])

def draw_pop_animations(pop_animations):
    for anim in pop_animations:
        pygame.draw.circle(window, pop_col, (int(anim[0].x), int(anim[0].y)), anim[1] + 2, 2)

def update_pop_animations(pop_animations):
    for anim in pop_animations:
        anim[1] += 2  # Increase radius
        if anim[1] > 30:  # Animation duration
            create_small_balls(anim[0], anim[1])
            pop_animations.remove(anim)

def draw_small_balls(small_balls):
    for ball in small_balls:
        pygame.draw.circle(window, small_ball_col, (int(ball[0].x), int(ball[0].y)), ball[1], 0)

def update_small_balls(small_balls):
    global score
    for ball in small_balls:
        ball[0].y += ball[2]  # Update the y position based on speed
        if ball[0].y > window_height:
            small_balls.remove(ball)  # Remove small ball if it goes beyond the screen
        distance = math.sqrt((ball[0].x - position.x)**2 + (ball[0].y - position.y)**2)
        if distance <= radius + ball[1]:
            small_balls.remove(ball)  # Remove small ball if it collides with player
            score += 1

def display_score_lives_timer(score, lives, elapsed_time):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    timer_text = font.render(f'Time: {int(elapsed_time)}', True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, window_height - 40))
    window.blit(timer_text, (window_width - 100, 10))

def display_game_over():
    game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
    retry_text = retry_font.render('Tap Spacebar to Retry', True, (255, 255, 255))
    window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - 36))
    window.blit(retry_text, (window_width // 2 - retry_text.get_width() // 2, window_height // 2 + 40))

def reset_game():
    global score, lives, objects_list, pop_animations, small_balls, start_time, radius
    score = 0
    lives = 3
    objects_list = [create_object() for _ in range(5)]
    pop_animations = []
    small_balls = []
    start_time = time.time()
    radius = 5

# game loop
running = True
game_over = False
clock = pygame.time.Clock()

# Create initial falling objects
for _ in range(5):
    objects_list.append(create_object())

while running:

    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if key[pygame.K_SPACE] and game_over:
            reset_game()
            game_over = False
        elif key[pygame.K_SPACE] and not game_over:
            radius += 2

    window.fill(background_col)

    elapsed_time = time.time() - start_time

    if not game_over:
        position = vtr(pygame.mouse.get_pos())

        update_objects(objects_list, elapsed_time)
        draw_objects(objects_list)
        draw_pop_animations(pop_animations)
        update_pop_animations(pop_animations)
        draw_small_balls(small_balls)
        update_small_balls(small_balls)

        player(position, radius)
        display_score_lives_timer(score, lives, elapsed_time)

        # Add new objects periodically
        if random.randrange(0, 100) < 2:  # Adjust the frequency of new objects
            objects_list.append(create_object())

        if lives <= 0:
            game_over = True
    else:
        display_game_over()

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

# game loop exit
pygame.quit()
sys.exit()
