# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './FormUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 692)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_date = QtWidgets.QLabel(self.centralwidget)
        self.label_date.setGeometry(QtCore.QRect(970, 10, 141, 17))
        self.label_date.setObjectName("label_date")
        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(190, 580, 83, 25))
        self.testButton.setObjectName("testButton")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(870, 30, 241, 171))
        self.calendarWidget.setObjectName("calendarWidget")
        self.groupBoxAddEx = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxAddEx.setGeometry(QtCore.QRect(20, 420, 261, 131))
        self.groupBoxAddEx.setObjectName("groupBoxAddEx")
        self.comboBoxEx = QtWidgets.QComboBox(self.groupBoxAddEx)
        self.comboBoxEx.setGeometry(QtCore.QRect(0, 30, 161, 25))
        self.comboBoxEx.setObjectName("comboBoxEx")
        self.pushButtonAdd = QtWidgets.QPushButton(self.groupBoxAddEx)
        self.pushButtonAdd.setGeometry(QtCore.QRect(170, 30, 41, 26))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.spinBoxSets = QtWidgets.QSpinBox(self.groupBoxAddEx)
        self.spinBoxSets.setGeometry(QtCore.QRect(180, 60, 49, 26))
        self.spinBoxSets.setMinimum(1)
        self.spinBoxSets.setMaximum(10)
        self.spinBoxSets.setProperty("value", 5)
        self.spinBoxSets.setObjectName("spinBoxSets")
        self.label = QtWidgets.QLabel(self.groupBoxAddEx)
        self.label.setGeometry(QtCore.QRect(5, 64, 171, 17))
        self.label.setObjectName("label")
        self.pushButtonDel = QtWidgets.QPushButton(self.groupBoxAddEx)
        self.pushButtonDel.setGeometry(QtCore.QRect(210, 30, 41, 26))
        self.pushButtonDel.setObjectName("pushButtonDel")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 851, 371))
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1116, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_date.setText(_translate("MainWindow", "Сегодня:"))
        self.testButton.setText(_translate("MainWindow", "testButton"))
        self.groupBoxAddEx.setTitle(_translate("MainWindow", "Добавить упражнение"))
        self.pushButtonAdd.setText(_translate("MainWindow", "+"))
        self.label.setText(_translate("MainWindow", "Количество подходов:"))
        self.pushButtonDel.setText(_translate("MainWindow", "-"))
