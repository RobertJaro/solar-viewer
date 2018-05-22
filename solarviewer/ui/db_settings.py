# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'db_settings.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_DBSettings(object):
    def setupUi(self, DBSettings):
        DBSettings.setObjectName("DBSettings")
        DBSettings.resize(400, 143)
        self.verticalLayout = QtWidgets.QVBoxLayout(DBSettings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(DBSettings)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.url = QtWidgets.QLineEdit(self.widget)
        self.url.setObjectName("url")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.url)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_path = QtWidgets.QLineEdit(self.widget_2)
        self.file_path.setEnabled(False)
        self.file_path.setObjectName("file_path")
        self.horizontalLayout.addWidget(self.file_path)
        self.file_select = QtWidgets.QPushButton(self.widget_2)
        self.file_select.setObjectName("file_select")
        self.horizontalLayout.addWidget(self.file_select)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.widget_2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(DBSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DBSettings)
        self.buttonBox.accepted.connect(DBSettings.accept)
        self.buttonBox.rejected.connect(DBSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DBSettings)

    def retranslateUi(self, DBSettings):
        _translate = QtCore.QCoreApplication.translate
        DBSettings.setWindowTitle(_translate("DBSettings", "Change Database Settings"))
        self.label.setText(_translate("DBSettings", "DB-URL:"))
        self.file_select.setText(_translate("DBSettings", "..."))
        self.label_2.setText(_translate("DBSettings", "Download Directory:"))
