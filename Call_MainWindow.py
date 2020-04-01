# -*- coding:utf-8 -*-

import sys
from MainWindow import Ui_MainWindow
from database_login import Ui_Login_Form
from PyQt5.QtWidgets import *
import pymysql
import hmac
import hashlib
import struct
import time


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        # 槽函数初始化，对应操作发生后自动执行相应的函数
        self.login_pushButton.clicked.connect(self.openForm)
        self.statusbar.showMessage(' MySQL未连接')  #主界面底部状态栏
        self.db_comboBox.activated.connect(self.db_change)
        self.tb_comboBox.currentIndexChanged.connect(self.tb_change)
        self.key_pushButton.clicked.connect(self.openKeyFile)
        self.add_pushButton.clicked.connect(self.watermarkInsert)

    def openForm(self):  # 点登陆按钮 打开登录框
        self.login = LoginForm()  #登陆界面类实例化
        self.login.show()
        self.db_status = self.login.exec_()  # 接收数据库登录框返回的登陆是否成功信息
        #成功登陆则修改状态栏信息，并将主机中的所有数据库名称添加到数据库下拉菜单中
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

    def db_change(self):  #数据库下拉菜单选项修改时执行此函数
        self.cur_db = self.db_comboBox.currentText()
        if self.cur_db != "请先连接MySQL":
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db)
            # print(type(cur_db),cur_db)
            self.login.db.select_db(self.cur_db)
            #将当前所选数据库中的所有表添加到数据表下拉菜单中
            self.cur.execute('show tables')
            item = []
            for i in self.cur.fetchall():
                item.append(i[0])
            self.tb_comboBox.clear()
            self.tb_comboBox.addItems(item)

    def tb_change(self):  #数据表下拉菜单选项修改时执行此函数
        self.cur_tb = self.tb_comboBox.currentText()
        self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db + ', 当前数据表: ' + self.cur_tb)

    def openKeyFile(self):  #打开并读取密钥文件到变量key中
        get_key_path, ok = QFileDialog.getOpenFileName(self, 'Select file', './', 'SecretKey Files(*.key)')
        if ok:
            self.key_lineEdit.setText(str(get_key_path))
        key_file = open(str(get_key_path), 'rb')
        self.key = key_file.readline()
        key_file.close()

    def watermarkInsert(self):  # 点击添加按钮后执行此函数
        time_start = time.time()
        sql = 'desc ' + self.cur_tb  #查询当前表下的所有属性
        self.cur.execute(sql)
        res = self.cur.fetchall()  #获取查询结果
        li = ['float', 'double', 'decimal']
        v_array = []  # 可添加水印属性列表
        maxAttrNum = 0  #可用来添加水印的最大属性数量
        for i, j in enumerate(res):
            if j[3] == 'PRI':
                pk_index = i  #记录属性为主键的索引
            else:
                if j[1] in li:
                    v_array.append(i)
                    maxAttrNum += 1
        # print('primary_key is:[' + res[pk_index][0] + '], and available attribution is:',[res[x][0] for x in v_array])
        pk_name = res[pk_index][0]  #主键属性名
        self.progressBar.setValue(0)  # 进度条清空
        sql = 'SELECT * FROM ' + self.cur_tb
        try:
            self.cur.execute(sql)
            rowcount = self.cur.rowcount
            cur_count = 0
            pk_li = self.cur.fetchall()  # 查询表中所有数据
            for value in pk_li:  # 遍历每一条数据
                # 密钥和主键值进行串接后做二次哈希运算（HMAC运算，直接套用库函数），返回字符串类型
                # print(cur_count,value)
                h = hmac.new(self.key, str(value[pk_index]).encode('utf-8'), digestmod='MD5').hexdigest()
                if not self.hmac_mod(h, self.scale_lineEdit.text()):  #判断哈希值对水印比例系数取模后是否为0
                    attr_index = self.hmac_mod(h, self.attrNum_lineEdit.text())
                    attr_name = res[v_array[attr_index]][0]
                    bit_index = self.hmac_mod(h, self.lsb_lineEdit.text())
                    new_data = self.mark(value[pk_index], value[v_array[attr_index]], bit_index)
                    sql = 'UPDATE ' + self.cur_tb + ' SET ' + attr_name + '=' + str(
                        new_data) + ' WHERE ' + pk_name + '=' + str(value[pk_index])
                    # 为了防止对数据库误修改 初步测试时建议只输出不UPDATE
                    # print(sql)
                    self.update_db(sql)
                    cur_count += 1
                    self.progressBar.setValue(cur_count / rowcount * 100)

        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
        time_end = time.time()
        QMessageBox.information(self, '添加成功', '水印添加成功！\n总用时：%.4fs' % (time_end - time_start), QMessageBox.Ok,
                                QMessageBox.Ok)

    def hmac_mod(self, hmac_str, mod_num):  #对HMAC值进行取模运算
        res = 0
        for ch in hmac_str:
            res = (res * 16 + int(ch, 16)) % int(str(mod_num), 10)
        return res

    def first_hash_calc(self, pk_value):  #密钥和主键串接后的一层哈希计算
        hash_value = hashlib.md5()
        hash_value.update(self.key + str(pk_value).encode('utf-8'))
        return self.hmac_mod(hash_value.hexdigest(), 2)

    def float2bin(self, f):  #浮点数转换为64位二进制数，返回二进制字符串
        return bin(struct.unpack('!Q', struct.pack('!d', f))[0])[2:].zfill(64)

    def bin2float(self, b):  #64位二进制字符串转换为浮点数，返回类型为float
        return struct.unpack('>d', int(b, 2).to_bytes(8, byteorder="big"))[0]

    def mark(self, pk_value, attr_value, bit_index):  #对选中元组的对应属性的值进行修改（水印添加）
        # print(type(attr_value), attr_value, bit_index)
        # 基本思路：接收浮点数并转换为二进制字符串，将比特串按修改比特位的位置进行分割，
        #修改对应比特位的数值后再连接，将连接后的比特串再转回浮点数并返回
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

    def update_db(self, sql):  #执行SQL更新操作
        try:
            self.cur.execute(sql)
            self.login.db.commit()
        except Exception as e:
            self.login.db.rollback()


#数据库登录界面
class LoginForm(QDialog, Ui_Login_Form):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.login)  #槽函数，点击按钮后登陆

    def login(self):
        username = self.user_lineEdit.text()
        if not username:  #不输入username则默认以root登陆
            self.user_lineEdit.setText('root')
            username = 'root'
        hostname = self.host_lineEdit.text()
        if not hostname:  #不输入hostname则默认连接localhost登陆
            self.host_lineEdit.setText('localhost')
            hostname = 'localhost'
        password = self.pwd_lineEdit.text()
        #使用pymysql模块进行数据库的连接
        try:
            self.db = pymysql.connect(hostname, username, password)
            QMessageBox.information(self, 'Database connection', 'Database connection success.')  # 弹出数据库连接成功提示框
            self.accept()  #关闭登陆，并给主窗口返回True
        except pymysql.Error as e:
            QMessageBox.critical(self, 'Database Connection', e.args[1])  #弹出数据库连接错误提示


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainForm()
    main.show()  # 启动主界面
    main.openForm()  #默认启动时打开登录框
    sys.exit(app.exec_())
