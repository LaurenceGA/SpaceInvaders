#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("barrier.py", "13/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

from gameObject import Object
from spriteSheet import SpriteSheet

import pygame


class Barrier(Object):
    width = 32
    height = 32
    frames = 4

    sprites = []
    sprite_sheet = SpriteSheet("resources/barrier.png")
    sprite_width = 16
    sprite_height = 16
    image_index = 0

    def __init__(self, diagonal, x_inv, y_inv, x=0, y=0,):
        super().__init__(x, y)
        img = []
        for i in range(self.frames):
            image = self.sprite_sheet.get_image(self.sprite_width*i, self.sprite_height*diagonal, self.sprite_width, self.sprite_height)
            image = pygame.transform.scale(image, (self.width, self.height))
            image = pygame.transform.flip(image, x_inv, y_inv)
            img.append(image)

        self.sprites = img
        self.image = self.sprites[self.image_index]

    def draw(self, screen):
        screen.blit(self.image, [self.x - self.width/2, self.y - self.height/2])

    def damage(self):
        self.image_index += 1
        if self.image_index > len(self.sprites)-1:
            self.destroy()
        else:
            self.image = self.sprites[self.image_index]