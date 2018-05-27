# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Download(object):
    def setupUi(self, Download):
        Download.setObjectName("Download")
        Download.resize(562, 733)
        self.verticalLayout = QtWidgets.QVBoxLayout(Download)
        self.verticalLayout.setObjectName("verticalLayout")
        self.message_box = NotificationBox(Download)
        self.message_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.message_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message_box.setObjectName("message_box")
        self.verticalLayout.addWidget(self.message_box)
        self.scrollArea = QtWidgets.QScrollArea(Download)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.content = QtWidgets.QWidget()
        self.content.setGeometry(QtCore.QRect(0, 0, 544, 652))
        self.content.setObjectName("content")
        self.content_layout = QtWidgets.QVBoxLayout(self.content)
        self.content_layout.setObjectName("content_layout")
        self.groupBox = QtWidgets.QGroupBox(self.content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.filter_combo = QtWidgets.QComboBox(self.groupBox)
        self.filter_combo.setObjectName("filter_combo")
        self.horizontalLayout_2.addWidget(self.filter_combo)
        self.add_filter_button = QtWidgets.QPushButton(self.groupBox)
        self.add_filter_button.setObjectName("add_filter_button")
        self.horizontalLayout_2.addWidget(self.add_filter_button)
        self.content_layout.addWidget(self.groupBox)
        self.scrollArea.setWidget(self.content)
        self.verticalLayout.addWidget(self.scrollArea)
        self.widget = QtWidgets.QWidget(Download)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.query_button = QtWidgets.QPushButton(self.widget)
        self.query_button.setAutoDefault(True)
        self.query_button.setDefault(True)
        self.query_button.setObjectName("query_button")
        self.horizontalLayout.addWidget(self.query_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Download)
        QtCore.QMetaObject.connectSlotsByName(Download)

    def retranslateUi(self, Download):
        _translate = QtCore.QCoreApplication.translate
        Download.setWindowTitle(_translate("Download", "Form"))
        self.groupBox.setTitle(_translate("Download", "Filter"))
        self.add_filter_button.setText(_translate("Download", "Add Filter"))
        self.query_button.setText(_translate("Download", "Query"))


from solarviewer.ui.util import NotificationBox
