import pygame as pg
import math
from random import *
from Colors import *


class Item:

    def __init__(self, game_handle, sprite=None, coordinates=(0, 0), width=250.0, color=green):
        self.game_handle = game_handle
        if sprite:  # comprehensive sprite handling
            if type(sprite) is str:
                self.sprite = pg.image.load(sprite)
                print('Image load successful.')
            elif isinstance(sprite, pg.Surface):  # for pre-loaded sprites
                self.sprite = sprite
        else:
            self.sprite = pg.Surface((32, 32), pg.SRCALPHA)
            pg.draw.rect(self.sprite, color, pg.Rect(4, 4, 24, 14), 4)

        self.rotated = self.sprite
        self.rect = self.rotated.get_rect(center=coordinates)
        self.center = list(coordinates)  # internal coordinates used to remap surface, takes lists of floats
        self.rotation = 0.0  # in degrees
        self.radius = width / 2
        # this is a rectangle used as a proxy for re-centering and blitting the sprite to the right location

    def translate(self, x_by=0.0, y_by=0.0, phi=0.0):  # used for both rotation and translation
        # defaults to zero for interoperability in updating Items
        self.center[0] += x_by
        self.center[1] += y_by
        self.rect.center = tuple(self.center)  # update pygame sprite placement
        self.rotate(phi)

    def translate_forward(self, distance):
        self.center[0] += -distance * math.sin(math.radians(self.rotation))  # sine takes radians, not degrees!
        self.center[1] += -distance * math.cos(math.radians(self.rotation))
        self.rect.center = tuple(self.center)  # update pygame sprite placement

    def teleport(self, x, y, reset_rotation=False):
        """translates to an exact location"""
        self.center[0] = x
        self.center[1] = y
        self.rect.center = tuple(self.center)  # update pygame sprite placement
        if reset_rotation:
            self.rotate(-self.rotation)

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        self.rect = self.rotated.get_rect(center=self.center)

    def update(self):
        # this function is here to generalize the update idea to all Items
        pass

    def show(self):
        self.game_handle.game_display.blit(self.rotated, self.rect)

    def center_to_string(self):
        return "({:.1f}, {:.1f})".format(self.center[0], self.center[1])

    def distance_squared(self, target):  # squaring is easier than square-rooting elsewhere
        return (self.center[0] - target.center[0])**2 + (self.center[1] - target.center[1])**2

    def collides_with(self, target):
        if self.distance_squared(target) < (self.radius + target.radius)**2:
            return True
        else:
            return False


class AcceleratingItem(Item):

    def __init__(self, game_handle, sprite=None, coordinates=(0, 0), width=250.0, velocity=(0.0, 0.0), womega=0.0):
        self.velocity = list(velocity)  # lists are mutable, tuples aren't
        self.omega = womega  # angular velocity
        super().__init__(game_handle, sprite, coordinates, width)

    def translate(self, x_by=0.0, y_by=0.0, phi=0.0):
        """updates position incrementally using relative coordinates"""
        self.center[0] += x_by + self.velocity[0]  # center tracks exact floating point positions
        self.center[1] += y_by + self.velocity[1]
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
        # This function encapsulates every normal incremental thing that AcceleratingItems do.
        self.accelerate(x_acc, y_acc, angular_acc)
        self.translate()

    def reset_velocity(self, velocity=(0.0, 0.0), reset_angular=False):
        self.velocity[0], self.velocity[1] = velocity[0], velocity[1]
        if reset_angular:
            self.reset_angular_velocity()

    def reset_angular_velocity(self, omega=0.0):
        self.omega = omega

    def freeze(self):
        self.reset_velocity((0, 0), reset_angular=True)

    def reset_position(self, x=550, y=300):
        self.freeze()
        self.teleport(x, y, reset_rotation=True)
        # self.smooth_translate() to origin instead of teleport

    def throw(self, x, y, speed=1.0):  # fast translate toward a specific point
        # if point is moving and speed=1, end with continued velocity
        # of speed*velocity of the moving point
        delta_x = x - self.center[0]
        delta_y = y - self.center[1]
        self.velocity = [delta_x*speed, delta_y*speed]

    def smooth_translate(self, x, y, sensitivity=3.0, damping_ratio=0.2):
        """Uses damped simple harmonic motion to smoothly move toward a specified absolute location"""
        delta_x = x - self.center[0]
        delta_y = y - self.center[1]
        k = sensitivity/50.0
        # the order of these operations actually matters to how accurate the representation of harmonic oscillation is
        self.accelerate(k * delta_x, k * delta_y)
        self.accelerate(-damping_ratio * self.velocity[0], -damping_ratio * self.velocity[1])

    def smooth_rotate(self, target_angular_velocity, sensitivity=100.0):  # 100 is max sensitivity - instant
        k = sensitivity/100.0  # sensitivity above 15 is quite fast
        angular_acceleration = k * (target_angular_velocity - self.omega)
        self.accelerate(0, 0, angular_acceleration)
        if not self.omega == 0:
            if abs(self.omega) < 0.003:
                self.omega = 0
            print(self.omega)


class NewtonianItem(AcceleratingItem):

    def __init__(self, game_handle, sprite=None, coordinates=(0, 0), width=250.0,
                 mass=1.0, velocity=(0.0, 0.0), womega=0.0):
        self.mass = mass
        self.netForces = [0.0, 0.0]
        super().__init__(game_handle, sprite, coordinates, width, velocity, womega)

    def set_net_forces(self, net_x, net_y):  # takes coordinate floats and puts them in the Force vector
        self.netForces = [net_x, net_y]

    def apply_force(self, x, y):  # adds to netForces
        self.netForces[0] += x
        self.netForces[1] += y

    def set_mass(self, mass):
        self.mass = mass

    def accelerate(self, x_extra=0.0, y_extra=0.0, angular_acceleration=0.0):  # computes using forces and mass
        self.velocity[0] += x_extra + self.netForces[0]/self.mass
        self.velocity[1] += y_extra + self.netForces[1]/self.mass
        self.omega += angular_acceleration

    # this is the class where update() becomes really important
    def update(self, x_force=0.0, y_force=0.0, angular_acc=0.0):
        # takes the x and y components of an applied force as arguments
        # (optional as update() can be called after any number of calls of apply_force() in the game loop)
        self.apply_force(x_force, y_force)
        self.accelerate()
        if self.game_handle.mode:
            if self.game_handle.mode['move'] == 'translate':
                self.reset_velocity()
                # print('It worked!')
        self.translate()
        self.set_net_forces(0.0, 0.0)
