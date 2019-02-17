# import pygame as pg  # not needed because it is imported in Toast.py

from Toast import *


# color definition triplets
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
violet = (128, 0, 128)


def quit_app():
    pg.quit()
    quit()


class Interface:

    def __init__(self):
        pg.init()

        self.display_width = 1100
        self.display_height = 600

        self.game_display = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption('Yeah Toast!')

        self.clock = pg.time.Clock()

        # self.x_current = display_width/3
        self.screen_surf = pg.display.get_surface()
        self.x_current = self.screen_surf.get_rect().centerx
        self.y_current = self.screen_surf.get_rect().centery

        self.HappyBread = Item(sprite='resources/HappyBread.png',
                               coordinates=(self.x_current, self.y_current))

    def mainloop(self):

        closed = False

        while not closed:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    closed = True

            self.translate_control(self.HappyBread)
            # should add acceleration next
            # should add bouncing off of objects/walls
            # collision detection

            self.game_display.fill(white)
            self.show_bread(self.HappyBread.rect)

            pg.display.update()
            self.clock.tick(48)

    def show_bread(self, surface):
        self.game_display.blit(self.HappyBread.rotated, surface)

    def translate_control(self, item, translation_sensitivity=9, rotation_sensitivity=6):
        # these controls give the bread (or any item) up/down and tumble left/right motion
        ground_axis = self.display_height - item.sprite.get_rect().height / 2
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            item.translate(0, -translation_sensitivity)
        if key[pg.K_LEFT]:
            item.rotate(rotation_sensitivity)
            item.translate(-translation_sensitivity, 0)
        if key[pg.K_RIGHT]:
            item.rotate(-rotation_sensitivity)
            item.translate(translation_sensitivity, 0)
        if key[pg.K_DOWN]:
            if item.center[1] < ground_axis:
                item.translate(0, translation_sensitivity)


if __name__ == "__main__":

    a = Interface()
    a.mainloop()
    quit_app()
