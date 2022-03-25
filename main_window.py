import numpy as np
# import numpy.typing as npt
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from celestial_body_object import CelestialBodyObject, update_trajectories
from load_yaml import dump_objects, load_objects
from main_window_ui import Ui_MainWindow
from simulation import CelestialBody, do_iteration


class PlotManager:
    def __init__(self, plot, body_obj):
        self._body_obj = body_obj

        pen = pg.mkPen(body_obj.color)
        x, y = body_obj.trajectory.x, body_obj.trajectory.y
        self._plot = plot.plot(x, y, pen=pen)
        self._marker = plot.plot(
            [body_obj.body.pos[0]], [body_obj.body.pos[1]],
            pen=pen,
            symbol='o',
            symbolSize=body_obj.size * 26,
            symbolBrush=body_obj.color,
            pxMode=False
        )

    def clear(self):
        self._marker.clear()
        self._plot.clear()

    def plot(self):
        self._marker.setData([self._body_obj.body.pos[0]],
                             [self._body_obj.body.pos[1]])
        self._plot.setData(self._body_obj.trajectory.x,
                           self._body_obj.trajectory.y)


def update_plots(plot_managers):
    for plot_manager in plot_managers:
        plot_manager.plot()


def magnitude(vec):
    return np.sqrt(vec.dot(vec))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graphicsView.setAspectLocked()

        self.plot_managers = []
        self.body_objects = []
        self.current_file_name = None

        self.openAction.triggered.connect(self.open_simulation)
        self.saveAction.triggered.connect(self.save_simulation)
        self.saveAsAction.triggered.connect(self.save_simulation_as)
        body1 = CelestialBody(
            np.array([0, 0], dtype=float),
            np.array([0, 0], dtype=float),
            1.9891e30
        )
        obj1 = CelestialBodyObject(
            body1,
            'body1',
            (255, 0, 0),
            30000000
        )
        self.add_body_obj(obj1)

        body2 = CelestialBody(
            np.array([1.496e11, 0], dtype=float),
            np.array([0, 2.98e4], dtype=float),
            5.98e24
        )
        obj2 = CelestialBodyObject(
            body2,
            'body2',
            (0, 255, 0),
            15000000
        )
        self.add_body_obj(obj2)

        body3 = CelestialBody(
            np.array([1.4998e11, 0], dtype=float),
            np.array([0, 30820.0], dtype=float),
            7.35e22
        )
        obj3 = CelestialBodyObject(
            body3,
            'body3',
            (0, 0, 255),
            200000
        )
        self.add_body_obj(obj3)

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

    def open_simulation(self):
        self.current_file_name, _ = QFileDialog.getOpenFileName(
            self, 'Открытие', filter='*.yaml'
        )
        self.body_objects.clear()
        for plot_manager in self.plot_managers:
            plot_manager.clear()
        self.plot_managers.clear()
        for body_obj in load_objects(self.current_file_name):
            self.add_body_obj(body_obj)

    def save_simulation(self):
        if self.current_file_name is None:
            return self.save_simulation_as()
        self.save_to_current_file()

    def save_to_current_file(self):
        dump_objects(self.body_objects, self.current_file_name)

    def save_simulation_as(self):
        self.current_file_name, _ = QFileDialog.getSaveFileName(
            self, 'Сохранение', filter='*.yaml'
        )
        self.save_to_current_file()

    def add_body_obj(self, body_obj):
        self.plot_managers += [PlotManager(self.graphicsView, body_obj)]
        self.body_objects += [body_obj]

    def do_simulation_iteration(self):
        bodies = [obj.body for obj in self.body_objects]
        do_iteration(bodies, self.delta_time)
        update_trajectories(self.body_objects)
        update_plots(self.plot_managers)

    def update_plot_data(self):
        elapsed = self.elapsed_timer.elapsed()
        self.delta_time = (elapsed - self.elapsed) / 1000
        # print(self.delta_time)
        self.elapsed = elapsed

        self.delta_time = 1000

        self.do_simulation_iteration()
