#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
print("%s created on %s by %s (%d)\n%s\n" % ("main.py", "7/04/15", __author__, 15062061, "-----" * 15))

import pygame
import os

import gameObject as gameObject
import player as player
import inputHandler as inp
import constants as const
import enemies as enemies
import barrier as barrier


def make_barrier(barrier_start):
    #TOP
    instance_list.instantiate(barrier.Barrier(True, False, False, barrier_start[0], barrier_start[1]))
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0]+barrier.Barrier.width, barrier_start[1]))
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0]+barrier.Barrier.width*2, barrier_start[1]))
    instance_list.instantiate(barrier.Barrier(True, True, False, barrier_start[0]+barrier.Barrier.width*3, barrier_start[1]))
    #MID
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0], barrier_start[1]+barrier.Barrier.height))
    instance_list.instantiate(barrier.Barrier(True, True, True, barrier_start[0]+barrier.Barrier.width, barrier_start[1]+barrier.Barrier.height))
    instance_list.instantiate(barrier.Barrier(True, False, True, barrier_start[0]+barrier.Barrier.width*2, barrier_start[1]+barrier.Barrier.height))
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0]+barrier.Barrier.width*3, barrier_start[1]+barrier.Barrier.height))
    #BOT
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0], barrier_start[1]+barrier.Barrier.height*2))
    instance_list.instantiate(barrier.Barrier(False, False, False, barrier_start[0]+barrier.Barrier.width*3, barrier_start[1]+barrier.Barrier.height*2))

pygame.init()

# Select the font to use, size, bold, italics
gameFont = pygame.font.SysFont('tlwgtypewriter', 25, False, False)

# Set the width, height and position of the screen
size = (const.WINDOW_WIDTH, const.WINDOW_HEIGHT)
screenInfo = pygame.display.Info()

# centre window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screenInfo.current_w/2 - size[0]/2, screenInfo.current_h/2 - size[1]/2)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Space Invaders!")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Input handler
input_handler = inp.InputHandler()

# Instance handling
instance_list = gameObject.InstanceList(input_handler, clock, gameFont)

instance_list.instantiate(player.Player(size[0]/2, size[1] - 50))
instance_list.instantiate(enemies.EnemyGroup(150, 700))

for i in range(3):
    make_barrier((size[0]/5 + i*((size[0]-size[0]/5)/3), size[1] - 300))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:   # If user clicked close
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            done = True
    input_handler.handle_input(events)

    # --- Game logic --- #
    instance_list.logic()

    # First, clear the screen to black
    # --- Drawing code --- #
    screen.fill(const.BLACK)

    instance_list.render(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()