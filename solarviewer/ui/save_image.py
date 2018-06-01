# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'save_image.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SaveImage(object):
    def setupUi(self, SaveImage):
        SaveImage.setObjectName("SaveImage")
        SaveImage.resize(394, 143)
        self.verticalLayout = QtWidgets.QVBoxLayout(SaveImage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(SaveImage)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_path = QtWidgets.QLineEdit(self.widget_2)
        self.file_path.setEnabled(False)
        self.file_path.setObjectName("file_path")
        self.horizontalLayout.addWidget(self.file_path)
        self.file_select = QtWidgets.QPushButton(self.widget_2)
        self.file_select.setObjectName("file_select")
        self.horizontalLayout.addWidget(self.file_select)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.widget_2)
        self.dpi_spin = QtWidgets.QSpinBox(self.widget)
        self.dpi_spin.setMaximum(10000)
        self.dpi_spin.setObjectName("dpi_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dpi_spin)
        self.dpi_check = QtWidgets.QCheckBox(self.widget)
        self.dpi_check.setChecked(False)
        self.dpi_check.setObjectName("dpi_check")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.dpi_check)
        self.transparent_check = QtWidgets.QCheckBox(self.widget)
        self.transparent_check.setText("")
        self.transparent_check.setObjectName("transparent_check")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.transparent_check)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.verticalLayout.addWidget(self.widget)
        self.button_box = QtWidgets.QDialogButtonBox(SaveImage)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(SaveImage)
        self.button_box.accepted.connect(SaveImage.accept)
        self.button_box.rejected.connect(SaveImage.reject)
        self.dpi_check.clicked['bool'].connect(self.dpi_spin.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(SaveImage)

    def retranslateUi(self, SaveImage):
        _translate = QtCore.QCoreApplication.translate
        SaveImage.setWindowTitle(_translate("SaveImage", "Dialog"))
        self.label.setText(_translate("SaveImage", "Filepath:"))
        self.file_select.setText(_translate("SaveImage", "..."))
        self.dpi_check.setText(_translate("SaveImage", "DPI:"))
        self.label_2.setText(_translate("SaveImage", "Transparent Background"))

