import pygame as pg
import math


class Item:
    def __init__(self, sprite, coordinates):
        self.center = list(coordinates)  # internal coordinates used to remap surface, takes floats
        self.rotation = 0.0  # in degrees
        self.sprite = pg.image.load(sprite)
        self.rotated = self.sprite
        self.rect = self.rotated.get_rect(center=coordinates)
        # this is a rectangle used as a proxy for re-centering and blitting the sprite to the right location

    def translate(self, x_by=0.0, y_by=0.0, phi=0.0):  # used for both rotation and translation
        # defaults to zero for interoperability in updating Items
        self.rect.centerx += x_by
        self.rect.centery += y_by
        self.center = list(self.rect.center)
        self.rotate(phi)

    def rotate(self, degrees):
        self.rotation += degrees
        self.rotated = pg.transform.rotate(self.sprite, self.rotation)
        self.rect = self.rotated.get_rect(center=self.center)  # working! :D


class AcceleratingItem(Item):
    def __init__(self, sprite, coordinates, velocity=(0.0, 0.0), womega=0.0):
        self.velocity = list(velocity)  # lists are mutable, tuples aren't
        self.omega = womega
        super().__init__(sprite, coordinates)

    def translate(self, x_by=0.0, y_by=0.0, phi=0.0):
        """updates position incrementally using relative coordinates"""
        self.center[0] += x_by + self.velocity[0]  # center tracks exact floating point positions
        self.center[1] += y_by + self.velocity[1]
        self.rect.center = tuple(self.center)  # this assignment updates the pygame sprite placement coordinates
        self.rotate(phi + self.omega)  # exact degrees

    def teleport(self, x, y, reset_rotation=False):
        """translates to an exact location"""
        self.center[0] = x
        self.center[1] = y
        self.rect.center = tuple(self.center)  # update pygame sprite placement
        if reset_rotation:
            self.rotate(-self.rotation)

    def accelerate(self, x_acceleration=0.0, y_acceleration=0.0, angular_acceleration=0.0):
        self.velocity[0] += x_acceleration
        self.velocity[1] += y_acceleration
        self.omega += angular_acceleration

    def accelerate_forward(self, acceleration=0.0):
        x_comp = -acceleration * math.sin(math.radians(self.rotation))  # sine takes radians, not degrees!
        y_comp = -acceleration * math.cos(math.radians(self.rotation))
        self.accelerate(x_comp, y_comp)

    def update(self, x_acc=0.0, y_acc=0.0, angular_acc=0.0):
        # this function is not really needed but here anyway to further generalize the update idea
        # and encapsulate every normal incremental thing that AcceleratingItems do.
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

    def throw(self, x, y, speed=1.0):  # fast translate to a specific point
        # if point is moving, end with continued velocity of speed*velocity of the moving point
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

    def smooth_rotate(self, degrees):
        pass


class NewtonianItem(AcceleratingItem):
    def __init__(self, sprite, coordinates, mass=1.0, velocity=(0.0, 0.0), womega=0.0):
        self.mass = mass
        self.netForces = [0.0, 0.0]
        super().__init__(sprite, coordinates, velocity, womega)

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

    # this is the class where update() becomes important
    def update(self, x_force=0.0, y_force=0.0, angular_acc=0.0):
        # takes the x and y components of an applied force as arguments
        # (optional as update() can be called after any number of calls of apply_force() in the game loop)
        self.apply_force(x_force, y_force)
        self.accelerate()
        self.translate()
        self.set_net_forces(0.0, 0.0)

