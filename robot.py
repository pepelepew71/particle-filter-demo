# from math import *
import math
import random

from config import *


class Robot:

    def __init__(self):
        self.x = random.random()*WORLD_SIZE
        self.y = random.random()*WORLD_SIZE
        self.orientation = random.random()*2.0*math.pi
        self.noise_forward = 0.0  # sigma
        self.noise_turn = 0.0
        self.noise_sensor = 0.0

    def set(self, x, y, orientation):
        if not 0.0 <= x < WORLD_SIZE:
            raise ValueError('X coordinate out of bound')
        if not 0.0 <= y < WORLD_SIZE:
            raise ValueError('Y coordinate out of bound')
        if not 0.0 <= orientation < 2.0*math.pi:
            raise ValueError('Orientation must be in [0, 2pi]')
        self.x = float(x)
        self.y = float(y)
        self.orientation = float(orientation)

    def set_random_stats(self):
        self.x = random.random()*WORLD_SIZE
        self.y = random.random()*WORLD_SIZE
        self.orientation = random.random()*2.0*math.pi

    def set_noise(self, noise_forward, noise_turn, noise_sensor):
        # -- makes it possible to change the noise parameters, this is often useful in particle filters
        self.noise_forward = noise_forward
        self.noise_turn = noise_turn
        self.noise_sensor = noise_sensor

    def get_measurements(self):
        measurements = []
        for landmark in LANDMARKS:
            dist = math.sqrt((self.x - landmark[0])**2.0 + (self.y - landmark[1])**2.0)
            dist += random.gauss(0.0, self.noise_sensor)
            measurements.append(dist)
        return measurements

    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cant move backwards')

        # -- turn, and add randomness to the turning command
        self.orientation += float(turn) + random.gauss(0.0, self.noise_turn)
        self.orientation %= 2 * math.pi  # cyclic truncate

        # -- move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.noise_forward)
        self.x += dist * math.cos(self.orientation)
        self.y += dist * math.sin(self.orientation)
        self.x %= WORLD_SIZE  # cyclic truncate
        self.y %= WORLD_SIZE

    def get_gaussian(self, mu, sigma, x):
        # -- calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return math.exp(- ((mu - x)**2) / (sigma**2) / 2.0) / math.sqrt(2.0*math.pi*(sigma**2.0))

    def get_measurements_likelihood(self, measurements):
        # -- calculates how likely a measurement should be
        prob = 1.0;
        for landmark, x in zip(LANDMARKS, measurements):
            dist = math.sqrt((self.x - landmark[0])**2.0 + (self.y - landmark[1])**2.0)
            prob *= self.get_gaussian(dist, self.noise_sensor, x)
        return prob

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
