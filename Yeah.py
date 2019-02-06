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

    def show_bread(self, surface):
        self.game_display.blit(self.HappyBread.rotated, surface)

    def mainloop(self):

        closed = False

        ground_axis = self.display_height - self.HappyBread.sprite.get_rect().height/2

        while not closed:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    closed = True

            # update image surface on controls
            # these controls give the bread up/down and tumble left/right motion
            key = pg.key.get_pressed()
            if key[pg.K_UP]:
                self.HappyBread.translate(0, -9)
            if key[pg.K_LEFT]:
                self.HappyBread.rotate(6)
                self.HappyBread.translate(-9, 0)
            if key[pg.K_RIGHT]:
                self.HappyBread.rotate(-6)
                self.HappyBread.translate(9, 0)
            if key[pg.K_DOWN]:
                if self.HappyBread.center[1] < ground_axis:
                    self.HappyBread.translate(0, 9)
            # should add acceleration next

            self.game_display.fill(white)
            self.show_bread(self.HappyBread.rect)

            pg.display.update()
            self.clock.tick(30)


if __name__ == "__main__":

    a = Interface()
    a.mainloop()
    quit_app()
