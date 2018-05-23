# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rotate.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Rotate(object):
    def setupUi(self, Rotate):
        Rotate.setObjectName("Rotate")
        Rotate.resize(216, 51)
        self.formLayout = QtWidgets.QFormLayout(Rotate)
        self.formLayout.setObjectName("formLayout")
        self.angle_spin = QtWidgets.QDoubleSpinBox(Rotate)
        self.angle_spin.setMinimum(-360.0)
        self.angle_spin.setMaximum(360.0)
        self.angle_spin.setObjectName("angle_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.angle_spin)
        self.label = QtWidgets.QLabel(Rotate)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.retranslateUi(Rotate)
        QtCore.QMetaObject.connectSlotsByName(Rotate)

    def retranslateUi(self, Rotate):
        _translate = QtCore.QCoreApplication.translate
        Rotate.setWindowTitle(_translate("Rotate", "Form"))
        self.angle_spin.setSuffix(_translate("Rotate", "°"))
        self.label.setText(_translate("Rotate", "Angle:"))
