import pygame as pg
from Toast import *

pg.init()

display_width = 800
display_height = 600

# color definition triplets
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)

gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Yeah Toast!')

clock = pg.time.Clock()


HappyBread = Bread(sprite='resources/HappyBread.png')


def show_bread(x, y):
    gameDisplay.blit(HappyBread.rotated, (x, y))


x_center = display_width/2
y_center = display_height/2

x = display_width/3
y = display_height/3


def display_everything():
    crashed = False

    while not crashed:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True

            print(event)

        pg.display.update()
        clock.tick(60)


def quit_app():
    pg.quit()
    quit()


def mainloop():
    global x, y

    closed = False

    while not closed:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                closed = True

        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            y -= 5
        elif key[pg.K_LEFT]:
            HappyBread.rotate(6)
        elif key[pg.K_RIGHT]:
            HappyBread.rotate(-6)
        elif key[pg.K_DOWN]:
            y += 5

        gameDisplay.fill(white)
        show_bread(x, y)

        pg.display.update()
        clock.tick(30)


if __name__ == "__main__":
    # display_everything()
    mainloop()
    quit_app()
