from copy import copy
import math
import random

import matplotlib.pyplot as plt

from config import *
from robot import Robot

def plot(robot, particles):

    ax = plt.gca()
    ax.cla()

    # -- particles
    x = list()
    y = list()
    markers = list()
    for i in particles:
        x.append(i.x)
        y.append(i.y)
        markers = (3, 1, i.orientation / math.pi * 180.0)
    ax.scatter(x, y, s=30, marker=markers, edgecolors='r', facecolors='none', alpha=0.1)

    # -- landmarks
    x = list()
    y = list()
    for mark in LANDMARKS:
        x.append(mark[0])
        y.append(mark[1])
    ax.scatter(x, y, s=30, marker='+', c='g')

    # -- robot
    marker_rotated_deg = robot.orientation/math.pi*180.0 - 90
    ax.scatter(robot.x, robot.y, s=100, marker=(3, 0, marker_rotated_deg), edgecolors='b', facecolors='none')
    ax.scatter(robot.x+2.0*math.cos(robot.orientation), robot.y+2.0*math.sin(robot.orientation), s=10, marker="o", c='b')  # for heading

    ax.set_xlim(left=0, right=100)
    ax.set_ylim(bottom=0, top=100)
    ax.set_aspect('equal', 'box')

    plt.pause(0.2)
    # plt.show()

def get_mean_error(r, p):
    sum = 0.0;
    for i in range(len(p)):  # calculate mean error
        dx = (p[i].x - r.x + (WORLD_SIZE/2.0)) % WORLD_SIZE - (WORLD_SIZE/2.0)
        dy = (p[i].y - r.y + (WORLD_SIZE/2.0)) % WORLD_SIZE - (WORLD_SIZE/2.0)
        err = math.sqrt(dx**2.0 + dy**2.0)
        sum += err
    return sum / float(len(p))

def resampling(weights, particles, is_add_random=False, random_num=100):
    samples = list()
    count = len(particles)
    index = int(random.random()*count)
    beta = 0.0
    max_weight = max(weights)

    for _ in range(count):
        beta += random.random() * 2.0 * max_weight
        while beta > weights[index]:
            beta -= weights[index]
            index = (index + 1) % count
        samples.append(copy(particles[index]))

    if is_add_random:
        noise_f = samples[0].noise_forward
        noise_t = samples[0].noise_turn
        noise_s = samples[0].noise_sensor
        samples = samples[:-random_num]
        for _ in range(random_num):
            p = Robot()
            p.set_noise(noise_forward=noise_f, noise_turn=noise_t, noise_sensor=noise_s)
            samples.append(p)

    return samples
