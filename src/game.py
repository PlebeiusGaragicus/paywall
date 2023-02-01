import pygame

# Initialize game engine
pygame.init()
background = pygame.image.load("./assets/bg1.jpg")

# Set screen dimensions
screen_width = background.get_width()
screen_height = background.get_height()
screen = pygame.display.set_mode([screen_width, screen_height])

# Load background image

# Load player image
player_image = pygame.image.load("./assets/char2.png")

# make character smaller
player_image = pygame.transform.scale(player_image, (int(player_image.get_width()/2), int(player_image.get_height()/2)))

# Set player position
player_x = screen_width/2 - player_image.get_width()/2
player_y = screen_height - player_image.get_height()

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

    # Draw background
    screen.blit(background, [0, 0])

    # Draw player
    screen.blit(player_image, [player_x, player_y])

    # Update screen
    pygame.display.update()

# Quit game engine
pygame.quit()
