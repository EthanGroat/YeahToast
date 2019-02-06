import pygame as pg


class Bread:
    def __init__(self, sprite='resources/HappyBread.png', coordinates=(100, 100)):
        self.sprite = pg.image.load(sprite)
        self.rotated = self.sprite
        self.surface = self.sprite.get_rect(center=coordinates)  # this is used for re-centering the image surface
        self.rotation = 0

    def translate(self, x, y):
        self.surface.centerx += x
        self.surface.centery += y

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        # need to add centered and re-centered x,y
