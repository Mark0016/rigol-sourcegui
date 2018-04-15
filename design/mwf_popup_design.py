'''This file is part of rigol-sourcegui.
   
   Copyright (c) 2017 Márk Vasi

   rigol-sourcegui is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   rigol-sourcegui is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with rigol-sourcegui.  If not, see <http://www.gnu.org/licenses/>.'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'morewf_popup.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(350, 370)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setTabKeyNavigation(False)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(_translate("MainWindow", "Custom...", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Sinusoid", None))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Square", None))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Pulse", None))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Noise", None))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "Ramp", None))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "DC", None))
        item = self.listWidget.item(6)
        item.setText(_translate("MainWindow", "Sinc", None))
        item = self.listWidget.item(7)
        item.setText(_translate("MainWindow", "Exp. Rise", None))
        item = self.listWidget.item(8)
        item.setText(_translate("MainWindow", "Exp. Fall", None))
        item = self.listWidget.item(9)
        item.setText(_translate("MainWindow", "ECG", None))
        item = self.listWidget.item(10)
        item.setText(_translate("MainWindow", "Gauss", None))
        item = self.listWidget.item(11)
        item.setText(_translate("MainWindow", "Lorentz", None))
        item = self.listWidget.item(12)
        item.setText(_translate("MainWindow", "Haversine", None))
        item = self.listWidget.item(13)
        item.setText(_translate("MainWindow", "Custom...", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)

