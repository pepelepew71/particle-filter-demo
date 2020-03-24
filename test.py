#!/usr/bin/env python3

# import random

import matplotlib.pyplot as plt

from config import *
from robot import Robot
import utilities

if __name__ == "__main__":

    plt.figure()

    # -- real robot
    robot = Robot()
    robot.set(x=50, y=50, orientation=0)
    robot.set_noise(0.05, 0.05, 5.0)

    # -- set particles
    N = 1000
    particles = []

    for _ in range(N):
        p = Robot()
        p.set_noise(0.05, 0.05, 5.0)
        particles.append(p)

    utilities.plot(robot=robot, particles=particles)

    # -- start moving
    step = 30

    for _ in range(step):
        # movement = -2.0 + random.random()*4.0, 5.0
        turn, forward = 0.2, 5.0
        robot.move(turn=turn, forward=forward)
        measurements = robot.get_measurements()

        for p in particles:
            p.move(turn=turn, forward=forward)

        weights = list()
        for p in particles:
            weights.append(p.get_measurements_likelihood(measurements=measurements))

        particles = utilities.resampling(weights=weights, particles=particles)

        utilities.plot(robot=robot, particles=particles)
        print(utilities.get_mean_error(robot, particles))
