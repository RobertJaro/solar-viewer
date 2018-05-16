# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fft.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(484, 403)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox_2)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.contrast_none = QtWidgets.QRadioButton(self.groupBox)
        self.contrast_none.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.contrast_none.setObjectName("contrast_none")
        self.verticalLayout_3.addWidget(self.contrast_none)
        self.contrast_min_max = QtWidgets.QRadioButton(self.groupBox)
        self.contrast_min_max.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.contrast_min_max.setObjectName("contrast_min_max")
        self.verticalLayout_3.addWidget(self.contrast_min_max)
        self.contrast_average = QtWidgets.QRadioButton(self.groupBox)
        self.contrast_average.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.contrast_average.setObjectName("contrast_average")
        self.verticalLayout_3.addWidget(self.contrast_average)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.dockWidgetContents)
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "DockWidget"))
        self.groupBox_2.setTitle(_translate("DockWidget", "Filter Parameters"))
        self.checkBox.setText(_translate("DockWidget", "Highpass"))
        self.checkBox_2.setText(_translate("DockWidget", "Lowpass"))
        self.groupBox.setTitle(_translate("DockWidget", "Contrast Adjustment"))
        self.contrast_none.setText(_translate("DockWidget", "None"))
        self.contrast_min_max.setText(_translate("DockWidget", "Min/Max"))
        self.contrast_average.setText(_translate("DockWidget", "Average"))

