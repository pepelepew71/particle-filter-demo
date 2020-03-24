#!/usr/bin/env python3

from copy import copy
import math
import random

from config import *
import gui
from robot import Robot
import utilities

if __name__ == "__main__":

    # -- noise (sigma)
    noise_f = 0.05
    noise_t = 0.05
    noise_s = 5.0

    # -- real robot
    robot = Robot()
    robot.set_noise(noise_forward=noise_f, noise_turn=noise_t, noise_sensor=noise_s)

    # -- set particles
    n = 1000
    particles = []

    for _ in range(n):
        p = Robot()
        p.set_noise(noise_forward=noise_f, noise_turn=noise_t, noise_sensor=noise_s)
        particles.append(p)

    # -- gui
    root = gui.Root(robot=robot, particles=particles)
    root.mainloop()
