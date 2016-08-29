#!/usr/bin/env python
__author__ = 'Laurence Armstrong'
authorship_string = "%s created on %s by %s (%d)\n%s\n" % \
                    ("gameObject.py", "9/04/15", __author__, 15062061, "-----" * 15) \
    if __name__ == '__main__' else ""
print(authorship_string, end="")


class InstanceList:
    def __init__(self, inp_handle, clock, font):
        self.instances = []
        self.input_handler = inp_handle
        self.clock = clock
        self.font = font

    def logic(self):
        for instance in self.instances:
            instance.step()

    def render(self, screen):
        for instance in self.instances:
            instance.draw(screen)

    def instantiate(self, obj):
        obj.instance_handler = self
        obj.input_handler = self.input_handler
        obj.clock = self.clock
        self.instances.append(obj)
        obj.awake()
        return obj

    def remove(self, inst):
        for instance in self.instances:
            if instance == inst:
                del self.instances[self.instances.index(instance)]

    def find_of_type(self, typ):
        insts_of_type = []
        for instance in self.instances:
            if instance is typ or issubclass(type(instance), typ):
                insts_of_type.append(instance)
        return insts_of_type

    def find_first_of_type(self, typ):
        for instance in self.instances:
            if instance is typ or issubclass(type(instance), typ):
                return instance
        return None

    def remove_of_type(self, typ):
        insts = self.find_of_type(typ)
        for inst in insts:
            inst.destroy()

    def __str__(self):
        string = ""
        for instance in self.instances:
            string += str(instance) + ", "
        return string


class Object:
    """
    @type instance_handler: InstanceList
    @type input_handler: spaceInvaders.inputHander.InputHandler
    @type clock: pygame.time.Clock
    """
    x_speed = 0
    y_speed = 0
    input_handler = None
    instance_handler = None
    clock = None

    def __init__(self, x=0, y=0, ):
        self.x = x
        self.y = y

    def awake(self):
        pass

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

    def step(self):
        self.move()

    def draw(self, screen):
        pass

    def destroy(self):
        self.instance_handler.remove(self)