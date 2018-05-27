# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wavelet.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Wavelet(object):
    def setupUi(self, Wavelet):
        Wavelet.setObjectName("Wavelet")
        Wavelet.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Wavelet)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Wavelet)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.wavelet_family_combo = QtWidgets.QComboBox(self.groupBox)
        self.wavelet_family_combo.setObjectName("wavelet_family_combo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.wavelet_family_combo)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.wavelet_combo = QtWidgets.QComboBox(self.groupBox)
        self.wavelet_combo.setObjectName("wavelet_combo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.wavelet_combo)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.level_spin = QtWidgets.QSpinBox(self.groupBox)
        self.level_spin.setObjectName("level_spin")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.level_spin)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Wavelet)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sigma_spin = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.sigma_spin.setObjectName("sigma_spin")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sigma_spin)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Wavelet)
        QtCore.QMetaObject.connectSlotsByName(Wavelet)

    def retranslateUi(self, Wavelet):
        _translate = QtCore.QCoreApplication.translate
        Wavelet.setWindowTitle(_translate("Wavelet", "Form"))
        self.groupBox.setTitle(_translate("Wavelet", "Wavelet Settings"))
        self.label.setText(_translate("Wavelet", "Wavelet Family:"))
        self.label_3.setText(_translate("Wavelet", "Wavelet:"))
        self.label_4.setText(_translate("Wavelet", "Level:"))
        self.groupBox_2.setTitle(_translate("Wavelet", "Denoising"))
        self.label_2.setText(_translate("Wavelet", "Sigma:"))
