import pygame as pg


class Bread:
    def __init__(self, sprite='resources/HappyBread.png', ):
        self.sprite = pg.image.load(sprite)
        self.rotated = self.sprite
        self.surface = self.sprite.get_rect()  # this is used for centering the image surface
        self.rotation = 0

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        # need to add centered and re-centered x,y
