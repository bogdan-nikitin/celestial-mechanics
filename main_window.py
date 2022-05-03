import random

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from celestial_body_object import CelestialBodyObject, update_trajectories
from load_yaml import dump_objects, load_objects
from main_window_ui import Ui_MainWindow
from simulation import CelestialBody, do_iteration, get_energy

LEGEND_OFFSET = (15, 5)
POSITIVE_DOUBLE_REG_EXP = QRegExp("[0-9]+,?[0-9]*")


class PlotManager:
    def __init__(self, plot, body_obj):
        self._body_obj = body_obj
        self._parent_plot = plot
        pen = pg.mkPen(body_obj.color)
        x, y = body_obj.trajectory.x, body_obj.trajectory.y
        self._plot = plot.plot(x, y, pen=pen, name=body_obj.name)
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
        self._parent_plot.addLegend(offset=LEGEND_OFFSET).removeItem(self._plot)

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
        self.legend = self.graphicsView.getPlotItem().addLegend(
            offset=LEGEND_OFFSET
        )
        self.update_legend_visibility()
        self.plot_managers = []
        self.body_objects = []
        self.current_file_name = None
        self.is_simulating = True
        validator = QRegExpValidator(POSITIVE_DOUBLE_REG_EXP, self)
        self.deltaTimeEdit.setValidator(validator)
        self.deltaTimeEdit.editingFinished.connect(self.update_delta_time)
        self.deltaTimeEdit.setText('0,01')
        # self.deltaTimeEdit.setText('0,0001')
        self.softeningEdit.setValidator(validator)
        self.softeningEdit.editingFinished.connect(self.update_softening)
        self.softeningEdit.setText('0,1')
        # self.softeningEdit.setText('0')
        self.showLegendBox.stateChanged.connect(self.update_legend_visibility)
        self.controlButton.clicked.connect(self.change_simulation_state)
        self.openAction.triggered.connect(self.open_simulation)
        self.saveAction.triggered.connect(self.save_simulation)
        self.saveAsAction.triggered.connect(self.save_simulation_as)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()

        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()
        self.last_elapsed = self.elapsed_timer.elapsed()
        self.elapsed = 0
        self.delta_time = self.parse_delta_time()
        self.softening = self.parse_softening()
        self.simulation_time = 0
        self.iter_count = 0

        # self._mass_center = self.graphicsView.plot(
        #     [], [],
        #     symbol='o',
        #     symbolSize=0.1,
        #     pxMode=False
        # )

        self.generate_random_simulation()
        self.start_energy = get_energy(self.get_bodies())

    def generate_random_simulation(self):
        for i in range(3):
            body = CelestialBody(
                np.random.sample(2) * 10,
                np.array([0, 0], dtype=float),
                5e10
            )
            obj = CelestialBodyObject(
                body,
                str(i),
                (random.randint(0, 255),
                 random.randint(0, 255),
                 random.randint(0, 255)),
                0.02
            )
            self.add_body_obj(obj)

    def update_legend_visibility(self):
        self.legend.setVisible(self.showLegendBox.checkState())

    def parse_delta_time(self):
        return float(self.deltaTimeEdit.text().replace(',', '.'))

    def parse_softening(self):
        return float(self.softeningEdit.text().replace(',', '.'))

    def update_delta_time(self):
        self.delta_time = self.parse_delta_time()

    def update_softening(self):
        self.softening = self.parse_softening()

    def change_simulation_state(self):
        self.is_simulating = not self.is_simulating
        if self.is_simulating:
            self.controlButton.setText('Остановить')
        else:
            self.controlButton.setText('Запустить')
            self.last_elapsed = self.elapsed_timer.elapsed()

    def open_simulation(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Открытие', filter='*.yaml'
        )
        if file_name == '':
            return
        try:
            objects = load_objects(file_name)
        except Exception as e:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText('При загрузке симуляции произошла ошибка')
            msg.setWindowTitle("Ошибка")
            msg.show()
            print(f'Error while loading file - {e.__class__.__name__}: {e}')
            return
        self.current_file_name = file_name
        self.body_objects.clear()
        for plot_manager in self.plot_managers:
            plot_manager.clear()
        self.plot_managers.clear()
        for body_obj in objects:
            self.add_body_obj(body_obj)
        self.start_energy = get_energy(self.get_bodies())
        self.simulation_time = 0
        self.iter_count = 0

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

    def get_bodies(self):
        return [obj.body for obj in self.body_objects]

    def do_simulation_iteration(self):
        self.iter_count += 1
        do_iteration(self.get_bodies(), self.delta_time, self.softening)
        update_trajectories(self.body_objects)
        update_plots(self.plot_managers)
        # if self.iter_count % 30 == 0:
        #
        #     update_plots(self.plot_managers)

    def update_simulation(self):
        if not self.is_simulating:
            return
        self.do_simulation_iteration()
        self.simulation_time += self.delta_time
        percent = (1 - get_energy(self.get_bodies()) / self.start_energy) * 100
        self.energyDeviationEdit.setText(f'{percent:.10f}')
        elapsed = self.elapsed_timer.elapsed()
        self.elapsed = (elapsed - self.last_elapsed) / 1000
        self.last_elapsed = elapsed
        # if self.elapsed != 0:
        self.simulationSpeedEdit.setText(
            f'{self.delta_time / self.elapsed:.10f}'
        )
        self.iterSpeedEdit.setText(f'{1 / self.elapsed:.10f}')
        self.iterCountEdit.setText(str(self.iter_count))
        self.simulationTimeEdit.setText(f'{self.simulation_time:.10f}')

        # # barycenter
        # bodies = self.get_bodies()
        # pos = bodies[0].pos.copy() * bodies[0].m
        # mass = bodies[0].m
        # for body in bodies[1:]:
        #     pos += body.pos * body.m
        #     mass += body.m
        # pos /= mass
        # self._mass_center.setData([pos[0]], [pos[1]])
