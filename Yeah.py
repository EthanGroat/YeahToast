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
violet = (128, 0, 144)


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

        self.HappyBread = AcceleratingItem(sprite='resources/HappyBread_wT.png',
                                           coordinates=(self.x_mid, self.y_mid))
        self.Toaster = Item(sprite='resources/Toaster.png', coordinates=(120, 140))

    def game_loop(self):

        closed = False
        mode = "accelerate"

        while not closed:

            ev = pg.event.get()
            for event in ev:
                if event.type == pg.QUIT:
                    closed = True

            key = pg.key.get_pressed()

            # modes:
            if key[pg.K_1]:
                mode = "accelerate"
            if key[pg.K_2]:
                mode = "translate"
                self.HappyBread.reset_velocity()
            # freeze and reset
            if key[pg.K_f]:
                self.HappyBread.freeze()
            if key[pg.K_r]:
                self.HappyBread.reset_position(self.x_mid, self.y_mid)

            # player control:
            if mode == "translate":
                self.translate_control(self.HappyBread, ev, key)
            elif mode == "accelerate":
                self.accelerate_control(self.HappyBread, ev, key)
            # should add bouncing off of objects/walls
            # and collision detection

            self.game_display.fill(violet)
            self.show(self.HappyBread)

            pg.display.update()
            self.clock.tick(48)  # Hobbit framerate

    def show(self, item):
        self.game_display.blit(item.rotated, item.rect)

    def translate_control(self, item, events, key, translation_sensitivity=10, rotation_sensitivity=6.4):
        # these controls give the bread (or any item) up/down and tumble left/right motion
        ground_axis = self.display_height - item.sprite.get_rect().height / 2
        if key[pg.K_UP] or key[pg.K_w]:
            item.translate(0, -translation_sensitivity)
        if key[pg.K_LEFT] or key[pg.K_a]:
            item.rotate(rotation_sensitivity)
            item.translate(-translation_sensitivity, 0)
        if key[pg.K_DOWN] or key[pg.K_s]:
            if item.center[1] < ground_axis:
                item.translate(0, translation_sensitivity)
        if key[pg.K_RIGHT] or key[pg.K_d]:
            item.rotate(-rotation_sensitivity)
            item.translate(translation_sensitivity, 0)
        # mouse controls
        if pg.mouse.get_pressed()[0]:
            spot = pg.mouse.get_pos()
            print(spot)
            item.teleport(spot[0], spot[1])
            item.rotate(item.omega)  # silly rotation, press freeze to stop it

    def accelerate_control(self, item, events, key, translation_sensitivity=0.38, rotation_sensitivity=0.5):
        # these controls give the item smooth wasd acceleration controls and left/right rotational acceleration
        # ground_axis = self.display_height - item.sprite.get_rect().height / 2
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
        if key[pg.K_UP]:
            item.accelerate_forward(translation_sensitivity)
        if key[pg.K_DOWN]:
            item.accelerate_forward(-translation_sensitivity)
        # mouse controls
        if pg.mouse.get_pressed()[0]:
            spot = pg.mouse.get_pos()
            item.smooth_translate(spot[0], spot[1])
        item.translate()  # updates after velocity has been updated


#   modes for friction,
#   boundaries,
#   automatic fly back


if __name__ == "__main__":
    a = Interface()
    a.game_loop()
    quit_app()
