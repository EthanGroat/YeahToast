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
