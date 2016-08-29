#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("spriteSheet.py", "10/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

import pygame
import constants as const


class SpriteSheet():
    """Class to grab images from a sprite sheet"""
    sprite_sheet = None

    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename)

    def get_image(self, x, y, width, height):
        # Create a new blank image
        image = pygame.Surface([width, height])

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        image.set_colorkey(const.BLACK)

        return image