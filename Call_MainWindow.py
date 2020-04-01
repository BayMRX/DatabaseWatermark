# -*- coding:utf-8 -*-

import sys
from MainWindow import Ui_MainWindow
from database_login import Ui_Login_Form
from PyQt5.QtWidgets import *
import pymysql
import hmac
import hashlib
import struct


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.openForm)
        self.statusbar.showMessage(' MySQL未连接')
        self.db_comboBox.activated.connect(self.db_change)
        self.tb_comboBox.currentIndexChanged.connect(self.tb_change)
        self.key_pushButton.clicked.connect(self.openKeyFile)
        self.add_pushButton.clicked.connect(self.readData)

    def openForm(self):
        self.login = LoginForm()
        self.login.show()
        self.db_status = self.login.exec_()
        if self.db_status:
            self.statusbar.showMessage(' MySQL已连接')
            self.cur = self.login.db.cursor()
            self.cur.execute('show databases')
            item = []
            for i in self.cur.fetchall():
                item.append(i[0])
            self.db_comboBox.clear()
            self.db_comboBox.addItems(item)
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.db_comboBox.currentText())

    def db_change(self):
        self.cur_db = self.db_comboBox.currentText()
        if self.cur_db != "请先连接MySQL":
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db)
            # print(type(cur_db),cur_db)
            self.login.db.select_db(self.cur_db)
            self.cur.execute('show tables')
            item = []
            for i in self.cur.fetchall():
                item.append(i[0])
            self.tb_comboBox.clear()
            self.tb_comboBox.addItems(item)

    def tb_change(self):
        self.cur_tb = self.tb_comboBox.currentText()
        self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db + ', 当前数据表: ' + self.cur_tb)

    def openKeyFile(self):
        get_key_path, ok = QFileDialog.getOpenFileName(self, 'Select file', './', 'SecretKey Files(*.key)')
        if ok:
            self.key_lineEdit.setText(str(get_key_path))
        key_file = open(str(get_key_path), 'rb')
        self.key = key_file.readline()
        key_file.close()

    def readData(self):
        sql = 'desc ' + self.cur_tb
        self.cur.execute(sql)
        res = self.cur.fetchall()
        li = ['float', 'double', 'decimal']
        v_array = []
        maxAttrNum = 0
        for i, j in enumerate(res):
            if j[3] == 'PRI':
                pk_index = i
            else:
                if j[1] in li:
                    v_array.append(i)
                    maxAttrNum += 1
        # print('primary_key is:[' + res[pk_index][0] + '], and available attribution is:',[res[x][0] for x in v_array])
        pk_name = res[pk_index][0]
        sql = 'SELECT * FROM ' + self.cur_tb
        try:
            self.cur.execute(sql)
            pk_li = self.cur.fetchall()
            for value in pk_li:
                h = hmac.new(self.key, str(value[pk_index]).encode('utf-8'), digestmod='MD5').hexdigest()
                if not self.hmac_mod(h, self.scale_lineEdit.text()):
                    attr_index = self.hmac_mod(h, self.attrNum_lineEdit.text())
                    attr_name = res[v_array[attr_index]][0]
                    bit_index = self.hmac_mod(h, self.lsb_lineEdit.text())
                    new_data = self.mark(value[pk_index], value[v_array[attr_index]], bit_index)
                    sql = 'UPDATE ' + self.cur_tb + ' SET ' + attr_name + '=' + str(
                        new_data) + ' WHERE ' + pk_name + '=' + str(value[pk_index])
                    # 为了防止对数据库误修改 初步测试时建议只输出不UPDATE
                    # print(sql)
                    # self.update_db(sql)
        except Exception as e:
            print(e)
        self.login.db.close()
        print('Done!')

    def hmac_mod(self, hmac_str, mod_num):
        res = 0
        for ch in hmac_str:
            res = (res * 16 + int(ch, 16)) % int(str(mod_num), 10)
        return res

    def first_hash_calc(self, pk_value):
        hash_value = hashlib.md5()
        hash_value.update(self.key + str(pk_value).encode('utf-8'))
        return self.hmac_mod(hash_value.hexdigest(), 2)

    def float2bin(self, f):
        return bin(struct.unpack('!Q', struct.pack('!d', f))[0])[2:].zfill(64)

    def bin2float(self, b):
        return struct.unpack('>d', int(b, 2).to_bytes(8, byteorder="big"))[0]

    def mark(self, pk_value, attr_value, bit_index):
        # print(type(attr_value), attr_value, bit_index)
        attr_binVal = self.float2bin(attr_value)
        str1 = attr_binVal[0:-(bit_index + 1)]
        if self.first_hash_calc(pk_value):
            bit_val = '1'
        else:
            bit_val = '0'
        if bit_index == 0:
            str0 = str1 + bit_val
        else:
            str2 = attr_binVal[-bit_index:]
            str0 = str1 + bit_val + str2
        return self.bin2float(str0)

    def update_db(self, sql):
        try:
            self.cur.execute(sql)
            self.login.db.commit()
        except Exception as e:
            self.login.db.rollback()



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
