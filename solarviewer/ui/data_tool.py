# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_tool.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_DataTool(object):
    def setupUi(self, DataTool):
        DataTool.setObjectName("DataTool")
        DataTool.resize(836, 681)
        self.vboxlayout = QtWidgets.QVBoxLayout(DataTool)
        self.vboxlayout.setObjectName("vboxlayout")
        self.message_box = NotificationBox(DataTool)
        self.message_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message_box.setObjectName("message_box")
        self.vboxlayout.addWidget(self.message_box)
        self.scrollArea = QtWidgets.QScrollArea(DataTool)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.content = QtWidgets.QWidget()
        self.content.setGeometry(QtCore.QRect(0, 0, 818, 600))
        self.content.setObjectName("content")
        self.scrollArea.setWidget(self.content)
        self.vboxlayout.addWidget(self.scrollArea)
        self.widget = QtWidgets.QWidget(DataTool)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_box = QtWidgets.QDialogButtonBox(self.widget)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Apply)
        self.button_box.setObjectName("button_box")
        self.verticalLayout_2.addWidget(self.button_box)
        self.vboxlayout.addWidget(self.widget)

        self.retranslateUi(DataTool)
        QtCore.QMetaObject.connectSlotsByName(DataTool)

    def retranslateUi(self, DataTool):
        _translate = QtCore.QCoreApplication.translate
        DataTool.setWindowTitle(_translate("DataTool", "Form"))


from solarviewer.ui.util import NotificationBox
