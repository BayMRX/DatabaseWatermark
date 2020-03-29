# -*- coding:utf-8 -*-

import sys
from MainWindow import Ui_MainWindow
from database_login import Ui_Login_Form
from PyQt5.QtWidgets import *
import pymysql


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.openForm)
        self.statusbar.showMessage(' MySQL未连接')
        self.db_comboBox.activated.connect(self.db_change)
        self.tb_comboBox.currentIndexChanged.connect(self.tb_change)
        self.key_pushButton.clicked.connect(self.openKeyFile)
        
    def openForm(self):
        self.login = LoginForm()
        self.login.show()
        res = self.login.exec_()
        if res:
            self.statusbar.showMessage(' MySQL已连接')
            self.cur = self.login.db.cursor()
            self.cur.execute('show databases')
            item = []
            for i in self.cur.fetchall():
                item.append(i[0])
            self.db_comboBox.clear()
            self.db_comboBox.addItems(item)
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' +self.db_comboBox.currentText())
    def db_change(self):
        self.cur_db = self.db_comboBox.currentText()
        if self.cur_db != "请先连接MySQL":
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: '+self.cur_db)
            #print(type(cur_db),cur_db)
            self.login.db.select_db(self.cur_db)
            self.cur.execute('show tables')
            item = []
            for i in self.cur.fetchall():
                item.append(i[0])
            self.tb_comboBox.clear()
            self.tb_comboBox.addItems(item)
    def tb_change(self):
        self.cur_tb = self.tb_comboBox.currentText()
        self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db+', 当前数据表: '+self.cur_tb)
    def openKeyFile(self):
        get_key_path,ok = QFileDialog.getOpenFileName(self,'Select file','./','SecretKey Files(*.key)')
        if ok:
            self.key_lineEdit.setText(str(get_key_path))
    def data(self):
        pass

class LoginForm(QDialog, Ui_Login_Form):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.login)

    def login(self):
        username = self.user_lineEdit.text()
        if not username:
            self.user_lineEdit.setText('root')
            username = 'root'
        hostname = self.host_lineEdit.text()
        if not hostname:
            self.host_lineEdit.setText('localhost')
            hostname = 'localhost'
        password = self.pwd_lineEdit.text()
        try:
            self.db = pymysql.connect(hostname, username, password)
            QMessageBox.information(self, 'Database connection', 'Database connection success.')
            self.accept()
        except pymysql.Error as e:
            QMessageBox.critical(self, 'Database Connection', e.args[1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainForm()
    main.show()
    main.openForm()
    sys.exit(app.exec_())
