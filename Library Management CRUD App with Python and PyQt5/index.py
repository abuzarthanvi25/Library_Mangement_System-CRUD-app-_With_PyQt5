from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb
from PyQt5.uic import loadUiType


ui,_ = loadUiType('library.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()

        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()

        self.Show_All_Books()

        self.Show_All_Users()
        self.Show_Issued_Books()
        self.Total_Number_Of_Issued_Books()
        self.Show_Premium_Books()
        self.Show_Moderately_Priced_Books()

        self.Show_Outsider_Record()
        self.Show_Employee_Record()
        self.Show_Student_Record()
        self.Show_Staff_Record()

        self.Show_Combined_Records()
        self.Show_User_Issued()

    def Handle_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
       self.pushButton_5.clicked.connect(self.Show_Themes)
       self.pushButton_22.clicked.connect(self.Hiding_Themes)

       self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
       self.pushButton_2.clicked.connect(self.Open_Books_Tab)
       self.pushButton_3.clicked.connect(self.Open_Users_Tab)
       self.pushButton_4.clicked.connect(self.Open_Settings_Tab)
       
       self.pushButton_7.clicked.connect(self.Add_New_Book)

       self.pushButton_15.clicked.connect(self.Add_Category)
       self.pushButton_16.clicked.connect(self.Add_Author)
       self.pushButton_17.clicked.connect(self.Add_Publisher)

       self.pushButton_19.clicked.connect(self.Dark_Theme)
       self.pushButton_18.clicked.connect(self.Dark_Blue_Theme)
       self.pushButton_20.clicked.connect(self.QDark_Theme)
       self.pushButton_21.clicked.connect(self.Dark_LightBlack_Theme)

       self.pushButton_6.clicked.connect(self.Day_To_Day_Operations)
       self.pushButton_10.clicked.connect(self.Search_Books)
       self.pushButton_9.clicked.connect(self.Edit_Books)
       self.pushButton_26.clicked.connect(self.Clear_Search_Data)
       self.pushButton_11.clicked.connect(self.Delete_Books)

       self.pushButton_12.clicked.connect(self.Add_New_User)
       self.pushButton_14.clicked.connect(self.Edit_User)


    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()
        

##################################################################
#################### Opening Tabs ################################

    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)

##################################################################
#################### Books #######################################

    def Add_New_Book(self):
        
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.lineEdit_25.text()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher,book_price)
            VALUES (%s , %s , %s , %s, %s, %s, %s )
        ''' ,(book_title , book_description , book_code ,book_category,book_author,book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_2.setText('')
        self.lineEdit_25.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)

        self.Show_All_Books()
       

    def Show_All_Books(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_code,book_name, book_author,book_publisher,book_category,book_price FROM book''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

    def Search_Books(self):

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        Search_book_title = self.lineEdit_9.text()

        sql = ''' SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql , [(Search_book_title)])

        data = self.cur.fetchone()
        
        self.Show_Search_Book()

    def Show_Search_Book(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        Search_book_title = self.lineEdit_9.text()

        sql = ''' SELECT book_name,book_description,book_category,book_author,book_publisher,book_price FROM book WHERE book_name = %s '''
        self.cur.execute(sql , [(Search_book_title)])

        data = self.cur.fetchall()

        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))

    def Clear_Search_Data(self):
        self.tableWidget_5.setRowCount(0)

    def Edit_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_30.text()
        book_description = self.lineEdit_35.text()
        book_code = self.lineEdit_10.text()
        book_category = self.lineEdit_33.text()
        book_author = self.lineEdit_32.text()
        book_publisher = self.lineEdit_31.text()
        book_price = self.lineEdit_8.text()


        search_book_title = self.lineEdit_9.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s WHERE book_name = %s            
        ''', (book_title,book_description,book_code,book_category,book_author,book_publisher , book_price , search_book_title))

        self.db.commit()
        self.statusBar().showMessage('Book Updated')
        self.lineEdit_30.setText('')
        self.lineEdit_35.setText('')
        self.lineEdit_10.setText('')
        self.lineEdit_33.setText('')
        self.lineEdit_32.setText('')
        self.lineEdit_31.setText('')
        self.lineEdit_8.setText('')

        self.Show_All_Books()

    def Delete_Books(self):
        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_34.text()

        warning = QMessageBox.warning(self , 'Delete Book' , "Are you sure you want to delete this book?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql , [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')
            self.lineEdit_34.setText('')

            self.Show_All_Books

##################################################################
#################### Users #######################################

    def Add_New_User(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        user_name = self.lineEdit_12.text()
        user_email = self.lineEdit_13.text()
        user_password = self.lineEdit_14.text()
        user_type = self.lineEdit_15.text()
        user_code = self.lineEdit_16.text()

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO users(user_name , user_email , user_password, user_type, user_code)
            VALUES (%s , %s , %s, %s, %s)
        ''' , (user_name , user_email , user_password, user_type, user_code))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('New user Added')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_15.setText('')
        

        self.Show_All_Users()

    def Show_All_Users(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT user_name , user_email ,user_password,user_type,user_code FROM users ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_6.setRowCount(0)
            self.tableWidget_6.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(row_position)

    def Login(self):
        pass

    def Edit_User(self):
        user_name = self.lineEdit_19.text()
        user_email = self.lineEdit_21.text()
        user_password = self.lineEdit_20.text()

        self.db = MySQLdb.connect(host='localhost' , user='root' , password ='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        Old_User_name = self.lineEdit_36.text()

        self.cur.execute('''
            UPDATE users SET user_name = %s , user_email = %s , user_password = %s WHERE user_name = %s
        ''' , (user_name , user_email , user_password, Old_User_name ))
        self.db.commit()
        self.statusBar().showMessage('User Data Updated')
        self.lineEdit_19.setText('')
        self.lineEdit_21.setText('')
        self.lineEdit_20.setText('')
        self.lineEdit_36.setText('')

        self.Show_All_Users()

##################################################################
#################### Settings ####################################

    def Add_Category(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_22.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
         ''' ,(category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_22.setText('')
        self.Show_Category()

    def Show_Category(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category  ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    
    def Add_Author(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_23.text()

        self.cur.execute('''
            INSERT INTO authors (author_name) VALUES (%s)
         ''' ,(author_name,))

        self.db.commit()
        self.lineEdit_23.setText('')
        self.statusBar().showMessage('New Author Added')
        self.Show_Author()

    def Show_Author(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def Add_Publisher(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_24.text()

        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (%s)
         ''' ,(publisher_name,))

        self.db.commit()
        self.lineEdit_24.setText('')
        self.statusBar().showMessage('New Publisher Added')
        self.Show_Publisher()

    def Show_Publisher(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

##################################################################
#################### Show Settings Data in UI ####################
    
    def Show_Category_Combobox(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category''')
        data = self.cur.fetchall()

        for category in data:
            self.comboBox_3.addItem(category[0])



    def Show_Author_Combobox(self):

        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        for author in data:
            self.comboBox_4.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        for publisher in data:
            self.comboBox_5.addItem(publisher[0])

###############################################################
#################### Day-To-Day Operations ####################
    def Day_To_Day_Operations(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        Issued_Book = self.lineEdit.text()
        Issue_type = self.comboBox.currentText()
        Issue_days = self.comboBox_2.currentText()
        User_Name = self.lineEdit_26.text()

        self.cur.execute('''
            INSERT INTO dayoperations (book_name, type, days, user_name) VALUES (%s, %s, %s, %s)
         ''' ,(Issued_Book, Issue_type, Issue_days, User_Name ))

        self.db.commit()
        self.lineEdit.setText('')
        self.lineEdit_26.setText('')
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)
        self.statusBar().showMessage('Book Issued Successfully!')







###############################################################
#################### UI Themes ################################
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_LightBlack_Theme(self):
        style = open('themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Show_Issued_Books(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        #self.cur.execute(''' SELECT COUNT(*) as Total_number_of_books_issued FROM dayoperations ''')
        self.cur.execute(''' SELECT COUNT(*) as Total_Number,book_category FROM book GROUP BY book_category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_12.setRowCount(0)
            self.tableWidget_12.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_12.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_12.rowCount()
                self.tableWidget_12.insertRow(row_position)

    def Total_Number_Of_Issued_Books(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT COUNT(*) as Total_number_of_books_issued FROM dayoperations ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_11.setRowCount(0)
            self.tableWidget_11.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_11.setItem(row, column, QTableWidgetItem(str(item)))

    def Show_Premium_Books(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_price,book_name FROM book WHERE book_price >= 10 ''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_10.setRowCount(0)
            self.tableWidget_10.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_10.rowCount()
                self.tableWidget_10.insertRow(row_position)

    def Show_Outsider_Record(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT user_name,user_email FROM users WHERE user_type = "outsider"''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_7.setRowCount(0)
            self.tableWidget_7.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_7.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_7.rowCount()
                self.tableWidget_7.insertRow(row_position)

    def Show_Employee_Record(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT user_name,user_email FROM users WHERE user_type = "employee"''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_8.setRowCount(0)
            self.tableWidget_8.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_8.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_8.rowCount()
                self.tableWidget_8.insertRow(row_position)

    def Show_Student_Record(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT user_name,user_email FROM users WHERE user_type = "student"''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_9.setRowCount(0)
            self.tableWidget_9.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_9.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_9.rowCount()
                self.tableWidget_9.insertRow(row_position)

    def Show_Staff_Record(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT user_name,user_email FROM users WHERE user_type = "staff"''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_13.setRowCount(0)
            self.tableWidget_13.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_13.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_13.rowCount()
                self.tableWidget_13.insertRow(row_position)

    def Show_Moderately_Priced_Books(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_price,book_name FROM book WHERE book_price BETWEEN 5 and 9''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_14.setRowCount(0)
            self.tableWidget_14.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_14.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_14.rowCount()
                self.tableWidget_14.insertRow(row_position)
            
    def Show_Combined_Records(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT bk.book_name, bk.book_price,us.user_name,us.user_email FROM book as bk INNER JOIN users as us ON bk.book_code = us.user_code''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_15.setRowCount(0)
            self.tableWidget_15.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_15.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_15.rowCount()
                self.tableWidget_15.insertRow(row_position)
        
    def Show_User_Issued(self):
        self.db = MySQLdb.connect(host= 'localhost' ,user='root' , password='hadronzeus' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_name,type,days,user_name FROM dayoperations''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_16.setRowCount(0)
            self.tableWidget_16.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_16.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_16.rowCount()
                self.tableWidget_16.insertRow(row_position)



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show() 
    app.exec_()


if __name__ == '__main__':
    main()