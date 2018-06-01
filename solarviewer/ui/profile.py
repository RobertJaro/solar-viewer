# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profile.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Profile(object):
    def setupUi(self, Profile):
        Profile.setObjectName("Profile")
        Profile.resize(465, 587)
        self.verticalLayout = QtWidgets.QVBoxLayout(Profile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.profile_box = QtWidgets.QFrame(Profile)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_box.sizePolicy().hasHeightForWidth())
        self.profile_box.setSizePolicy(sizePolicy)
        self.profile_box.setFrameShape(QtWidgets.QFrame.Box)
        self.profile_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.profile_box.setObjectName("profile_box")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.profile_box)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout.addWidget(self.profile_box)
        self.groupBox_2 = QtWidgets.QGroupBox(Profile)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.none_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.none_radio.setChecked(True)
        self.none_radio.setObjectName("none_radio")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.none_radio)
        self.horizontal_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.horizontal_radio.setObjectName("horizontal_radio")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.horizontal_radio)
        self.vertical_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.vertical_radio.setObjectName("vertical_radio")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.vertical_radio)
        self.free_radio = QtWidgets.QRadioButton(self.groupBox_2)
        self.free_radio.setObjectName("free_radio")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.free_radio)
        self.reset_button = QtWidgets.QPushButton(self.groupBox_2)
        self.reset_button.setEnabled(False)
        self.reset_button.setObjectName("reset_button")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.reset_button)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Profile)
        self.free_radio.toggled['bool'].connect(self.reset_button.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Profile)

    def retranslateUi(self, Profile):
        _translate = QtCore.QCoreApplication.translate
        Profile.setWindowTitle(_translate("Profile", "Form"))
        self.groupBox_2.setTitle(_translate("Profile", "Mode"))
        self.none_radio.setText(_translate("Profile", "None"))
        self.horizontal_radio.setText(_translate("Profile", "Horizontal"))
        self.vertical_radio.setText(_translate("Profile", "Vertical"))
        self.free_radio.setText(_translate("Profile", "Free Line"))
        self.reset_button.setText(_translate("Profile", "Reset Line"))

