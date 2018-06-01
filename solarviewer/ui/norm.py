# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'norm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Norm(object):
    def setupUi(self, Norm):
        Norm.setObjectName("Norm")
        Norm.resize(400, 107)
        self.layout = QtWidgets.QFormLayout(Norm)
        self.layout.setObjectName("layout")
        self.norm_combo = QtWidgets.QComboBox(Norm)
        self.norm_combo.setObjectName("norm_combo")
        self.layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.norm_combo)
        self.label = QtWidgets.QLabel(Norm)
        self.label.setObjectName("label")
        self.layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.retranslateUi(Norm)
        QtCore.QMetaObject.connectSlotsByName(Norm)

    def retranslateUi(self, Norm):
        _translate = QtCore.QCoreApplication.translate
        Norm.setWindowTitle(_translate("Norm", "Form"))
        self.label.setText(_translate("Norm", "Normalization:"))

