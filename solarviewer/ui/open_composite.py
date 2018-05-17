# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_composite.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_OpenComposite(object):
    def setupUi(self, OpenComposite):
        OpenComposite.setObjectName("OpenComposite")
        OpenComposite.resize(526, 399)
        self.verticalLayout = QtWidgets.QVBoxLayout(OpenComposite)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(OpenComposite)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list = QtWidgets.QListView(OpenComposite)
        self.list.setObjectName("list")
        self.verticalLayout.addWidget(self.list)
        self.button_box = QtWidgets.QDialogButtonBox(OpenComposite)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(OpenComposite)
        self.button_box.accepted.connect(OpenComposite.accept)
        self.button_box.rejected.connect(OpenComposite.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenComposite)

    def retranslateUi(self, OpenComposite):
        _translate = QtCore.QCoreApplication.translate
        OpenComposite.setWindowTitle(_translate("OpenComposite", "Dialog"))
        self.label.setText(_translate("OpenComposite", "Select Maps:"))

