import pygame as pg


class Item:
    def __init__(self, sprite, coordinates):
        self.center = coordinates  # internal coordinates used to remap surface (might not be needed)
        self.rotation = 0  # in degrees
        self.sprite = pg.image.load(sprite)
        self.rotated = self.sprite
        self.rect = self.rotated.get_rect(center=coordinates)
        # this is a rectangle used as a proxy for re-centering and blitting the sprite to the right location

    def translate(self, x, y):
        self.rect.centerx += x
        self.rect.centery += y
        self.center = self.rect.center

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        self.rect = self.rotated.get_rect(center=self.center)  # working! :D


class AcceleratingItem(Item):
    def __init__(self, sprite, coordinates, velocity=(0, 0), womega=0):
        self.velocity = velocity
        self.omega = womega
        super().__init__(sprite, coordinates)

    def translate(self, x=0, y=0):
        self.rect.centerx += x + self.velocity[0]
        self.rect.centery += y + self.velocity[1]
        self.center = self.rect.center

    def accelerate(self, x_acceleration, y_acceleration, angular_acceleration):
        self.velocity[0] += x_acceleration
        self.velocity[1] += y_acceleration
        self.omega += angular_acceleration

    def smooth_translate(self, x, y):
        pass

    def smooth_rotate(self, degrees):
        pass


# class GravitationallyAffectedItem(AcceleratingItem):
