import pygame
import random

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()

# Set the display window size
win_width = 800
win_height = 600

# Create the window
win = pygame.display.set_mode((win_width, win_height))

# Set the title of the window
pygame.display.set_caption("Pong")

# Load the ball image
ball = pygame.image.load("./assets/pong.png")

# Scale the ball image to a smaller size
ball = pygame.transform.scale(ball, (20, 20))

# Initialize ball position and velocity
ball_x = win_width//2 - 10
ball_y = win_height//2 - 10
ball_velocity = [random.uniform(2, 5), random.uniform(-5, 5)]

# Load the paddle image
paddle = pygame.image.load("./assets/paddle.png")

# Scale the paddle image
paddle = pygame.transform.scale(paddle, (20, 100))

# Initialize paddle position and velocity
paddle_x = win_width - 20
paddle_y = win_height//2 - 50
paddle_velocity = 0

# Run the game loop
running = True
while running:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update paddle position based on velocity
    paddle_y += paddle_velocity
    
    # Keep paddle within the window
    if paddle_y < 0:
        paddle_y = 0
    elif paddle_y > win_height - 100:
        paddle_y = win_height - 100
    
    # Update ball position based on velocity
    ball_x += ball_velocity[0]
    ball_y += ball_velocity[1]
    
    # Check for ball collision with paddle
    if ball_x >= win_width - 20 and ball_y >= paddle_y and ball_y <= paddle_y + 100:
        ball_velocity[0] = -ball_velocity[0]
    
    # Check for ball collision with top and bottom of the window
    if ball_y <= 0 or ball_y >= win_height - 20:
        ball_velocity[1] = -ball_velocity[1]
    
    # Check for ball going out of the window from left
    if ball_x <= 0:
        # running = False
        ball_velocity[0] = -ball_velocity[0]
    
    # Check for ball going out of the window from right
    if ball_x >= win_width:
        running = False
        # ball_velocity[0] = -ball_velocity[0]

    # Clear the window
    win.fill((255, 255, 255))
    
    # Draw the ball and paddle
    win.blit(ball, (ball_x, ball_y))
    win.blit(paddle, (paddle_x, paddle_y))
    
    # Update the display
    pygame.display.update()
    
    # Handle keyboard events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle_velocity = -5
    elif keys[pygame.K_DOWN]:
        paddle_velocity = 5
    else:
        paddle_velocity = 0
    

# Quit Py
