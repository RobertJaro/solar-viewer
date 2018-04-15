# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cmap.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Colormap(object):
    def setupUi(self, Colormap):
        Colormap.setObjectName("Colormap")
        Colormap.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Colormap)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Colormap)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cmap_combo = QtWidgets.QComboBox(self.groupBox)
        self.cmap_combo.setObjectName("cmap_combo")
        self.verticalLayout_2.addWidget(self.cmap_combo)
        self.verticalLayout.addWidget(self.groupBox)
        self.color_clipped = QtWidgets.QGroupBox(Colormap)
        self.color_clipped.setFlat(False)
        self.color_clipped.setCheckable(True)
        self.color_clipped.setObjectName("color_clipped")
        self.formLayout_2 = QtWidgets.QFormLayout(self.color_clipped)
        self.formLayout_2.setObjectName("formLayout_2")
        self.checkBox = QtWidgets.QCheckBox(self.color_clipped)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.color_clipped)
        self.checkBox_2.setChecked(False)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox_2)
        self.color_above = QColorButton(self.color_clipped)
        self.color_above.setEnabled(True)
        self.color_above.setText("")
        self.color_above.setObjectName("color_above")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.color_above)
        self.color_below = QColorButton(self.color_clipped)
        self.color_below.setText("")
        self.color_below.setObjectName("color_below")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.color_below)
        self.verticalLayout.addWidget(self.color_clipped)

        self.retranslateUi(Colormap)
        QtCore.QMetaObject.connectSlotsByName(Colormap)

    def retranslateUi(self, Colormap):
        _translate = QtCore.QCoreApplication.translate
        Colormap.setWindowTitle(_translate("Colormap", "Form"))
        self.groupBox.setTitle(_translate("Colormap", "Select Colormap"))
        self.color_clipped.setTitle(_translate("Colormap", "Color Clipped Values"))
        self.checkBox.setText(_translate("Colormap", "Over"))
        self.checkBox_2.setText(_translate("Colormap", "Under"))


from solarviewer.ui.util import QColorButton
