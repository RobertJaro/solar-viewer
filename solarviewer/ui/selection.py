# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selection.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Selection(object):
    def setupUi(self, Selection):
        Selection.setObjectName("Selection")
        Selection.resize(753, 542)
        self.verticalLayout = QtWidgets.QVBoxLayout(Selection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Selection)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.selection_table = QtWidgets.QTableWidget(self.groupBox)
        self.selection_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.selection_table.setObjectName("selection_table")
        self.selection_table.setColumnCount(3)
        self.selection_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.selection_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.selection_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.selection_table.setHorizontalHeaderItem(2, item)
        self.verticalLayout_2.addWidget(self.selection_table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.import_button = QtWidgets.QPushButton(self.groupBox)
        self.import_button.setObjectName("import_button")
        self.horizontalLayout.addWidget(self.import_button)
        self.export_button = QtWidgets.QPushButton(self.groupBox)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout.addWidget(self.export_button)
        self.clear_button = QtWidgets.QPushButton(self.groupBox)
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout.addWidget(self.clear_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Selection)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.marker_color = QColorButton(self.groupBox_2)
        self.marker_color.setEnabled(True)
        self.marker_color.setText("")
        self.marker_color.setObjectName("marker_color")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.marker_color)
        self.text_color = QColorButton(self.groupBox_2)
        self.text_color.setText("")
        self.text_color.setObjectName("text_color")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.text_color)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Selection)
        QtCore.QMetaObject.connectSlotsByName(Selection)

    def retranslateUi(self, Selection):
        _translate = QtCore.QCoreApplication.translate
        Selection.setWindowTitle(_translate("Selection", "Form"))
        self.groupBox.setTitle(_translate("Selection", "Selected Values"))
        item = self.selection_table.horizontalHeaderItem(0)
        item.setText(_translate("Selection", "X"))
        item = self.selection_table.horizontalHeaderItem(1)
        item.setText(_translate("Selection", "Y"))
        item = self.selection_table.horizontalHeaderItem(2)
        item.setText(_translate("Selection", "Value"))
        self.import_button.setText(_translate("Selection", "Import"))
        self.export_button.setText(_translate("Selection", "Export"))
        self.clear_button.setText(_translate("Selection", "Clear"))
        self.groupBox_2.setTitle(_translate("Selection", "Style"))
        self.label.setText(_translate("Selection", "Marker Colour:"))
        self.label_2.setText(_translate("Selection", "Text Colour:"))


from solarviewer.ui.util import QColorButton
