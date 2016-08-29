#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("input.py", "9/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

import pygame


class InputHandler:
    move_left = False
    move_right = False
    shoot = False

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.move_left = True
                elif event.key == pygame.K_d:
                    self.move_right = True
                elif event.key == pygame.K_SPACE:
                    self.shoot = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.move_left = False
                elif event.key == pygame.K_d:
                    self.move_right = False
                elif event.key == pygame.K_SPACE:
                    self.shoot = False

    def __str__(self):
        return "Left: %s, Right: %s, Shoot: %s" % (self.move_left, self.move_right, self.shoot)
