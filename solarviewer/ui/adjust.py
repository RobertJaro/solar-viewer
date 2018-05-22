# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adjust.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_AdjustData(object):
    def setupUi(self, AdjustData):
        AdjustData.setObjectName("AdjustData")
        AdjustData.resize(376, 107)
        self.formLayout = QtWidgets.QFormLayout(AdjustData)
        self.formLayout.setObjectName("formLayout")
        self.clip_radio = QtWidgets.QRadioButton(AdjustData)
        self.clip_radio.setChecked(True)
        self.clip_radio.setObjectName("clip_radio")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.clip_radio)
        self.offset_radio = QtWidgets.QRadioButton(AdjustData)
        self.offset_radio.setObjectName("offset_radio")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.offset_radio)
        self.range_radio = QtWidgets.QRadioButton(AdjustData)
        self.range_radio.setObjectName("range_radio")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.range_radio)
        self.offset_spin = QtWidgets.QDoubleSpinBox(AdjustData)
        self.offset_spin.setEnabled(False)
        self.offset_spin.setMinimum(-10000.0)
        self.offset_spin.setMaximum(10000.0)
        self.offset_spin.setObjectName("offset_spin")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.offset_spin)
        self.range_widget = QtWidgets.QWidget(AdjustData)
        self.range_widget.setEnabled(False)
        self.range_widget.setObjectName("range_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.range_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.range_min_spin = QtWidgets.QDoubleSpinBox(self.range_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.range_min_spin.sizePolicy().hasHeightForWidth())
        self.range_min_spin.setSizePolicy(sizePolicy)
        self.range_min_spin.setObjectName("range_min_spin")
        self.horizontalLayout_2.addWidget(self.range_min_spin)
        self.label = QtWidgets.QLabel(self.range_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.range_max_spin = QtWidgets.QDoubleSpinBox(self.range_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.range_max_spin.sizePolicy().hasHeightForWidth())
        self.range_max_spin.setSizePolicy(sizePolicy)
        self.range_max_spin.setObjectName("range_max_spin")
        self.horizontalLayout_2.addWidget(self.range_max_spin)
        self.range_max_spin.raise_()
        self.range_min_spin.raise_()
        self.label.raise_()
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.range_widget)
        self.clip_spin = QtWidgets.QSpinBox(AdjustData)
        self.clip_spin.setObjectName("clip_spin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.clip_spin)

        self.retranslateUi(AdjustData)
        self.offset_radio.toggled['bool'].connect(self.offset_spin.setEnabled)
        self.range_radio.toggled['bool'].connect(self.range_widget.setEnabled)
        self.clip_radio.toggled['bool'].connect(self.clip_spin.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(AdjustData)

    def retranslateUi(self, AdjustData):
        _translate = QtCore.QCoreApplication.translate
        AdjustData.setWindowTitle(_translate("AdjustData", "Form"))
        self.clip_radio.setText(_translate("AdjustData", "Clip Below"))
        self.offset_radio.setText(_translate("AdjustData", "Shift to Value"))
        self.range_radio.setText(_translate("AdjustData", "Clip to Range"))
        self.label.setText(_translate("AdjustData", "-"))
