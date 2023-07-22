import pygame, sys

# initialize pygame
pygame.init()

# set up the window
WINDOW = pygame.display.set_mode((400, 300))

# colors
WHITE = (127, 255, 212)
RED = (0, 255, 0)

# ball position and size
ball_x = 200
ball_y = 150
ball_radius = 20
ball_vel_x = 0.1
ball_vel_y = 0.1

# player position and size
player_x = 200
player_y = 280
player_width = 70
player_height = 20
player_vel = 0.1

# game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if player_x > 0 and player_x + player_width < 400:
        if keys[pygame.K_LEFT]:
            player_x -= player_vel
            if player_x < 0:
                player_x += 10
        if keys[pygame.K_RIGHT]:
            player_x += player_vel
            if player_x + player_width > 400:
                player_x -= 10

    # update ball position
    ball_x += ball_vel_x
    ball_y += ball_vel_y

    # bounce the ball if it hits a wall
    if ball_x > 400 - ball_radius or ball_x < 0 + ball_radius:
        ball_vel_x = -ball_vel_x
    if ball_y > 300 - ball_radius or ball_y < 0 + ball_radius:
        ball_vel_y = -ball_vel_y

    # check for collision with player
    if player_x + player_width >= ball_x - ball_radius and player_x < ball_x + ball_radius:
        if player_y + player_height >= ball_y - ball_radius and player_y < ball_y + ball_radius:
            # Ballen skal sprette tilbake
            ball_vel_y = -ball_vel_y
    
    # check if ball hits the floor
    if ball_y > 300 - ball_radius:
        run = False

    # update window color
    WINDOW.fill((100, 149, 237))

    # draw the ball
    pygame.draw.circle(WINDOW, WHITE, (int(ball_x), int(ball_y)), ball_radius)

    # draw the player
    pygame.draw.rect(WINDOW, RED, [player_x, player_y, player_width, player_height])

    # update the display
    pygame.display.update()

pygame.quit()