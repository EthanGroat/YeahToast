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

        self.screen_surf = pg.display.get_surface()
        self.x_mid = self.screen_surf.get_rect().centerx
        self.y_mid = self.screen_surf.get_rect().centery

        self.HappyBread = AcceleratingItem(sprite='resources/HappyBread.png',
                                           coordinates=(float(self.x_mid), float(self.y_mid)))

    def mainloop(self):

        closed = False

        while not closed:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    closed = True

            # self.translate_control(self.HappyBread)
            self.accelerate_control(self.HappyBread)
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

    def accelerate_control(self, item, translation_sensitivity=0.38, rotation_sensitivity=0.5):
        # these controls give the item smooth wasd acceleration controls and left/right rotational acceleration
        # ground_axis = self.display_height - item.sprite.get_rect().height / 2
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            item.accelerate(0, -translation_sensitivity)
        if key[pg.K_a]:
            item.accelerate(-translation_sensitivity, 0)
        if key[pg.K_s]:
            item.accelerate(0, translation_sensitivity)
        if key[pg.K_d]:
            item.accelerate(translation_sensitivity, 0)
        if key[pg.K_LEFT]:
            item.accelerate(0, 0, rotation_sensitivity)
        if key[pg.K_RIGHT]:
            item.accelerate(0, 0, -rotation_sensitivity)
        # if item.center[1] < ground_axis:
        item.translate()  # updates after velocity has been updated


if __name__ == "__main__":
    a = Interface()
    a.mainloop()
    quit_app()
