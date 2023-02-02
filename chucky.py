import random
import time
import pygame


# Initialize game engine
pygame.init()

# Load background image
background = pygame.image.load("./assets/bg1.jpg")

# Set screen dimensions
screen_width = background.get_width()
screen_height = background.get_height()
screen = pygame.display.set_mode([screen_width, screen_height])

# Load object image
object_image = pygame.image.load("./assets/knife1.png")

# resize object width to 25 pixels and keep aspect ratio
object_image = pygame.transform.scale(object_image, (60, int(object_image.get_height() * 60 / object_image.get_width())))

# rotate object 45 degrees counterclockwise
object_image = pygame.transform.rotate(object_image, -45)

# Set initial object position
object_x = random.randint(0, screen_width - object_image.get_width())
object_y = 0

# Create the font object
font = pygame.font.SysFont("Arial", 40, bold=True)

# Set initial speed
object_speed = 0.5

# Create rect for collision detection
object_rect = pygame.Rect(object_x, object_y, object_image.get_width(), object_image.get_height())

# Set initial score
score = 5

# Load player image
player_image = pygame.image.load("./assets/chuckchar.png")

# make character smaller
# player_image = pygame.transform.scale(player_image, (int(player_image.get_width()/2), int(player_image.get_height()/2)))

# Set player position
player_x = screen_width/2 - player_image.get_width()/2
player_y = screen_height - player_image.get_height()

# Create rects for collision detection
player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())

# Set player speed
player_speed = 2

# Set player jump speed
player_jump_speed = 2

# Set player jump state
player_jumping = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if score == 0:
        running = False
    
    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and not player_jumping:
        player_jumping = True

    # Update player position
    if player_jumping:
        player_y -= player_jump_speed
        player_jump_speed -= 0.005
        # if player_jump_speed < 0:
        if player_y > screen_height - player_image.get_height():
            player_jumping = False
            player_jump_speed = 2
    else:
        player_y = screen_height - player_image.get_height()

    # wrap player around screen
    if player_x < 0:
        player_x = screen_width
    if player_x > screen_width:
        player_x = 0

    player_rect.x = player_x
    player_rect.y = player_y

    # Check for collision with obstacle
    player_rect.x = player_x
    player_rect.y = player_y
    # if player_rect.colliderect(obstacle_rect):
    #     player_y = obstacle_y - player_image.get_height()

    # Update object position
    object_y += object_speed
    object_rect.x = object_x
    object_rect.y = object_y

    # Check for collision with player
    if player_rect.colliderect(object_rect):
        score -= 1
        object_x = random.randint(0, screen_width - object_image.get_width())
        object_y = 0

    if object_y > screen_height:
        object_y = 0
        object_x = random.randint(0, screen_width - object_image.get_width())

    # Draw background
    screen.blit(background, [0, 0])

    # Draw object
    screen.blit(object_image, [object_x, object_y])

    # Draw player
    screen.blit(player_image, [player_x, player_y])

    # Render the text surface with the score value
    text_surface = font.render("Score: {}".format(score), True, (255, 255, 0), (0, 0, 0))

    # Get the dimensions of the text surface
    text_width, text_height = text_surface.get_size()

    # Define the position to display the text
    text_x = screen_width - text_width - 10
    text_y = 10

    # Draw the text surface on the screen
    screen.blit(text_surface, (text_x, text_y))

    # Update screen
    pygame.display.update()

chuck = pygame.image.load("./assets/chuckdagger.png")

# resize chuck to fit on screen
chuck = pygame.transform.scale(chuck, (screen_width, screen_height))

# screen.fill((0, 0, 0))
screen.blit(chuck, [0, 0])

text_surface = font.render("yOu KiLLeD ChUcKy !!!".format(score), True, (255, 200, 150), (0, 0, 0))

# Get the dimensions of the text surface
text_width, text_height = text_surface.get_size()

# Define the position to display the text
text_x = screen_width/2 - text_width/2
text_y = screen_height/2 - text_height/2

# Draw the text surface on the screen
screen.blit(text_surface, (text_x, text_y))

pygame.display.update()

time.sleep(5)

# Quit game engine
pygame.quit()
