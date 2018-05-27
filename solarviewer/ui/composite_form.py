# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'composite_form.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_CompositeForm(object):
    def setupUi(self, CompositeForm):
        CompositeForm.setObjectName("CompositeForm")
        CompositeForm.resize(367, 102)
        self.formLayout = QtWidgets.QFormLayout(CompositeForm)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(CompositeForm)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.order = QtWidgets.QSpinBox(CompositeForm)
        self.order.setMaximum(100)
        self.order.setObjectName("order")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.order)
        self.label = QtWidgets.QLabel(CompositeForm)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.alpha_spin = QtWidgets.QSpinBox(CompositeForm)
        self.alpha_spin.setMaximum(100)
        self.alpha_spin.setObjectName("alpha_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.alpha_spin)
        self.levels_check = QtWidgets.QCheckBox(CompositeForm)
        self.levels_check.setObjectName("levels_check")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.levels_check)
        self.levels_list = QtWidgets.QLineEdit(CompositeForm)
        self.levels_list.setEnabled(False)
        self.levels_list.setClearButtonEnabled(True)
        self.levels_list.setObjectName("levels_list")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.levels_list)

        self.retranslateUi(CompositeForm)
        self.levels_check.toggled['bool'].connect(self.levels_list.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(CompositeForm)

    def retranslateUi(self, CompositeForm):
        _translate = QtCore.QCoreApplication.translate
        CompositeForm.setWindowTitle(_translate("CompositeForm", "Form"))
        self.label_2.setText(_translate("CompositeForm", "Z-Order:"))
        self.label.setText(_translate("CompositeForm", "Alpha:"))
        self.alpha_spin.setSuffix(_translate("CompositeForm", "%"))
        self.levels_check.setText(_translate("CompositeForm", "Levels (in %):"))
        self.levels_list.setInputMask(_translate("CompositeForm", "00 00 00 00 00 00 00 00 00 00 00 00"))
        self.levels_list.setText(_translate("CompositeForm", "10 20 30 40 50 60 70 80 90   "))

