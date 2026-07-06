# This is a Simple Snake Game made by Benjibyte for a teaching excersize. No AI generation is used. All code is written
# hand or using PyCharm's autocomplete. AI was, however, used as a tutor in a few minor instances for researching
# different methods and procedures in python and pygame-ce's documentation for learning purposes.
# July 2nd, 2026
import pygame
import random
red = (255, 100, 100)
green = (150, 200, 110)
black = (50,60,70)
score = 0
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
running = True
keys = pygame.key.get_pressed()
# Screen
screen.fill(black) # Background color
# Snake
width = 18
step = 2
growth = 16
snake_length = 24 # initial length of snake
x = 300 # the positions of the snake's head
y = 300
snake_direction = "right"
snake = []
for i in range(snake_length):
    collision_box = pygame.Rect(x, y, width, width)
    snake.append([x, y, collision_box])
    x += step
def add_node(snake_list, direction, step_int, width):
    snake_head = snake_list[-1]
    old_x = snake_head[0]
    old_y = snake_head[1]
    new_x = 0
    new_y = 0
    if direction == "left":
        new_x = old_x - step_int
        new_y = old_y
    elif direction == "right":
        new_x = old_x + step_int
        new_y = old_y
    elif direction == "up":
        new_x = old_x
        new_y = old_y - step_int # Remember! going down is up in pygame
    elif direction == "down":
        new_x = old_x
        new_y = old_y + step_int
    # Get pygame.Rect Collision box
    new_collision = pygame.Rect(new_x, new_y, width, width)
    return [new_x, new_y, new_collision]
def draw(screen, snake, width):
    for node in snake:
        pygame.draw.rect(screen, green, (node[0], node[1], width, width), border_radius=8)
def remove_node(snake, length=snake_length):
    if len(snake) > length:
        snake.pop(0)
def detect(thing_to_detect, snake_list, direction, snake_width):
    snake_head = snake_list[-1]
    # Using Pygame's built in Rect() hitboxes functions
    sensor = pygame.Rect(snake_head[0], snake_head[1], snake_width, snake_width)
    if direction == "left":
        sensor.x -= snake_width
    elif direction == "right":
        sensor.x += snake_width
    elif direction == "up":
        sensor.y -= snake_width
    elif direction == "down":
        sensor.y += snake_width
    return sensor.colliderect(thing_to_detect)
def die(snake_list, snake_width):
    global running
    snake_head = snake_list[-1]
    body_length = len(snake_list) - snake_width - 1
    snake_body = snake_list[:body_length]
    snake_skull = snake_head[2]
    for node in snake_body:
        if node[2].colliderect(snake_skull):
            print(snake_body.index(node))
            running = False
def increase_growth(score): # Make the snake grow more the more food it eats
    global growth
    if score > 10:
        growth += step

# Fruit Variables
fruits = []
max_fruits = 1
# Fruit functions
def get_fruit_pos(fruit_width, snake, screen_w=600, screen_h=600):
    # Gets random position outside of Snake bounding box to spawn a fruit
    while True: # Keep pickng a new position until we find one that isn't on the snake's body
        screen_w_limit = screen_w - fruit_width
        screen_h_limit = screen_h - fruit_width
        fruit_x = random.randrange(0, screen_w_limit, fruit_width + fruit_width)
        fruit_y = random.randrange(0, screen_h_limit, fruit_width + fruit_width)
        # Make a pygame RECT for a collision box
        fruit_rect = pygame.Rect(fruit_x, fruit_y, fruit_width, fruit_width)
        fruit = [fruit_x, fruit_y, fruit_rect]
        fruit_on_snake = False
        for node in snake:
            if fruit_rect.colliderect(node[2]):
                fruit_on_snake = True
                # Skip spawning a fruit in the frame that this function was called in
        if fruit_on_snake == False:
            return fruit
def draw_fruit(screen, fruit_list, width):
    for fruit in fruit_list:
        fruit_pos = fruit
        pygame.draw.rect(screen, red, (fruit_pos[0], fruit_pos[1], width, width), border_radius=8)
# Warp Wall
def check_warp(snake_list, direction, snake_width, screen_w, screen_h):
    snake_head = snake_list[-1]
    if direction == "left" and snake_head[0] < 0:
        new_x = screen_w
        new_y = snake_head[1]
        collision_box = pygame.Rect(new_x, new_y, snake_width, snake_width)
        snake_list.append([new_x, new_y, collision_box])
    elif direction == "right" and snake_head[0] > screen_w:
        new_x = 0 # If width of the snake is 10, then place the new snake node the width of that snake node away...
        # ... from the opposite screen edge
        new_y = snake_head[1]
        collision_box = pygame.Rect(new_x, new_y, snake_width, snake_width)
        snake_list.append([new_x, new_y, collision_box])
    elif direction == "up" and snake_head[1] < 0:
        new_x = snake_head[0]
        new_y = screen_h
        collision_box = pygame.Rect(new_x, new_y, snake_width, snake_width)
        snake_list.append([new_x, new_y, collision_box])
    elif direction == "down" and snake_head[1] > screen_h: # If the snake is going down and is ...
        # ...almost touching the bottom edge
        new_x = snake_head[0]
        new_y = 0
        collision_box = pygame.Rect(new_x, new_y, snake_width, snake_width)
        snake_list.append([new_x, new_y, collision_box])
    return snake_list

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake_direction != "right":
                snake_direction = "left"
            elif event.key == pygame.K_RIGHT and snake_direction != "left":
                snake_direction = "right"
            elif event.key == pygame.K_UP and snake_direction != "down":
                snake_direction = "up"
            elif event.key == pygame.K_DOWN and snake_direction != "up":
                snake_direction = "down"
    screen.fill(black)
    # Snake Code
    new_head = add_node(snake, snake_direction, step, width)
    snake.append(new_head)
    draw(screen, snake, width)
    remove_node(snake, snake_length)
    die(snake, width)
    # Check for Snake Collisions
    # Chance to spawn a fruit every frame
    chance = random.randint(0,100)
    if chance >= 90 and (len(fruits) < max_fruits):
        new_fruit = get_fruit_pos(width, snake)
        fruits.append(new_fruit)
    if len(fruits) > 0:
        draw_fruit(screen, fruits, width)
        # Detect for snake eating food, and if so--increase the max_snake_length by snake_width and score by 1.
        for each_fruit in fruits:
            fruit_collision = each_fruit[2]
            fruit_in_front = detect(fruit_collision, snake, snake_direction, width) # Detect if each_fruit's position in front
            if fruit_in_front:
                snake_length += growth
                score += 1
                fruits.remove(each_fruit)
                increase_growth(score)
                print(score)
    # If the snake bumps a wall
    check_warp(snake, snake_direction, width, 600, 600)
    # Game Frame Settings...
    pygame.display.flip()
    clock.tick(60)
pygame.quit()