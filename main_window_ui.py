# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 427)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.deltaTimeBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.deltaTimeBox.setMinimum(0.0)
        self.deltaTimeBox.setMaximum(1e+297)
        self.deltaTimeBox.setProperty("value", 0.01)
        self.deltaTimeBox.setObjectName("deltaTimeBox")
        self.horizontalLayout.addWidget(self.deltaTimeBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.controlButton = QtWidgets.QPushButton(self.centralwidget)
        self.controlButton.setObjectName("controlButton")
        self.horizontalLayout.addWidget(self.controlButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openAction = QtWidgets.QAction(MainWindow)
        self.openAction.setObjectName("openAction")
        self.saveAsAction = QtWidgets.QAction(MainWindow)
        self.saveAsAction.setObjectName("saveAsAction")
        self.saveAction = QtWidgets.QAction(MainWindow)
        self.saveAction.setObjectName("saveAction")
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.saveAsAction)
        self.menu.addAction(self.saveAction)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Небесная механика"))
        self.label.setText(_translate("MainWindow", "Шаг симуляции (в с): "))
        self.controlButton.setText(_translate("MainWindow", "Остановить"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.openAction.setText(_translate("MainWindow", "Загрузить симуляцию..."))
        self.saveAsAction.setText(_translate("MainWindow", "Сохранить симуляцию как..."))
        self.saveAction.setText(_translate("MainWindow", "Сохранить симуляцию"))

from pyqtgraph import PlotWidget
