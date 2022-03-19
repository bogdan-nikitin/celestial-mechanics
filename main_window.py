from simulation import CelestialBody, do_iteration


import numpy as np
# import numpy.typing as npt
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from dataclasses import dataclass

from typing import List
from main_window_ui import Ui_MainWindow


@dataclass
class CelestialBodyTrajectory:
    x: List[float]
    y: List[float]


@dataclass
class CelestialBodyProperties:
    name: str
    color: (int, int, int)
    size: int


class CelestialBodyPlotItems:
    def __init__(self, main_window, body, trajectory, properties):
        self._body = body
        self._trajectory = trajectory
        self._properties = properties

        pen = pg.mkPen(properties.color)
        x, y = trajectory.x, trajectory.y
        self._plot = main_window.graphicsView.plot(x, y, pen=pen)
        self._marker = main_window.graphicsView.plot(
            [body.pos[0]], [body.pos[1]],
            pen=pen,
            symbol='o',
            symbolSize=properties.size * 25,
            symbolBrush=properties.color,
            pxMode=False
        )

    def plot(self):
        self._marker.setData([self._body.pos[0]], [self._body.pos[1]])
        self._plot.setData(self._trajectory.x, self._trajectory.y)


@dataclass
class CelestialBodyObject:
    def __init__(self, main_window, body, properties):
        self.body = body
        self.trajectory = CelestialBodyTrajectory([body.pos[0]], [body.pos[1]])
        self.properties = properties
        self.plot_items = CelestialBodyPlotItems(
            main_window, body, self.trajectory, properties
        )

    body: CelestialBody
    trajectory: CelestialBodyTrajectory
    properties: CelestialBodyProperties
    plot_items: CelestialBodyPlotItems


def update_trajectories(bodies_and_trajectories):
    for body, trajectory in bodies_and_trajectories:
        trajectory.x += [body.pos[0]]
        trajectory.y += [body.pos[1]]


def update_plots(celestial_body_plot_items_list):
    for celestial_body_plot_items in celestial_body_plot_items_list:
        celestial_body_plot_items.plot()


def magnitude(vec):
    return np.sqrt(vec.dot(vec))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setAspectLocked()

        self.celestial_body_objects = []
        body1 = CelestialBody(
            np.array([0, 0], dtype=float),
            np.array([0, 0], dtype=float),
            1.9891e30
        )
        body1_prop = CelestialBodyProperties(
            'body1',
            (255, 0, 0),
            30000000
        )
        obj1 = CelestialBodyObject(self, body1, body1_prop)

        body2 = CelestialBody(
            np.array([1.496e11, 0], dtype=float),
            np.array([0, 2.98e4], dtype=float),
            5.98e24
        )
        body2_prop = CelestialBodyProperties(
            'body2',
            (0, 255, 0),
            15000000
        )
        obj2 = CelestialBodyObject(self, body2, body2_prop)

        body3 = CelestialBody(
            np.array([1.4998e11, 0], dtype=float),
            np.array([0, 30820.0], dtype=float),
            7.35e22
        )
        body3_prop = CelestialBodyProperties(
            'body2',
            (0, 0, 255),
            200000
        )
        obj3 = CelestialBodyObject(self, body3, body3_prop)

        self.celestial_body_objects += [obj1, obj2, obj3]

        # self.graphicsView.setBackground('w')
        # arrow = pg.ArrowItem(pos=[1000, 1000], angle=90, tailLen=100)
        # self.graphicsView.addItem(arrow)
        # arrow.hide()

        self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        # self.update_plot_data()

        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        self.elapsed = 0
        self.delta_time = 0

    def do_simulation_iteration(self):
        bodies = [obj.body for obj in self.celestial_body_objects]
        do_iteration(bodies, self.delta_time)
        bodies_and_trajectories = [
            (obj.body, obj.trajectory) for obj in self.celestial_body_objects
        ]
        update_trajectories(bodies_and_trajectories)
        celestial_body_plot_items = [
            obj.plot_items for obj in self.celestial_body_objects
        ]
        update_plots(celestial_body_plot_items)

    def update_plot_data(self):
        elapsed = self.elapsed_timer.elapsed()
        self.delta_time = (elapsed - self.elapsed) / 1000
        # print(self.delta_time)
        self.elapsed = elapsed

        self.delta_time = 1000

        self.do_simulation_iteration()


