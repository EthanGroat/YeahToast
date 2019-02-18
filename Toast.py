import pygame as pg
import math


class Item:
    def __init__(self, sprite, coordinates):
        self.center = list(coordinates)  # internal coordinates used to remap surface, takes floats
        self.rotation = 0.0  # in degrees
        self.sprite = pg.image.load(sprite)
        self.rotated = self.sprite
        self.rect = self.rotated.get_rect(center=coordinates)
        # this is a rectangle used as a proxy for re-centering and blitting the sprite to the right location

    def translate(self, x=0.0, y=0.0, phi=0.0):  # used for both rotation and translation
        # defaults to zero for interoperability in updating Items
        self.rect.centerx += x
        self.rect.centery += y
        self.center = self.rect.center
        self.rotate(phi)

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        self.rect = self.rotated.get_rect(center=self.center)  # working! :D


class AcceleratingItem(Item):
    def __init__(self, sprite, coordinates, velocity=(0.0, 0.0), womega=0.0):
        self.velocity = list(velocity)  # lists are mutable, tuples aren't
        self.omega = womega
        super().__init__(sprite, coordinates)

    def translate(self, x=0.0, y=0.0, phi=0.0):  # updates position incrementally - serves as the update() function
        self.center[0] += x + self.velocity[0]  # center tracks exact floating point positions
        self.center[1] += y + self.velocity[1]
        self.rect.center = tuple(self.center)  # this assignment updates the pygame sprite placement coordinates
        self.rotate(phi + self.omega)  # exact degrees

    def accelerate(self, x_acceleration=0.0, y_acceleration=0.0, angular_acceleration=0.0):
        self.velocity[0] += x_acceleration
        self.velocity[1] += y_acceleration
        self.omega += angular_acceleration

    def accelerate_forward(self, acceleration=0.0):
        x_comp = -acceleration * math.sin(math.radians(self.rotation))  # sine takes radians, not degrees!
        y_comp = -acceleration * math.cos(math.radians(self.rotation))
        self.accelerate(x_comp, y_comp)

    def update(self, x_acc=0.0, y_acc=0.0, angular_acc=0.0):
        # this function is not really needed but here anyway to further generalize the update idea
        # and encapsulate every normal incremental thing that AcceleratingItems do.
        self.accelerate(x_acc, y_acc, angular_acc)
        self.translate()

    def reset_velocity(self, velocity=(0.0, 0.0)):
        self.velocity[0], self.velocity[1] = velocity[0], velocity[1]

    def smooth_translate(self, x, y):
        pass

    def smooth_rotate(self, degrees):
        pass


# class GravitationallyAffectedItem(AcceleratingItem):
