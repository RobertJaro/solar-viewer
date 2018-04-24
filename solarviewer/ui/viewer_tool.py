# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewer_tool.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_ViewerTool(object):
    def setupUi(self, ViewerTool):
        ViewerTool.setObjectName("ViewerTool")
        ViewerTool.resize(836, 681)
        self.vboxlayout = QtWidgets.QVBoxLayout(ViewerTool)
        self.vboxlayout.setObjectName("vboxlayout")
        self.scrollArea = QtWidgets.QScrollArea(ViewerTool)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.content = QtWidgets.QWidget()
        self.content.setGeometry(QtCore.QRect(0, 0, 814, 659))
        self.content.setObjectName("content")
        self.scrollArea.setWidget(self.content)
        self.vboxlayout.addWidget(self.scrollArea)

        self.retranslateUi(ViewerTool)
        QtCore.QMetaObject.connectSlotsByName(ViewerTool)

    def retranslateUi(self, ViewerTool):
        _translate = QtCore.QCoreApplication.translate
        ViewerTool.setWindowTitle(_translate("ViewerTool", "Form"))
