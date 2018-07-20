# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_callisto.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QueryCallisto(object):
    def setupUi(self, QueryCallisto):
        QueryCallisto.setObjectName("QueryCallisto")
        QueryCallisto.resize(297, 137)
        self.verticalLayout = QtWidgets.QVBoxLayout(QueryCallisto)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(QueryCallisto)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.instrument = QtWidgets.QComboBox(self.widget)
        self.instrument.setEditable(True)
        self.instrument.setObjectName("instrument")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.instrument)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.start_time = QtWidgets.QDateTimeEdit(self.widget)
        self.start_time.setCalendarPopup(True)
        self.start_time.setObjectName("start_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.start_time)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.end_time = QtWidgets.QDateTimeEdit(self.widget)
        self.end_time.setCalendarPopup(True)
        self.end_time.setObjectName("end_time")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.end_time)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(QueryCallisto)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QueryCallisto)
        self.buttonBox.accepted.connect(QueryCallisto.accept)
        self.buttonBox.rejected.connect(QueryCallisto.reject)
        QtCore.QMetaObject.connectSlotsByName(QueryCallisto)

    def retranslateUi(self, QueryCallisto):
        _translate = QtCore.QCoreApplication.translate
        QueryCallisto.setWindowTitle(_translate("QueryCallisto", "Query Callisto Spectrogram"))
        self.label.setText(_translate("QueryCallisto", "Instrument:"))
        self.label_2.setText(_translate("QueryCallisto", "Start:"))
        self.start_time.setDisplayFormat(_translate("QueryCallisto", "yyyy-MM-ddThh:mm"))
        self.label_3.setText(_translate("QueryCallisto", "End:"))
        self.end_time.setDisplayFormat(_translate("QueryCallisto", "yyyy-MM-ddThh:mm"))

