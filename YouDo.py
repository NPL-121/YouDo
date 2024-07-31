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
        
        # init GUI elements-------------------------
        # add list of exercisez
        self.comboBoxEx.addItems(["Отжимания", "Приседания"])

        self.pushButtonAdd.clicked.connect(self.base_add_exercise) #button '+'

        # get current time -----------------------------------------
        current_date = datetime.datetime.now().date()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        day = current_date.strftime("%d")
        #set text (date) for label_date
        self.label_date.setText("Сегодня: " + day+"."+month+"."+year)
        # -----------------------------------------------------------

        # ------ db -----
        self.con1 = self.create_connection(path)
        self.read_table_d0(self.con1, "SELECT id, num, current_date FROM table_d0")
        self.create_table_d0 = """
        CREATE TABLE IF NOT EXISTS table_d0 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num TEXT,
        current_date TEXT
        );
        """
        
        self.current_row = 0
        self.edit_flag = False

        # ---click testButton------------
        self.testButton.clicked.connect(self.create_plotWindow)

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
        num = 1
        insertDataQuery.prepare("INSERT INTO table_d0 (num, current_date) VALUES (?,?)")

        data = [(num, current_date)]
        for num, current_date in data:
            insertDataQuery.addBindValue(num)
            insertDataQuery.addBindValue(current_date)
            insertDataQuery.exec()
            print("query complete")
        #self.close_connection()
        
        self.read_table_d0(self.con1, "SELECT id, num, current_date FROM table_d0")
        
        
    def read_table_d0(self, connection, query): # читаем базу и выводим
        self.tableWidget.setRowCount(0)      # в таблицу QTableWidget
        data = QSqlQuery(query)
        self.tableWidget.setColumnCount(3)
        while data.next():
            rows = self.tableWidget.rowCount()
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers) #set read Only
            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setItem(rows, 0, QTableWidgetItem(str(data.value(0))))
            self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(data.value(1))))
            self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(data.value(2))))
        self.tableWidget.resizeColumnsToContents()
        print("Table read. Rows count = ", self.tableWidget.rowCount());
        if self.tableWidget.rowCount() == 0:
            self.create_table(self.con1, """
        CREATE TABLE IF NOT EXISTS table_d0 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num TEXT,
        current_date TEXT
        );
        """)
    # ---- db realization END --------------------


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
