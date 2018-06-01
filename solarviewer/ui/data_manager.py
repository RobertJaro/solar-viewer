# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_manager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataManager(object):
    def setupUi(self, DataManager):
        DataManager.setObjectName("DataManager")
        DataManager.resize(650, 622)
        self.verticalLayout = QtWidgets.QVBoxLayout(DataManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.data_table = QtWidgets.QTableView(DataManager)
        self.data_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_table.setSortingEnabled(True)
        self.data_table.setObjectName("data_table")
        self.verticalLayout.addWidget(self.data_table)
        self.widget = QtWidgets.QWidget(DataManager)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_button = QtWidgets.QPushButton(self.widget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.remove_button = QtWidgets.QPushButton(self.widget)
        self.remove_button.setObjectName("remove_button")
        self.horizontalLayout.addWidget(self.remove_button)
        self.open_button = QtWidgets.QPushButton(self.widget)
        self.open_button.setObjectName("open_button")
        self.horizontalLayout.addWidget(self.open_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.filter_button = QtWidgets.QPushButton(self.widget)
        self.filter_button.setObjectName("filter_button")
        self.horizontalLayout.addWidget(self.filter_button)
        self.refresh_button = QtWidgets.QPushButton(self.widget)
        self.refresh_button.setObjectName("refresh_button")
        self.horizontalLayout.addWidget(self.refresh_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(DataManager)
        QtCore.QMetaObject.connectSlotsByName(DataManager)

    def retranslateUi(self, DataManager):
        _translate = QtCore.QCoreApplication.translate
        DataManager.setWindowTitle(_translate("DataManager", "Form"))
        self.add_button.setText(_translate("DataManager", "Add"))
        self.remove_button.setText(_translate("DataManager", "Remove"))
        self.open_button.setText(_translate("DataManager", "Open"))
        self.filter_button.setText(_translate("DataManager", "Set Filter"))
        self.refresh_button.setText(_translate("DataManager", "Refresh"))

