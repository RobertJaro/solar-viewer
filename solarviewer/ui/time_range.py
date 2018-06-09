# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_range.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_TimeRange(object):
    def setupUi(self, TimeRange):
        TimeRange.setObjectName("TimeRange")
        TimeRange.resize(299, 22)
        self.horizontalLayout = QtWidgets.QHBoxLayout(TimeRange)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.from_time = QtWidgets.QDateTimeEdit(TimeRange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.from_time.sizePolicy().hasHeightForWidth())
        self.from_time.setSizePolicy(sizePolicy)
        self.from_time.setCalendarPopup(True)
        self.from_time.setObjectName("from_time")
        self.horizontalLayout.addWidget(self.from_time)
        self.label = QtWidgets.QLabel(TimeRange)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.to_time = QtWidgets.QDateTimeEdit(TimeRange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.to_time.sizePolicy().hasHeightForWidth())
        self.to_time.setSizePolicy(sizePolicy)
        self.to_time.setCalendarPopup(True)
        self.to_time.setObjectName("to_time")
        self.horizontalLayout.addWidget(self.to_time)

        self.retranslateUi(TimeRange)
        QtCore.QMetaObject.connectSlotsByName(TimeRange)

    def retranslateUi(self, TimeRange):
        _translate = QtCore.QCoreApplication.translate
        TimeRange.setWindowTitle(_translate("TimeRange", "Form"))
        self.from_time.setDisplayFormat(_translate("TimeRange", "yyyy-MM-ddThh:mm"))
        self.label.setText(_translate("TimeRange", "-"))
        self.to_time.setDisplayFormat(_translate("TimeRange", "yyyy-MM-ddThh:mm"))
