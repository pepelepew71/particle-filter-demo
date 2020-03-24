from copy import copy
import math
import random

from config import *
from robot import Robot

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

def get_gaussian(mu, sigma, x):
    # -- calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
    return math.exp(- ((mu - x)**2) / (sigma**2) / 2.0) / math.sqrt(2.0*math.pi*(sigma**2.0))
