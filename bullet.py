#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("bullet.py", "10/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

from gameObject import Object
from constants import *
import enemies as enemies
import player
from spriteSheet import SpriteSheet
from barrier import Barrier

import pygame


class Bullet(Object):
    move_speed = 20
    width = 5
    height = 20

    def __init__(self, x=0, y=0, y_speed=-10):
        super().__init__(x, y)
        self.y_speed = y_speed

    def step(self):
        super().step()

        if self.y < 0:
            self.destroy()

        # Collision
        for inst in self.instance_handler.instances:
            if type(inst) is Barrier:
                if abs((self.x - inst.x) / inst.width) < 0.5 and abs((self.y - inst.y) / inst.height) < 1:
                    inst.damage()
                    self.destroy()
            if self.target_collide(inst):
                break

    def target_collide(self, inst):
        if issubclass(type(inst), enemies.Enemy):
                if abs((self.x - inst.x) / inst.width) < 0.5 and abs((self.y - inst.y) / inst.height) < 1:
                    self.instance_handler.instantiate(Explosion(inst.x, inst.y, inst.width, inst.height))
                    self.instance_handler.find_first_of_type(player.Player).add_score(inst.value)

                    inst.destroy()
                    self.destroy()
                    return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, [self.x - self.width/2, self.y - self.height/2, self.width, self.height], 0)


class EnemyBullet(Bullet):
    def target_collide(self, inst):
        if type(inst) is player.Player:
            if abs((self.x - inst.x) / inst.width) < 0.5 and abs((self.y - inst.y) / inst.height) < 1:
                inst.die()

                self.destroy()


class Explosion(Object):
    img_width = 32
    img_height = 32
    frames = 4
    image_speed = 50
    image_timer = 0

    sprite_sheet = SpriteSheet("resources/explode.png")

    image_index = 0

    def __init__(self, x=0, y=0, width=32, height=32):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.image_timer = self.image_speed
        img = []

        for i in range(self.frames):
            image = self.sprite_sheet.get_image(self.img_width*i, 0, self.img_width, self.img_height)
            image = pygame.transform.scale(image, (width, height))
            img.append(image)

        self.animation = img
        self.image = self.animation[self.image_index]

    def step(self):
        self.image_timer -= self.clock.get_time()
        if self.image_timer <= 0:
            self.image_index += 1
            if self.image_index > len(self.animation)-1:
                self.destroy()
            else:
                self.image = self.animation[self.image_index]
            self.image_timer = self.image_speed

    def draw(self, screen):
        screen.blit(self.image, [self.x - self.width/2, self.y - self.height/2])