# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result_tab.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_ResultTab(object):
    def setupUi(self, ResultTab):
        ResultTab.setObjectName("ResultTab")
        ResultTab.resize(1041, 599)
        ResultTab.setMinimumSize(QtCore.QSize(0, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(ResultTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progress = QtWidgets.QProgressBar(ResultTab)
        self.progress.setMaximum(0)
        self.progress.setProperty("value", -1)
        self.progress.setTextVisible(False)
        self.progress.setObjectName("progress")
        self.verticalLayout.addWidget(self.progress)
        self.table = QtWidgets.QTableWidget(ResultTab)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(ResultTab)
        QtCore.QMetaObject.connectSlotsByName(ResultTab)

    def retranslateUi(self, ResultTab):
        _translate = QtCore.QCoreApplication.translate
        ResultTab.setWindowTitle(_translate("ResultTab", "Form"))
