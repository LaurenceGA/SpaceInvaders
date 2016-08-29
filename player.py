#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("player.py", "9/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

from gameObject import Object
from constants import *
from bullet import Bullet

import pygame


class Player(Object):
    score = 0

    alive = True
    lives = 3
    death_time = 2000
    death_timer = 0

    move_speed = 7
    base = [100, 20]
    base_indent = [5, 5]
    cannon = [25, 30]
    cannon_tip = [5, 15]

    # For collision
    width = base[0]
    height = base[1] + base_indent[1]

    can_shoot = True
    attack_time = 700
    shoot_timer = 0

    def draw(self, screen):
        s = self
        # Base
        pygame.draw.rect(screen, GREEN, [s.x - s.base[0]/2, s.y - s.base[1]/2, s.base[0], s.base[1]], 0)
        # Base indent
        pygame.draw.rect(screen, GREEN, [s.x - s.base[0]/2 + s.base_indent[0], s.y - s.base[1]/2 - s.base_indent[1], s.base[0] - s.base_indent[0]*2, s.base[1]], 0)
        if self.alive:
            # Cannon
            pygame.draw.rect(screen, GREEN, [s.x - s.cannon[0]/2, s.y - s.base[1]/2 - s.base_indent[1] - s.cannon[1], s.cannon[0], s.cannon[1]], 0)
            # tip
            pygame.draw.rect(screen, GREEN, [s.x - s.cannon_tip[0]/2, s.y - s.base[1]/2 - s.base_indent[1] - s.cannon[1] - s.cannon_tip[1], s.cannon_tip[0], s.cannon_tip[1]], 0)

        pygame.draw.line(screen, GREEN, [0, WINDOW_HEIGHT-20], [WINDOW_WIDTH, WINDOW_HEIGHT-20], 3)

        # Draw the score
        # Render the text. "True" means anti-aliased text.
        text = self.instance_handler.font.render("Score: %d     Lives: %d" % (self.score, self.lives), True, WHITE)

        # Put the image of the text on the screen
        screen.blit(text, [20, 20])

    def shoot(self):
        self.instance_handler.instantiate(Bullet(self.x + self.x_speed, self.y - self.base[1]/2 - self.cannon[1] - self.cannon_tip[1]))
        self.can_shoot = False
        self.shoot_timer = self.attack_time

    def add_score(self, value):
        self.score += value

    def die(self):
        if self.alive:
            self.alive = False
            self.lives -= 1
            self.death_timer = self.death_time

    def step(self):
        if not self.can_shoot:
            self.shoot_timer -= self.clock.get_time()

        if not self.alive:
            self.death_timer -= self.clock.get_time()
            if self.lives == 0:
                print("GAME OVER")
                quit()

        if self.shoot_timer <= 0 and not self.input_handler.shoot:
            self.can_shoot = True

        if self.death_timer <= 0:
            self.alive = True
            self.death_timer = -1

        if self.input_handler.move_left and not self.input_handler.move_right and self.alive:
            self.x_speed = -self.move_speed
        elif self.input_handler.move_right and not self.input_handler.move_left and self.alive:
            self.x_speed = self.move_speed
        else:
            self.x_speed = 0

        self.move()

        if self.x + self.base[0]/2 > WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.base[0]/2
        if self.x - self.base[0]/2 < 0:
            self.x = self.base[0]/2

        if self.input_handler.shoot and self.can_shoot and self.alive:
            self.shoot()