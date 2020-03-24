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
    noise_forward = 0.05
    noise_turn = 0.05
    noise_sensor = 5.0

    # -- real robot
    robot = Robot()
    # robot.set(x=50, y=50, orientation=0)
    robot.set_noise(noise_forward=noise_forward, noise_turn=noise_turn, noise_sensor=noise_sensor)

    # -- set particles
    N = 1000
    particles = []

    for _ in range(N):
        p = Robot()
        p.set_noise(noise_forward=noise_forward, noise_turn=noise_turn, noise_sensor=noise_sensor)
        particles.append(p)

    # -- gui
    root = gui.Root(robot=robot, particles=particles)
    root.mainloop()
