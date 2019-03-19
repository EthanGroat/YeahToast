# import pygame as pg  # not needed because it is imported in Toast.py

from Toast import *
from Fleet import *

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


class Game:

    def __init__(self):
        pg.init()

        self.display_width = 1200
        self.display_height = 600

        self.game_display = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption('Yeah Toast!')

        self.clock = pg.time.Clock()

        self.screen_surf = pg.display.get_surface()
        self.x_mid = self.screen_surf.get_rect().centerx
        self.y_mid = self.screen_surf.get_rect().centery

        self.HappyBread = NewtonianItem(game_handle=self, sprite='resources/HappyBread_wT.png',
                                        coordinates=(self.x_mid, self.y_mid))
        self.Toaster = Item(game_handle=self, sprite='resources/Toaster.png',
                            coordinates=(256, 288))
        self.fleet = Fleet([self.Toaster, self.HappyBread])

        self.mode = {'move': 'accelerate', 'sticky_rotate': False}
        # self.events = []

    #   -----------------------------------------------------------------------

    def game_loop(self):

        closed = False

        while not closed:

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    closed = True

            key = pg.key.get_pressed()

            # special controls
            # ----------------
            # modes:
            if key[pg.K_1]:
                self.mode['move'] = "accelerate"
            if key[pg.K_2]:
                self.mode['move'] = "translate"
                self.HappyBread.reset_velocity()
            # freeze and reset
            if key[pg.K_f]:
                self.HappyBread.freeze()
            if key[pg.K_r]:
                self.HappyBread.reset_position(self.x_mid, self.y_mid)

            # Standard player controls:
            if self.mode['move'] == "translate":
                self.translate_control(self.HappyBread, key)
            elif self.mode['move'] == "accelerate":
                self.accelerate_control(self.HappyBread, key)

            # should add bouncing off of objects/walls

            # collision detection:
            if self.fleet.items[0].collides_with(self.fleet.items[1]):
                print("collision at " + self.HappyBread.center_to_string())
                self.HappyBread.apply_force(6, 0)

            self.fleet.update()

            self.game_display.fill(black)
            self.show_all_items()

            pg.display.update()
            self.clock.tick(48)  # Hobbit framerate

    #   -----------------------------------------------------------------------

    def show(self, item):
        self.game_display.blit(item.rotated, item.rect)

    def show_all_items(self):
        for item in self.fleet.items:
            self.show(item)

    #   -----------------------------------------------------------------------

    def translate_control(self, item, key,
                          translation_sensitivity=10,
                          rotation_sensitivity=6.4):
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
            item.rotate(item.omega)
            # silly rotation, press freeze to stop it

    def accelerate_control(self, item, key,
                           accelerate_sensitivity=0.38,
                           rotational_accelerate_sensitivity=0.5,
                           target_rotation=8):
        # these controls give the item smooth wasd acceleration controls and left/right rotational acceleration

        # keyboard controls
        # -----------------
        # non-relative up, down, left, right:
        if key[pg.K_w]:
            item.accelerate(0, -accelerate_sensitivity)
        if key[pg.K_a]:
            item.accelerate(-accelerate_sensitivity, 0)
        if key[pg.K_s]:
            item.accelerate(0, accelerate_sensitivity)
        if key[pg.K_d]:
            item.accelerate(accelerate_sensitivity, 0)
        # angular acceleration:
        if key[pg.K_q] or key[pg.K_u]:
            item.accelerate(0, 0, rotational_accelerate_sensitivity)
            self.mode['sticky_rotate'] = False
        if key[pg.K_e] or key[pg.K_o]:
            item.accelerate(0, 0, -rotational_accelerate_sensitivity)
            self.mode['sticky_rotate'] = False
        # relative forward, backward:
        if key[pg.K_i] or key[pg.K_UP]:
            item.accelerate_forward(accelerate_sensitivity)
        if key[pg.K_k] or key[pg.K_DOWN]:
            item.accelerate_forward(-accelerate_sensitivity)
        # sticky (non-accelerating) rotation:
        if key[pg.K_LEFT] or key[pg.K_j]:
            item.smooth_rotate(target_rotation, sensitivity=16)
            self.mode['sticky_rotate'] = True
        if key[pg.K_RIGHT] or key[pg.K_l]:
            item.smooth_rotate(-target_rotation, sensitivity=16)
            self.mode['sticky_rotate'] = True
        # reset rotation smoothly back to zero:
        if self.mode['sticky_rotate']:
            if not (key[pg.K_LEFT] or key[pg.K_j] or key[pg.K_RIGHT] or key[pg.K_l]):
                item.smooth_rotate(0, sensitivity=30)

        # mouse controls
        if pg.mouse.get_pressed()[0]:
            spot = pg.mouse.get_pos()
            item.smooth_translate(spot[0], spot[1])

    #   -----------------------------------------------------------------------

#   modes for friction,
#   boundary walls,
#   automatic fly back into view


if __name__ == "__main__":
    a = Game()
    a.game_loop()
    quit_app()
