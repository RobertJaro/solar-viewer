# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Plot(object):
    def setupUi(self, Plot):
        Plot.setObjectName("Plot")
        Plot.resize(734, 536)
        self.verticalLayout = QtWidgets.QVBoxLayout(Plot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progress = QtWidgets.QProgressBar(Plot)
        self.progress.setMaximum(0)
        self.progress.setProperty("value", 0)
        self.progress.setTextVisible(False)
        self.progress.setInvertedAppearance(False)
        self.progress.setObjectName("progress")
        self.verticalLayout.addWidget(self.progress, 0, QtCore.Qt.AlignVCenter)

        self.retranslateUi(Plot)
        QtCore.QMetaObject.connectSlotsByName(Plot)

    def retranslateUi(self, Plot):
        _translate = QtCore.QCoreApplication.translate
        Plot.setWindowTitle(_translate("Plot", "Form"))

