# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SpectraSettings(object):
    def setupUi(self, SpectraSettings):
        SpectraSettings.setObjectName("SpectraSettings")
        SpectraSettings.resize(375, 215)
        self.verticalLayout = QtWidgets.QVBoxLayout(SpectraSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(SpectraSettings)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.vmin_spin = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.vmin_spin.setEnabled(False)
        self.vmin_spin.setMinimum(-1000000.0)
        self.vmin_spin.setMaximum(1000000.0)
        self.vmin_spin.setObjectName("vmin_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.vmin_spin)
        self.vmax_spin = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.vmax_spin.setEnabled(False)
        self.vmax_spin.setMinimum(-1000000.0)
        self.vmax_spin.setMaximum(1000000.0)
        self.vmax_spin.setObjectName("vmax_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.vmax_spin)
        self.vmin_check = QtWidgets.QCheckBox(self.groupBox_2)
        self.vmin_check.setObjectName("vmin_check")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.vmin_check)
        self.vmax_check = QtWidgets.QCheckBox(self.groupBox_2)
        self.vmax_check.setObjectName("vmax_check")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.vmax_check)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(SpectraSettings)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.substract_background_check = QtWidgets.QCheckBox(self.groupBox)
        self.substract_background_check.setObjectName("substract_background_check")
        self.verticalLayout_2.addWidget(self.substract_background_check)
        self.linear_check = QtWidgets.QCheckBox(self.groupBox)
        self.linear_check.setObjectName("linear_check")
        self.verticalLayout_2.addWidget(self.linear_check)
        self.color_bar_check = QtWidgets.QCheckBox(self.groupBox)
        self.color_bar_check.setObjectName("color_bar_check")
        self.verticalLayout_2.addWidget(self.color_bar_check)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(SpectraSettings)
        self.vmin_check.toggled['bool'].connect(self.vmin_spin.setEnabled)
        self.vmax_check.toggled['bool'].connect(self.vmax_spin.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(SpectraSettings)

    def retranslateUi(self, SpectraSettings):
        _translate = QtCore.QCoreApplication.translate
        SpectraSettings.setWindowTitle(_translate("SpectraSettings", "Form"))
        self.groupBox_2.setTitle(_translate("SpectraSettings", "Clip Intensities"))
        self.vmin_check.setText(_translate("SpectraSettings", "Minimum:"))
        self.vmax_check.setText(_translate("SpectraSettings", "Maximum:"))
        self.groupBox.setTitle(_translate("SpectraSettings", "Display Settings"))
        self.substract_background_check.setText(_translate("SpectraSettings", "Substract Background"))
        self.linear_check.setText(_translate("SpectraSettings", "Linear"))
        self.color_bar_check.setText(_translate("SpectraSettings", "Colorbar"))

