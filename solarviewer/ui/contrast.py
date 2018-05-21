# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contrast.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Contrast(object):
    def setupUi(self, Contrast):
        Contrast.setObjectName("Contrast")
        Contrast.resize(563, 756)
        self.verticalLayout = QtWidgets.QVBoxLayout(Contrast)
        self.verticalLayout.setObjectName("verticalLayout")
        self.histo_button = QtWidgets.QPushButton(Contrast)
        self.histo_button.setCheckable(True)
        self.histo_button.setObjectName("histo_button")
        self.verticalLayout.addWidget(self.histo_button)
        self.histo_plot = QtWidgets.QFrame(Contrast)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histo_plot.sizePolicy().hasHeightForWidth())
        self.histo_plot.setSizePolicy(sizePolicy)
        self.histo_plot.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.histo_plot.setFrameShape(QtWidgets.QFrame.Box)
        self.histo_plot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.histo_plot.setObjectName("histo_plot")
        self.hist_layout = QtWidgets.QVBoxLayout(self.histo_plot)
        self.hist_layout.setContentsMargins(0, 0, 0, 0)
        self.hist_layout.setSpacing(0)
        self.hist_layout.setObjectName("hist_layout")
        self.verticalLayout.addWidget(self.histo_plot)
        self.groupBox = QtWidgets.QGroupBox(Contrast)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spin_min = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spin_min.setPrefix("")
        self.spin_min.setObjectName("spin_min")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_min)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spin_max = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spin_max.setObjectName("spin_max")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spin_max)
        self.min_max_button = QtWidgets.QPushButton(self.groupBox)
        self.min_max_button.setObjectName("min_max_button")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.min_max_button)
        self.average_button = QtWidgets.QPushButton(self.groupBox)
        self.average_button.setObjectName("average_button")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.average_button)
        self.peak_button = QtWidgets.QPushButton(self.groupBox)
        self.peak_button.setObjectName("peak_button")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.peak_button)
        self.verticalLayout.addWidget(self.groupBox)
        self.color_clipped = QtWidgets.QGroupBox(Contrast)
        self.color_clipped.setFlat(False)
        self.color_clipped.setCheckable(True)
        self.color_clipped.setObjectName("color_clipped")
        self.formLayout_2 = QtWidgets.QFormLayout(self.color_clipped)
        self.formLayout_2.setObjectName("formLayout_2")
        self.over_check = QtWidgets.QCheckBox(self.color_clipped)
        self.over_check.setChecked(False)
        self.over_check.setObjectName("over_check")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.over_check)
        self.under_check = QtWidgets.QCheckBox(self.color_clipped)
        self.under_check.setChecked(False)
        self.under_check.setObjectName("under_check")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.under_check)
        self.over_color = QColorButton(self.color_clipped)
        self.over_color.setEnabled(True)
        self.over_color.setText("")
        self.over_color.setObjectName("over_color")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.over_color)
        self.under_color = QColorButton(self.color_clipped)
        self.under_color.setText("")
        self.under_color.setObjectName("under_color")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.under_color)
        self.verticalLayout.addWidget(self.color_clipped)

        self.retranslateUi(Contrast)
        self.histo_button.clicked['bool'].connect(self.histo_plot.setVisible)
        QtCore.QMetaObject.connectSlotsByName(Contrast)

    def retranslateUi(self, Contrast):
        _translate = QtCore.QCoreApplication.translate
        Contrast.setWindowTitle(_translate("Contrast", "Form"))
        self.histo_button.setText(_translate("Contrast", ">>Histogram"))
        self.groupBox.setTitle(_translate("Contrast", "Settings"))
        self.label.setText(_translate("Contrast", "Min:"))
        self.label_2.setText(_translate("Contrast", "Max:"))
        self.min_max_button.setText(_translate("Contrast", "Adjust Min/Max"))
        self.average_button.setText(_translate("Contrast", "Adjust Average"))
        self.peak_button.setText(_translate("Contrast", "Adjust Peak"))
        self.color_clipped.setTitle(_translate("Contrast", "Color Clipped Values"))
        self.over_check.setText(_translate("Contrast", "Over"))
        self.under_check.setText(_translate("Contrast", "Under"))


from solarviewer.ui.util import QColorButton
