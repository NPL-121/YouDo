#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Name:        YouDo.py
# Purpose:
#
# Author:      NPL
#
# Created:     29.07.2024
# Copyright:   (c) StarRiver
# Licence:     <My>
#-------------------------------------------------------------------------------

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
import FormUI
import sqlite3 as sl
from sqlite3 import Error
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import datetime
import pyqtgraph as pg
import numpy as np

# window graph ------------------------------------------------------------------
class WindowPlot(QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.view = view = pg.PlotWidget()
        self.curve = view.plot(name="Line")

        self.btn = QtWidgets.QPushButton("Random plot")
        self.btn.clicked.connect(self.random_plot)

        layout.addWidget(QtWidgets.QLabel("Some text"))
        layout.addWidget(self.view)
        layout.addWidget(self.btn)
    
    def random_plot(self):
        random_array = np.random.random_sample(20)
        self.curve.setData(random_array)




# main window -------------------------------------------------------------------
class UIForm(QtWidgets.QMainWindow, FormUI.Ui_MainWindow):
    def __init__(self, path):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.path = path

        self.w = None  # No external window yet.
        
        self.setWindowTitle("YouDo v. 0.0.5")

        # init GUI elements-------------------------
        # add list of exercisez
        self.comboBoxEx.addItems(["Отжимания", "Приседания", "Жим гантелей стоя", 
                                  "Подъём гантелей перед собой",\
                                  "Подъём гантелей на бицепс"])
        # ======== S I G N A L S ==============================================
        self.pushButtonAdd.clicked.connect(self.base_add_exercise) #button '+'
        self.pushButtonDel.clicked.connect(self.base_del_exercise) #button '-'
        self.tableWidget.clicked.connect(self.select_row) #select row in table
        self.tableWidget.doubleClicked.connect(self.table_edit) #table edit mode
        self.tableWidget.cellChanged.connect(self.table_endChange) #Savings change
        # ---click testButton------------
        self.testButton.clicked.connect(self.create_plotWindow)
        # ========= E N D   S I G N A L S =====================================

        # ===== V A R S =======================================================
        self.id_key = 0  # ID выбранной ячейки
        self.current_row = 0 # selected row
        self.edit_flag = False # edit mode is off
        self.table_d0Rows = 0
        #self.edited = False #переменная принимающая true после редактирования таблицы
        self.column_edit = 0
        self.row_edit = 0
        # ====== E N D    V A R S =============================================

        # C A L E N D A R -----------------------------------------------------------
        # get current time -----------------------------------------
        current_date = datetime.datetime.now().date()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")
        #set text (date) for label_date
        self.label_date.setText("Сегодня: " + day+"."+month+"."+year)
                
        # -----------------------------------------------------------

        # ======== D A T A B A S E ==================================================
        self.con1 = self.create_connection(path)
        # read database -------
        self.read_table_d0(self.con1, "SELECT id, selected_date, mass, exer1,  \
                Ex1mass, n1, n2, n3, n4, n5 FROM table_d0 ORDER BY selected_date")

        self.create_table_d0 = """
        CREATE TABLE IF NOT EXISTS table_d0 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        selected_date DATE,
        mass DECIMAL,
        exer1 TEXT,
        Ex1mass DECIMAL,
        n1 TINYINT,
        n2 TINYINT,
        n3 TINYINT,
        n4 TINYINT,
        n5 TINYINT
        );
        """
        
        
       
    # =========================================================
    # --- db realization START ----------------
    def create_connection(self, path): #---------------------------------------------
        connection = None
        try:
            connection = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            connection.setDatabaseName(path)
            connection.open()
            print("Connection to SQLite DB succesful.")
        except Error as e:
            print("The error occurred:")
            print(e)
        return connection

    def close_connection(self): # -----------------------------------------------
        self.con1.close()
        if self.con1.isOpen() == False:
            print ("Connection closed.")
            
    def create_table(self, connection, query): #----------------------------------
        createTableQuery = QSqlQuery()
        try:
            createTableQuery.exec(query)
            print("Query executed succesfully.")
        except Error as e:
                print("The error occurred:")
                print(e)

    def base_add_exercise(self, connection):   # add new row in table, button '+' ------
        # add exercise for current date from calendar
        print("add exercise")
        # get vars
        current_date = datetime.datetime.now().date()

        insertDataQuery = QSqlQuery()
        mass = 90.0
        #exer1 = "Test exer"
        exer1 = self.comboBoxEx.currentText()
        Ex1mass = 0.0
        n1 = 1
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        insertDataQuery.prepare("INSERT INTO table_d0 (selected_date, mass, \
                exer1, Ex1mass, n1, n2, n3, n4, n5) VALUES (?,?,?,?,?,?,?,?,?)")
        
        # get selected date-----------------------------------------
        selected_date = self.calendarWidget.selectedDate()
        data = [(selected_date, mass, exer1, Ex1mass, n1, n2, n3, n4, n5)]
        for selected_date, mass, exer1, Ex1mass, n1, n2, n3, n4, n5 in data:
            insertDataQuery.addBindValue(selected_date)
            insertDataQuery.addBindValue(mass)
            insertDataQuery.addBindValue(exer1)
            insertDataQuery.addBindValue(Ex1mass)
            insertDataQuery.addBindValue(n1)
            insertDataQuery.addBindValue(n2)
            insertDataQuery.addBindValue(n3)
            insertDataQuery.addBindValue(n4)
            insertDataQuery.addBindValue(n5)
            insertDataQuery.exec()
            print("query complete")
        #self.close_connection()
        
        # variant with id
        self.read_table_d0(self.con1, "SELECT id, selected_date, mass, \
                exer1, Ex1mass, n1, n2, n3, n4, n5 FROM table_d0")
        # varint without id
        #self.read_table_d0(self.con1, "SELECT mass, selected_date, \
        #        exer1, Ex1mass, n1, n2, n3, n4, n5 FROM table_d0")


    # удаление записи упражнения --------------------------------   
    def base_del_exercise(self, connection):
        print("Delete exercise")
        id_key = 0 
        #con1 = self.con1
        key = self.id_key
        query = "DELETE FROM table_d0 WHERE id LIKE '%s'" % key
        try:
            self.con1.exec(query)
            self.con1.commit()
            self.read_table_d0(self.con1, "SELECT id, selected_date, mass, \
                    exer1, Ex1mass, n1, n2, n3, n4, n5 FROM table_d0")

        except Error as e:
            print("The error occurred:")
            print(e)

    # выбор ячейки в таблице мышкой ------------------------------
    def select_row(self):
        id_ = 0
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        print("select row, column: ", row, ", ", col)

        # old key id realization ---------------------
        id_key = self.tableWidget.item(row,0).text()

        # new key id realization ---------------------
        # id_key = 
        print("id: ", id_key)
        
        self.id_key = id_key

    # чтение базы и вывод в таблицу -------------------------------------
    def read_table_d0(self, connection, query): # читаем базу и выводим
        self.tableWidget.setRowCount(0)      # в таблицу QTableWidget
        data = QSqlQuery(query)
        self.tableWidget.setColumnCount(10)
        
        # if table not present
        if self.tableWidget.rowCount() == 0:
            self.create_table(self.con1, """
        CREATE TABLE IF NOT EXISTS table_d0 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        selected_date DATE,
        mass DECIMAL,
        exer1 TEXT,
        Ex1mass DECIMAL,
        n1 TINYINT,
        n2 TINYINT,
        n3 TINYINT,
        n4 TINYINT,
        n5 TINYINT
        );
        """)

        # title create ------------
        self.create_title_table_d0()

        # если мы не хотим чтоб id выводился в таблицу, то сделаем сдвиг на 1
        # т.е sh = 1, иначе sh = 0
        sh = 0

        # table write -------------
        while data.next():
            rows = self.tableWidget.rowCount()
            #set read Only
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.tableWidget.setRowCount(rows + 1)
            # поле, содержащее id заполняем так, ради Read only
            item_id = QTableWidgetItem(str(data.value(0+sh)))
            item_id.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rows, 0, item_id)
            # поле "дата" заполняем так, ради Read only
            item = QTableWidgetItem(str(data.value(1+sh)))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rows, 1, item)
            print("DATE: ", item.text())

            # все остальные поля заполняем так
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(data.value(2+sh))))
            self.tableWidget.setItem(rows, 3, QTableWidgetItem(str(data.value(3+sh))))
            self.tableWidget.setItem(rows, 4, QTableWidgetItem(str(data.value(4+sh))))
            self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(data.value(5+sh))))
            self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(data.value(6+sh))))
            self.tableWidget.setItem(rows, 7, QTableWidgetItem(str(data.value(7+sh))))
            self.tableWidget.setItem(rows, 8, QTableWidgetItem(str(data.value(8+sh))))
            self.tableWidget.setItem(rows, 9, QTableWidgetItem(str(data.value(9+sh))))
        self.tableWidget.resizeColumnsToContents()
        print("Table read. Rows count = ", self.tableWidget.rowCount())

    # table edit -----------------------------------------------
    def table_edit(self):
        print ("Table is editing now")
        self.tableWidget.edit(self.tableWidget.currentIndex())
        self.column_edit = self.tableWidget.currentColumn()
        self.row_edit = self.tableWidget.currentRow()
        self.edit_flag = True

    # table savings change after close editing mode
    def table_endChange(self):
        if self.edit_flag == True:
            print("edit mode off")
            self.edit_flag == False

            item_value = self.tableWidget.item(self.row_edit, self.column_edit).text()
            id_value=self.tableWidget.item(self.row_edit, 0).text()
            #print("id_value = ", id_value)
            upDataQuery = QSqlQuery()

            if self.column_edit == 2: #mass
                mass = item_value
                upDataQuery.prepare('UPDATE table_d0 SET mass=:mass WHERE id=:var')
                upDataQuery.bindValue(':mass', mass)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()

            if self.column_edit == 4: #Ex1mass
                Ex1mass = item_value
                upDataQuery.prepare('UPDATE table_d0 SET Ex1mass=:Ex1mass WHERE id=:var')
                upDataQuery.bindValue(':Ex1mass', Ex1mass)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()
            if self.column_edit == 5: #n1
                n1 = item_value
                upDataQuery.prepare('UPDATE table_d0 SET n1=:n1 WHERE id=:var')
                upDataQuery.bindValue(':n1', n1)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()
            if self.column_edit == 6: #n2
                n2 = item_value
                upDataQuery.prepare('UPDATE table_d0 SET n2=:n2 WHERE id=:var')
                upDataQuery.bindValue(':n2', n2)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()
            if self.column_edit == 7: #n3
                n3 = item_value
                upDataQuery.prepare('UPDATE table_d0 SET n3=:n3 WHERE id=:var')
                upDataQuery.bindValue(':n3', n3)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()
            if self.column_edit == 8: #n4
                n4 = item_value
                upDataQuery.prepare('UPDATE table_d0 SET n4=:n4 WHERE id=:var')
                upDataQuery.bindValue(':n4', n4)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()
            if self.column_edit == 9: #n5
                n5 = item_value
                upDataQuery.prepare('UPDATE table_d0 SET n5=:n5 WHERE id=:var')
                upDataQuery.bindValue(':n5', n5)
                upDataQuery.bindValue(':var', id_value)
                upDataQuery.exec()

        
    # create TITLE table_d0 ------------------------------------
    def create_title_table_d0(self):
        print("Title for table_d0 create")
        self.table_d0Rows=0
        self.tableWidget.setRowCount(1)
        # row 1 -----
        item = QTableWidgetItem("id")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,0,item)
        # row 2 -----
        item = QTableWidgetItem("Дата")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,1,item)
        # row 3 -----
        item = QTableWidgetItem("Масса, кг")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,2,item)
        # row 4 -----
        item = QTableWidgetItem("Упражнение")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,3,item)
        # row 5 -----
        item = QTableWidgetItem("Отягощение, кг")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,4,item)
        # row 6 -----
        item = QTableWidgetItem("сет 1")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,5,item)
        # row 7 -----
        item = QTableWidgetItem("сет 2")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,6,item)
        # row 8 -----
        item = QTableWidgetItem("сет 3")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,7,item)
        # row 9 -----
        item = QTableWidgetItem("сет 4")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        item.setFlags(QtCore.Qt.ItemIsEnabled) 
        self.tableWidget.setItem(self.table_d0Rows,8,item)
        # row 10 -----
        item = QTableWidgetItem("сет 5")
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        #item.setFlags(QtCore.Qt.ItemIsEditable) #this cell is read only
        item.setFlags(QtCore.Qt.ItemIsEnabled) # another variant read only
        self.tableWidget.setItem(self.table_d0Rows,9,item)

    # ---- db realization END --------------------
    #=====================================================================


    def create_plotWindow(self):
        if self.w is None:
            self.w = WindowPlot()
        self.w.show()
        print("testGraph")

# ------------------------------------ #
#                 M A I N              #
# ------------------------------------ #

def main():

 	# get current time
    current_time = datetime.datetime.now().time()
    print(current_time)
    # get current date
    current_date = datetime.datetime.now().date()
    print(current_date)

    #con1 = create_connection('test.db')
    #create_table(con1, create_users_table)
    #create_row_table(con1, create_user, data)
    #execute_read_query(con1, read_all)    
    
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')

    #wPlot = WindowPlot()
    window = UIForm('data.db')  # Создаём объект класса UIForm

    window.show()  # Показываем окно

    app.exec_()  # и запускаем приложение
    
    window.close_connection()    

if __name__ == '__main__':
    main()
