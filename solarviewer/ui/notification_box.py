# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notification_box.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NotificationBox(object):
    def setupUi(self, NotificationBox):
        NotificationBox.setObjectName("NotificationBox")
        NotificationBox.resize(400, 38)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        NotificationBox.setPalette(palette)
        NotificationBox.setAutoFillBackground(True)
        NotificationBox.setFrameShape(QtWidgets.QFrame.Panel)
        NotificationBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(NotificationBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message_label = QtWidgets.QLabel(NotificationBox)
        self.message_label.setObjectName("message_label")
        self.horizontalLayout.addWidget(self.message_label)
        self.close_button = QtWidgets.QToolButton(NotificationBox)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)

        self.retranslateUi(NotificationBox)
        self.close_button.clicked.connect(NotificationBox.hide)
        QtCore.QMetaObject.connectSlotsByName(NotificationBox)

    def retranslateUi(self, NotificationBox):
        _translate = QtCore.QCoreApplication.translate
        NotificationBox.setWindowTitle(_translate("NotificationBox", "Frame"))
        self.message_label.setText(_translate("NotificationBox", "ERROR Message"))
        self.close_button.setText(_translate("NotificationBox", "X"))

