# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fft.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FFT(object):
    def setupUi(self, FFT):
        FFT.setObjectName("FFT")
        FFT.resize(382, 522)
        self.verticalLayout = QtWidgets.QVBoxLayout(FFT)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(FFT)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.highpass_check = QtWidgets.QCheckBox(self.groupBox_2)
        self.highpass_check.setChecked(True)
        self.highpass_check.setObjectName("highpass_check")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.highpass_check)
        self.highpass_spin = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.highpass_spin.setDecimals(3)
        self.highpass_spin.setSingleStep(0.1)
        self.highpass_spin.setProperty("value", 0.1)
        self.highpass_spin.setObjectName("highpass_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.highpass_spin)
        self.lowpass_check = QtWidgets.QCheckBox(self.groupBox_2)
        self.lowpass_check.setObjectName("lowpass_check")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lowpass_check)
        self.lowpass_spin = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.lowpass_spin.setDecimals(3)
        self.lowpass_spin.setSingleStep(0.1)
        self.lowpass_spin.setProperty("value", 70.0)
        self.lowpass_spin.setObjectName("lowpass_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lowpass_spin)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(FFT)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.ideal_radio = QtWidgets.QRadioButton(self.groupBox)
        self.ideal_radio.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ideal_radio.setObjectName("ideal_radio")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ideal_radio)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.butter_order_spin = QtWidgets.QSpinBox(self.groupBox)
        self.butter_order_spin.setProperty("value", 2)
        self.butter_order_spin.setObjectName("butter_order_spin")
        self.horizontalLayout_2.addWidget(self.butter_order_spin)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.butter_radio = QtWidgets.QRadioButton(self.groupBox)
        self.butter_radio.setChecked(True)
        self.butter_radio.setObjectName("butter_radio")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.butter_radio)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(FFT)
        QtCore.QMetaObject.connectSlotsByName(FFT)

    def retranslateUi(self, FFT):
        _translate = QtCore.QCoreApplication.translate
        FFT.setWindowTitle(_translate("FFT", "Form"))
        self.groupBox_2.setTitle(_translate("FFT", "Filter Parameters"))
        self.highpass_check.setText(_translate("FFT", "Highpass"))
        self.highpass_spin.setSuffix(_translate("FFT", "%"))
        self.lowpass_check.setText(_translate("FFT", "Lowpass"))
        self.lowpass_spin.setSuffix(_translate("FFT", "%"))
        self.groupBox.setTitle(_translate("FFT", "Filter"))
        self.ideal_radio.setText(_translate("FFT", "Ideal Filter"))
        self.label.setText(_translate("FFT", "Order:"))
        self.butter_radio.setText(_translate("FFT", "Butterworth Fitler"))

