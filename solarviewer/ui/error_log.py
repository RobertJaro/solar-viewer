# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error_log.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_ErrorLog(object):
    def setupUi(self, ErrorLog):
        ErrorLog.setObjectName("ErrorLog")
        ErrorLog.setEnabled(True)
        ErrorLog.resize(557, 446)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ErrorLog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.log = QtWidgets.QTextEdit(ErrorLog)
        self.log.setReadOnly(True)
        self.log.setObjectName("log")
        self.horizontalLayout.addWidget(self.log)

        self.retranslateUi(ErrorLog)
        QtCore.QMetaObject.connectSlotsByName(ErrorLog)

    def retranslateUi(self, ErrorLog):
        _translate = QtCore.QCoreApplication.translate
        ErrorLog.setWindowTitle(_translate("ErrorLog", "Form"))
