# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plot_settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_PlotSettings(object):
    def setupUi(self, PlotSettings):
        PlotSettings.setObjectName("PlotSettings")
        PlotSettings.resize(273, 265)
        self.verticalLayout = QtWidgets.QVBoxLayout(PlotSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(PlotSettings)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.color_bar = QtWidgets.QCheckBox(self.groupBox)
        self.color_bar.setObjectName("color_bar")
        self.verticalLayout_2.addWidget(self.color_bar)
        self.grid = QtWidgets.QCheckBox(self.groupBox)
        self.grid.setObjectName("grid")
        self.verticalLayout_2.addWidget(self.grid)
        self.limb = QtWidgets.QCheckBox(self.groupBox)
        self.limb.setObjectName("limb")
        self.verticalLayout_2.addWidget(self.limb)
        self.verticalLayout.addWidget(self.groupBox)
        self.contours = QtWidgets.QGroupBox(PlotSettings)
        self.contours.setCheckable(True)
        self.contours.setObjectName("contours")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.contours)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.contours_list = QtWidgets.QLineEdit(self.contours)
        self.contours_list.setClearButtonEnabled(True)
        self.contours_list.setObjectName("contours_list")
        self.verticalLayout_3.addWidget(self.contours_list)
        self.verticalLayout.addWidget(self.contours)

        self.retranslateUi(PlotSettings)
        QtCore.QMetaObject.connectSlotsByName(PlotSettings)

    def retranslateUi(self, PlotSettings):
        _translate = QtCore.QCoreApplication.translate
        PlotSettings.setWindowTitle(_translate("PlotSettings", "Form"))
        self.groupBox.setTitle(_translate("PlotSettings", "Display Settings"))
        self.color_bar.setText(_translate("PlotSettings", "Colorbar"))
        self.grid.setText(_translate("PlotSettings", "Grid"))
        self.limb.setText(_translate("PlotSettings", "Limb"))
        self.contours.setTitle(_translate("PlotSettings", "Contours"))
        self.contours_list.setInputMask(_translate("PlotSettings", "00 00 00 00 00 00 00 00 00 00 00 00"))
        self.contours_list.setText(_translate("PlotSettings", "10 20 30 40 50 60 70 80 90   "))
