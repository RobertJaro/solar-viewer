# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wave_select.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_WaveSelect(object):
    def setupUi(self, WaveSelect):
        WaveSelect.setObjectName("WaveSelect")
        WaveSelect.resize(188, 44)
        self.horizontalLayout = QtWidgets.QHBoxLayout(WaveSelect)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wave_spin = QtWidgets.QDoubleSpinBox(WaveSelect)
        self.wave_spin.setMaximum(100000.0)
        self.wave_spin.setObjectName("wave_spin")
        self.horizontalLayout.addWidget(self.wave_spin)
        self.unit_combo = QtWidgets.QComboBox(WaveSelect)
        self.unit_combo.setObjectName("unit_combo")
        self.horizontalLayout.addWidget(self.unit_combo)

        self.retranslateUi(WaveSelect)
        QtCore.QMetaObject.connectSlotsByName(WaveSelect)

    def retranslateUi(self, WaveSelect):
        _translate = QtCore.QCoreApplication.translate
        WaveSelect.setWindowTitle(_translate("WaveSelect", "Form"))
