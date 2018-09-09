# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ndcube_plot_settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NDCubePlotSettings(object):
    def setupUi(self, NDCubePlotSettings):
        NDCubePlotSettings.setObjectName("NDCubePlotSettings")
        NDCubePlotSettings.resize(427, 319)
        self.verticalLayout = QtWidgets.QVBoxLayout(NDCubePlotSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_axes = QtWidgets.QGroupBox(NDCubePlotSettings)
        self.image_axes.setCheckable(False)
        self.image_axes.setObjectName("image_axes")
        self.formLayout = QtWidgets.QFormLayout(self.image_axes)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.image_axes)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.xaxis = QtWidgets.QComboBox(self.image_axes)
        self.xaxis.setObjectName("xaxis")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.xaxis)
        self.label_2 = QtWidgets.QLabel(self.image_axes)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.yaxis = QtWidgets.QComboBox(self.image_axes)
        self.yaxis.setObjectName("yaxis")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.yaxis)
        self.verticalLayout.addWidget(self.image_axes)

        self.retranslateUi(NDCubePlotSettings)
        QtCore.QMetaObject.connectSlotsByName(NDCubePlotSettings)

    def retranslateUi(self, NDCubePlotSettings):
        _translate = QtCore.QCoreApplication.translate
        NDCubePlotSettings.setWindowTitle(_translate("NDCubePlotSettings", "Form"))
        self.image_axes.setTitle(_translate("NDCubePlotSettings", "Image Axes"))
        self.label.setText(_translate("NDCubePlotSettings", "X-Axis:"))
        self.label_2.setText(_translate("NDCubePlotSettings", "Y-Axis:"))

