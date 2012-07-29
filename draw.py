# ------------------------------------------------------------------------
#
#  Written by Sergii Shelestiuk
#
#  Based on code by Martin J. Laubach
#
# ------------------------------------------------------------------------

import turtle
import math
from math import *

turtle.tracer(50000, delay=0)
turtle.register_shape('tri', ((-2, -3), (0, 3), (2, -3), (0, 0)))
turtle.speed(0)
turtle.title("Particle filter demonstration")

UPDATE_EVERY = 0
DRAW_EVERY = 0

class World(object):
    def __init__(self, world_size, beacons):
        self.beacons = beacons
        self.width = int(world_size)
        self.height = int(world_size)
        turtle.setworldcoordinates(0, 0, self.width, self.height)
        self.update_cnt = 0
        self.one_px = float(turtle.window_width()) / float(self.width) / 2

    def draw(self):
        turtle.color("#000000")
        for x, y in self.beacons:
            turtle.up()
            sq = 1.5
            turtle.setposition(x - sq / 2, y - sq / 2)
            turtle.down()
            turtle.setheading(90)
            turtle.begin_fill()
            for _ in range(0, 4):
                turtle.fd(sq)
                turtle.right(90)
            turtle.end_fill()
            turtle.up()

        turtle.color("#88aa00")
        for x, y in self.beacons:
            turtle.setposition(x, y)
            turtle.dot()
        turtle.update()

    def weight_to_color(self, weight):
        return "#%02x00%02x" % (int(weight * 255), int((1 - weight) * 255))

    def show_mean(self, x, y, confident=False):
        if confident:
            turtle.color("#00aa00")
        else:
            turtle.color("#cccccc")
        turtle.setposition(x, y)
        turtle.shape('circle')
        turtle.stamp()

    def show_particles(self, particles):
        self.update_cnt += 1
        if UPDATE_EVERY > 0 and self.update_cnt % UPDATE_EVERY != 1:
            return

        turtle.clearstamps()
        turtle.shape('tri')

        # Particle weights are shown using color variation
        show_color_weights = 1 #len(weights) == len(particles)
        draw_cnt = 0
        px = {}
        for i, p in enumerate(particles):
            draw_cnt += 1
            if DRAW_EVERY == 0 or draw_cnt % DRAW_EVERY == 1:
                # Keep track of which positions already have something
                # drawn to speed up display rendering
                scaled_x = int(p.x * self.one_px)
                scaled_y = int(p.y * self.one_px)
                scaled_xy = scaled_x * 10000 + scaled_y
                if not scaled_xy in px:
                    px[scaled_xy] = 1
                    turtle.setposition([p.x + self.width / 2, p.y + self.height / 2])
                    turtle.setheading(p.theta / pi * 180.0)
                    if(show_color_weights):
                        weight = p.w
                    else:
                        weight = 0.0
                    turtle.color(self.weight_to_color(weight))
                    turtle.stamp()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition([robot.x + self.width / 2, robot.y + self.height / 2])
        turtle.setheading(robot.theta / pi * 180.0)
        turtle.stamp()
        turtle.update()

    def random_place(self):
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return x, y

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def freeze(self):
        turtle.mainloop()


