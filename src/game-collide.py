# Load obstacle image
obstacle_image = pygame.image.load("obstacle.png")

# Set obstacle position
obstacle_x = screen_width/2 - obstacle_image.get_width()/2
obstacle_y = screen_height - obstacle_image.get_height() - player_image.get_height()

# Create rects for collision detection
player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())
obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_image.get_width(), obstacle_image.get_height())

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
        player_jump_speed -= 1
        if player_jump_speed < 0:
            player_jumping = False
            player_jump_speed = 20
    else:
        player_y = screen_height - player_image.get_height()

    # Check for collision with obstacle
    player_rect.x = player_x
    player_rect.y = player_y
    if player_rect.colliderect(obstacle_rect):
        player_y = obstacle_y - player_image.get_height()

    # Draw background
    screen.blit(background, [0, 0])

    # Draw obstacle
    screen.blit(obstacle_image, [obstacle_x, obstacle_y])

    # Draw player
    screen.blit(player_image, [player_x, player_y])

    # Update screen
    pygame.display.update()

# Quit game engine
pygame.quit()