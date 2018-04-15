# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contrast.ui'
#
# Created by: PyQt5 UI code generator 5.6
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
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pushButton_2)
        self.verticalLayout.addWidget(self.groupBox)
        self.color_clipped = QtWidgets.QGroupBox(Contrast)
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

        self.retranslateUi(Contrast)
        self.color_clipped.clicked['bool'].connect(self.checkBox.setEnabled)
        self.color_clipped.clicked['bool'].connect(self.checkBox_2.setEnabled)
        self.color_clipped.clicked['bool'].connect(self.color_above.setEnabled)
        self.color_clipped.clicked['bool'].connect(self.color_below.setEnabled)
        self.histo_button.clicked['bool'].connect(self.histo_plot.setVisible)
        QtCore.QMetaObject.connectSlotsByName(Contrast)

    def retranslateUi(self, Contrast):
        _translate = QtCore.QCoreApplication.translate
        Contrast.setWindowTitle(_translate("Contrast", "Form"))
        self.histo_button.setText(_translate("Contrast", ">>Histogram"))
        self.groupBox.setTitle(_translate("Contrast", "Settings"))
        self.label.setText(_translate("Contrast", "Min:"))
        self.label_2.setText(_translate("Contrast", "Max:"))
        self.pushButton.setText(_translate("Contrast", "Adjust Min/Max"))
        self.pushButton_2.setText(_translate("Contrast", "Adjust Average"))
        self.color_clipped.setTitle(_translate("Contrast", "Color Clipped Values"))
        self.checkBox.setText(_translate("Contrast", "Over"))
        self.checkBox_2.setText(_translate("Contrast", "Under"))


from solarviewer.ui.util import QColorButton
