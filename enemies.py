#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("enemies.py", "10/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")

from gameObject import Object
from constants import *
import bullet
import player
from spriteSheet import SpriteSheet

import pygame

import random


class EnemyGroup(Object):
    enemies = []
    width = 11
    rows_of_large = 2
    rows_of_medium = 2
    rows_of_small = 1
    enemy_width = 64
    enemy_height = 64

    padding = 16
    x_begin = WINDOW_WIDTH/2 - enemy_width*(width//2) - (width//2)*padding
    y_change = 0

    move_distance = 16
    move_timer = 0

    ufo_timer = random.randint(15, 30) * 1000

    def __init__(self, y_begin, time_to_move):
        self.y_begin = y_begin
        self.time_to_move = time_to_move
        self.move_timer = time_to_move

    def awake(self):
        for j in range(self.rows_of_small):
            a = j
            for i in range(self.width):
                en = self.instance_handler.instantiate(SmallAlien(self, self.x_begin + i*self.enemy_width + i*self.padding, self.y_begin + a*self.enemy_height + a*self.padding))
                self.enemies.append(en)

        for k in range(self.rows_of_medium):
            a = k + self.rows_of_small
            for i in range(self.width):
                en = self.instance_handler.instantiate(MediumAlien(self, self.x_begin + i*self.enemy_width + i*self.padding, self.y_begin + a*self.enemy_height + a*self.padding))
                self.enemies.append(en)

        for l in range(self.rows_of_large):
            a = l + self.rows_of_small + self.rows_of_medium
            for i in range(self.width):
                en = self.instance_handler.instantiate(LargeAlien(self, self.x_begin + i*self.enemy_width + i*self.padding, self.y_begin + a*self.enemy_height + a*self.padding))
                self.enemies.append(en)

    def step(self):
        self.move_timer -= self.clock.get_time()
        self.ufo_timer -= self.clock.get_time()

        if self.ufo_timer <= 0:
            if self.instance_handler.find_first_of_type(UFO) is None:
                side = random.choice([-UFO.width, WINDOW_WIDTH])
                obj = self.instance_handler.instantiate(UFO(self, side, UFO.height*2))
                obj.x_speed = 2 if side <= 0 else -2
            self.ufo_timer = random.randint(15, 30) * 1000

        if self.move_timer <= 0:
            self.move()
            self.move_timer = self.time_to_move

    def move(self):
        dx = self.move_distance
        dy = 0
        for enemy in self.enemies:
            if enemy.x - enemy.width/2 + self.move_distance < 0 or enemy.x + enemy.width/2 + self.move_distance > WINDOW_WIDTH:
                self.move_distance *= -1

                dy = self.enemy_height/2
                dx = 0
                self.y_change = dy

                #self.time_to_move -= 100
                self.time_to_move *= 0.9
                if self.time_to_move <= 0:
                    self.time_to_move = 0
        for enemy in self.enemies:
            enemy.jump(dx, dy)
            enemy.animate()


class Enemy(Object):
    width = 48
    height = 48
    frames = 2

    animation = []
    sprite_sheet = SpriteSheet("resources/Aliens.png")
    sprite_origin = (0, 0)
    sprite_dimensions = (1, 1)
    image_index = 0

    def __init__(self, parent_list, x=0, y=0):
        super().__init__(x, y)
        self.shoot_timer = random.randint(3, 10) * 1000
        self.parent_list = parent_list
        #x_scale = round(self.height / self.sprite_dimensions[1]) * self.sprite_dimensions[0]
        x_scale = self.width

        img = []
        for i in range(self.frames):
            image = self.sprite_sheet.get_image(self.sprite_origin[0] + self.sprite_dimensions[0]*i, self.sprite_origin[1], self.sprite_dimensions[0], self.sprite_dimensions[1])
            image = pygame.transform.scale(image, (x_scale, self.height))
            img.append(image)

        #self.width = x_scale

        self.animation = img
        self.image = self.animation[self.image_index]

    def step(self):
        super().step()
        self.shoot_timer -= self.clock.get_time()

        if self.shoot_timer <= 0:
            self.shoot(random.choice([True, False]))
            self.shoot_timer = random.randint(3, 5) * 1000

    def shoot(self, fire):
        if fire:
            for enm in self.parent_list.enemies:
                if enm.x == self.x:
                    if enm.y > self.y:
                        break
            else:
                self.instance_handler.instantiate(bullet.EnemyBullet(self.x, self.y, 5))

    def jump(self, dx, dy):
        self.x += dx
        self.y += dy
        self.check_win()

    def check_win(self):
        if self.y > WINDOW_HEIGHT-WIN_HEIGHT:
            print("GAME OVER MAN, GAME OVER!")
            quit()

    def animate(self):
        self.image_index += 1
        self.image = self.animation[self.image_index % 2]

    def draw(self, screen):
        screen.blit(self.image, [self.x - self.width/2, self.y - self.height/2])

    def destroy(self):
        for enem in self.parent_list.enemies:
            if enem == self:
                del self.parent_list.enemies[self.parent_list.enemies.index(enem)]
        if len(self.parent_list.enemies) == 0:
            self.instance_handler.remove_of_type(bullet.Bullet)
            self.parent_list.destroy()
            self.instance_handler.instantiate(EnemyGroup(self.parent_list.y_begin + self.parent_list.y_change, self.parent_list.time_to_move*1.2))
            for inst in self.instance_handler.instances:
                if type(inst) is player.Player:
                    inst.lives += 1
                    break

        super().destroy()


class SmallAlien(Enemy):
    value = 40
    sprite_origin = (0, 0)
    sprite_dimensions = (8, 8)


class MediumAlien(Enemy):
    value = 20
    sprite_origin = (0, 8)
    sprite_dimensions = (11, 8)


class LargeAlien(Enemy):
    value = 10
    sprite_origin = (0, 16)
    sprite_dimensions = (12, 8)


class UFO(Enemy):
    width = 80
    height = 40
    frames = 1

    value = random.choice([50, 100, 150])
    sprite_origin = (0, 24)
    sprite_dimensions = (16, 7)

    def step(self):
        super().step()
        if self.x < -UFO.width * 2 or self.x > WINDOW_WIDTH + UFO.width * 2:
            self.destroy()

    def shoot(self, fire):
        pass