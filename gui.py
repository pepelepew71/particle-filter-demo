import math
import random
import time
import tkinter as tk
import tkinter.ttk as ttk

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import *
import utilities

matplotlib.use('TkAgg')


class Root(tk.Tk, object):

    def __init__(self, robot, particles):
        super(Root, self).__init__()

        self.robot = robot
        self.particles = particles

        self.frame_fig = FrameFig(master=self)
        self.frame_scale = FrameScale(master=self)
        self.frame_button = FrameButton(master=self)

        self.frame_fig.pack(side='top', fill='both', padx=10, pady=(10, 5), expand=True)
        self.frame_scale.pack(side='top', padx=10, pady=(5, 5))
        self.frame_button.pack(side='top', fill='x', padx=10, pady=(5, 10))

        self._setup_bind()

    def _setup_bind(self):
        self.bind('<Escape>', lambda evt: self.destroy())


class FrameFig(tk.Frame, object):

    def __init__(self, master):
        super(FrameFig, self).__init__(master=master)

        figure = plt.Figure(figsize=(6,6), dpi=100)
        self.ax = figure.add_subplot(111)
        self.plot = FigureCanvasTkAgg(figure=figure, master=self)
        self.plot.get_tk_widget().pack(side='top', expand=True)


class FrameScale(tk.Frame, object):

    def __init__(self, master):
        super(FrameScale, self).__init__(master=master)

        tk.Label(master=self, text="Forward").grid(row=0, column=0, sticky='es')
        self.scale_forward = tk.Scale(master=self, from_=0.0, to=10.0, length=300, orient="horizontal")
        self.scale_forward.set(1.0)
        self.scale_forward.grid(row=0, column=1)

        tk.Label(master=self, text="Turn").grid(row=1, column=0, sticky='es')
        self.scale_turn = tk.Scale(master=self, from_=-60.0, to=60.0, length=300, orient="horizontal")
        self.scale_turn.set(0.0)
        self.scale_turn.grid(row=1, column=1)

        tk.Label(master=self, text="Random").grid(row=2, column=0, sticky='es')
        self.scale_resample = tk.Scale(master=self, from_=1, to=100.0, length=300, orient="horizontal")
        self.scale_resample.set(0)
        self.scale_resample.grid(row=2, column=1)
        self.check_num = tk.IntVar()
        tk.Checkbutton(master=self, variable=self.check_num).grid(row=2, column=2, sticky='s')


class FrameButton(tk.Frame, object):

    def __init__(self, master):
        super(FrameButton, self).__init__(master=master)

        self.btn_init = tk.Button(master=self, text="Init", command=self._call_init)
        self.btn_01_s = tk.Button(master=self, text="1 Step", command=self._call_01_step)
        self.btn_20_s = tk.Button(master=self, text="20 Steps", command=self._call_20_step)
        self.btn_auto = tk.Button(master=self, text="Auto", command=self._call_auto)
        self.btn_stop = tk.Button(master=self, text="Stop", command=self._call_stop)
        self.btn_kid = tk.Button(master=self, text="Kidnapped", command=self._call_kidnap)

        self.btn_init.pack(side='left', padx=(5,5), pady=(5,0))
        self.btn_01_s.pack(side='left', padx=(0,5), pady=(5,0))
        self.btn_20_s.pack(side='left', padx=(0,5), pady=(5,0))
        self.btn_auto.pack(side='left', padx=(0,5), pady=(5,0))
        self.btn_stop.pack(side='left', padx=(0,5), pady=(5,0))
        self.btn_kid.pack(side='left', padx=(0,5), pady=(5,0))

        self._is_running = None

        self._plot()  # initial plot

    def _plot(self):
        self.master.frame_fig.ax.cla()

        # -- particles
        xs = list()
        ys = list()
        markers = list()
        for p in self.master.particles:
            xs.append(p.x)
            ys.append(p.y)
            markers = (3, 1, p.orientation / math.pi * 180.0 - 90.0)
        self.master.frame_fig.ax.scatter(xs, ys, s=30, marker=markers, edgecolors='r', facecolors='none', alpha=0.1)

        # -- landmarks
        xs = list()
        ys = list()
        for mark in LANDMARKS:
            xs.append(mark[0])
            ys.append(mark[1])
        self.master.frame_fig.ax.scatter(xs, ys, s=30, marker='+', c='g')

        # -- robot
        x = self.master.robot.x
        y = self.master.robot.y
        orient = self.master.robot.orientation
        marker_rotated_deg = self.master.robot.orientation/math.pi*180.0 - 90.0
        self.master.frame_fig.ax.scatter(x, y, s=100, marker=(3, 0, marker_rotated_deg), edgecolors='b', facecolors='none')
        self.master.frame_fig.ax.scatter(x+2.0*math.cos(orient), y+2.0*math.sin(orient), s=10, marker="o", c='b')  # for heading

        self.master.frame_fig.ax.set_xlim(left=0, right=100)
        self.master.frame_fig.ax.set_ylim(bottom=0, top=100)
        self.master.frame_fig.ax.set_aspect('equal', 'box')
        self.master.frame_fig.plot.draw()

        self.master.update()

    def _call_01_step(self):
        forward = float(self.master.frame_scale.scale_forward.get())
        turn = - float(self.master.frame_scale.scale_turn.get()) / 180.0 * math.pi  # inverse scale bar for direction

        # -- robot
        self.master.robot.move(turn=turn, forward=forward)
        measurements = self.master.robot.get_measurements()

        # -- particles
        for p in self.master.particles:
            p.move(turn=turn, forward=forward)

        weights = list()
        for p in self.master.particles:
            weights.append(p.get_measurements_likelihood(measurements=measurements))

        if self.master.frame_scale.check_num.get():
            num = int(self.master.frame_scale.scale_resample.get())
            self.master.particles = utilities.resampling(weights=weights, particles=self.master.particles, is_add_random=True, random_num=num)
        else:
            self.master.particles = utilities.resampling(weights=weights, particles=self.master.particles)

        print(utilities.get_mean_error(r=self.master.robot, p=self.master.particles))
        self._plot()

    def _call_20_step(self):
        step = 20
        for _ in range(step):
            self._call_01_step()
            time.sleep(0.1)

    def _call_init(self):
        for p in self.master.particles:
            p.set_random_stats()
        self._plot()

    def _call_auto(self):
        self._is_running = True
        while self._is_running:
            self._call_01_step()
            time.sleep(0.1)

    def _call_stop(self):
        self._is_running = False

    def _call_kidnap(self):
        self.master.robot.set_random_stats()
        self._plot()
