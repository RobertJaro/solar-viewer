# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_tool.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_DataTool(object):
    def setupUi(self, DataTool):
        DataTool.setObjectName("DataTool")
        DataTool.resize(836, 681)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataTool)
        self.verticalLayout.setObjectName("verticalLayout")
        self.content = QtWidgets.QWidget(DataTool)
        self.content.setObjectName("content")
        self.verticalLayout.addWidget(self.content)
        self.button_box = QtWidgets.QDialogButtonBox(DataTool)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(DataTool)
        QtCore.QMetaObject.connectSlotsByName(DataTool)

    def retranslateUi(self, DataTool):
        _translate = QtCore.QCoreApplication.translate
        DataTool.setWindowTitle(_translate("DataTool", "Form"))

