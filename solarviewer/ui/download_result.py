# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_result.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_DownloadResult(object):
    def setupUi(self, DownloadResult):
        DownloadResult.setObjectName("DownloadResult")
        DownloadResult.resize(617, 416)
        self.verticalLayout = QtWidgets.QVBoxLayout(DownloadResult)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(DownloadResult)
        self.tabs.setTabsClosable(True)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabs)
        self.widget = QtWidgets.QWidget(DownloadResult)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(392, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.download_button = QtWidgets.QPushButton(self.widget)
        self.download_button.setAutoDefault(True)
        self.download_button.setDefault(True)
        self.download_button.setObjectName("download_button")
        self.horizontalLayout.addWidget(self.download_button)
        self.open_button = QtWidgets.QPushButton(self.widget)
        self.open_button.setObjectName("open_button")
        self.horizontalLayout.addWidget(self.open_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(DownloadResult)
        QtCore.QMetaObject.connectSlotsByName(DownloadResult)

    def retranslateUi(self, DownloadResult):
        _translate = QtCore.QCoreApplication.translate
        DownloadResult.setWindowTitle(_translate("DownloadResult", "Form"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("DownloadResult", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("DownloadResult", "Tab 2"))
        self.download_button.setText(_translate("DownloadResult", "Download"))
        self.open_button.setText(_translate("DownloadResult", "Open"))
