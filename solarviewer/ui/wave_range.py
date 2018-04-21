# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wave_range.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_WaveRange(object):
    def setupUi(self, WaveRange):
        WaveRange.setObjectName("WaveRange")
        WaveRange.resize(157, 44)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WaveRange)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.from_spin = QtWidgets.QDoubleSpinBox(WaveRange)
        self.from_spin.setObjectName("from_spin")
        self.horizontalLayout.addWidget(self.from_spin)
        self.label = QtWidgets.QLabel(WaveRange)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.to_spin = QtWidgets.QDoubleSpinBox(WaveRange)
        self.to_spin.setObjectName("to_spin")
        self.horizontalLayout.addWidget(self.to_spin)

        self.retranslateUi(WaveRange)
        QtCore.QMetaObject.connectSlotsByName(WaveRange)

    def retranslateUi(self, WaveRange):
        _translate = QtCore.QCoreApplication.translate
        WaveRange.setWindowTitle(_translate("WaveRange", "Form"))
        self.label.setText(_translate("WaveRange", "-"))
