# -*- coding:utf-8 -*-

import sys
import pymysql
import hmac
import hashlib
import struct
import time
import os
from UI_InsertDetect import Ui_MainWindow
from database_login import Ui_Login_Form
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 全局变量声明
db = key = cursor = cur_tb = None
username = hostname = password = None
pk_index = pk_name = v_dict = None


# 程序主界面
class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.login = LoginForm()  # 登陆界面类实例化
        self.setupUi(self)
        # 添加输入框数字验证器（只允许输入数字）
        IntValidator = QIntValidator(self)
        DoubleValidator = QDoubleValidator(self)
        # DoubleValidator.setRange(0, 100, 5)
        self.scale_lineEdit.setValidator(IntValidator)
        # 槽函数初始化，对应操作发生后自动执行相应的函数
        self.login_pushButton.clicked.connect(self.openForm)
        self.statusbar.showMessage(' MySQL未连接')  # 主界面底部状态栏
        self.db_comboBox.activated.connect(self.db_change)
        self.tb_comboBox.activated.connect(self.tb_change)
        self.key_pushButton.clicked.connect(self.openKeyFile)
        self.add_pushButton.clicked.connect(self.watermarkInsert)
        self.detect_pushButton.clicked.connect(self.watermarkDetect)
        self.backup_pushButton.clicked.connect(self.backup)
        self.recover_pushButton.clicked.connect(self.recover)
        self.addAttr_pushButton.clicked.connect(self.move2left)
        self.delAddr_pushButton.clicked.connect(self.move2right)

    def openForm(self):  # 点登陆按钮 打开登录框
        global cursor
        self.login.show()
        db_status = self.login.exec_()  # 接收数据库登录框返回的登陆是否成功信息
        # 成功登陆则修改状态栏信息，并将主机中的所有数据库名称添加到数据库下拉菜单中
        if db_status:
            self.statusbar.showMessage(' MySQL已连接')
            cursor = db.cursor()
            cursor.execute('show databases')
            item = []
            for i in cursor.fetchall():
                item.append(i[0])
            self.db_comboBox.clear()
            self.db_comboBox.addItems(item)
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.db_comboBox.currentText())

    def db_change(self):  # 数据库下拉菜单选项修改时执行此函数
        self.cur_db = self.db_comboBox.currentText()
        if self.cur_db != "请先连接MySQL":
            self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db)
            # print(type(cur_db),cur_db)
            db.select_db(self.cur_db)
            # 将当前所选数据库中的所有表添加到数据表下拉菜单中
            cursor.execute('show tables')
            item = []
            for i in cursor.fetchall():
                item.append(i[0])
            self.tb_comboBox.clear()
            self.tb_comboBox.addItems(item)

    def tb_change(self):  # 数据表下拉菜单选项修改时执行此函数
        global cur_tb, pk_index, pk_name, v_dict
        cur_tb = self.tb_comboBox.currentText()
        self.statusbar.showMessage(' MySQL已连接| 当前数据库: ' + self.cur_db + ', 当前数据表: ' + cur_tb)
        # 下面是读取数据表中的所有属性并添加到界面左边的列表栏中
        sql = 'desc ' + cur_tb  # 查询当前表下的所有属性
        cursor.execute(sql)
        res = cursor.fetchall()  # 获取查询结果
        db.commit()
        v_dict = {}
        li = ['float', 'double', 'decimal']
        self.left_listWidget.clear()
        self.right_listWidget.clear()
        for i, j in enumerate(res):
            if j[3] == 'PRI':
                pk_index = i  # 记录属性为主键的索引
            else:
                if j[1] in li:
                    self.left_listWidget.addItem(j[0])
                    v_dict[j[0]] = i
        pk_name = res[pk_index][0]  # 主键属性名
        # print(v_dict)

    def openKeyFile(self):  # 打开并读取密钥文件到变量key中
        global key
        get_key_path, ok = QFileDialog.getOpenFileName(self, 'Select file', './', 'SecretKey Files(*.key)')
        if ok:
            self.key_lineEdit.setText(str(get_key_path))
            key_file = open(str(get_key_path), 'rb')
            key = key_file.readline()
            key_file.close()

    # 对当前数据表进行备份，备份到软件当前目录
    def backup(self):
        global username, password, cur_tb
        filename = "./" + cur_tb + ".sql"
        try:
            # 在正常的备份语句前需添加临时环境变量，否则会有warning黑框弹出
            cmd = "MYSQL_PWD=" + password + "&& mysqldump -u" + username + " " + self.cur_db + " " + cur_tb + " > " + filename
            if os.name == 'nt':
                cmd = "set " + cmd
            # print(cmd)
            if not os.path.exists(filename):
                os.system(cmd)
                self.finishDialog("备份完成！")
            else:
                # 备份文件已存在弹窗选择是否进行覆盖
                rec_code = QMessageBox.warning(self, '文件已存在！', '此数据表已有备份文件存在，是否覆盖？', QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.Yes)
                if rec_code != 65536:
                    os.system(cmd)
                    self.finishDialog("备份完成！")
                    os.system("set MYSQL_PWD=")
        except Exception as e:
            self.err_info(str(e))

    # 对当前数据表备份过的数据进行还原
    def recover(self):
        global db, username, password, cur_tb, cursor
        filename = "./" + cur_tb + ".sql"
        try:
            # 在正常的恢复语句前需添加临时环境变量，否则会有warning黑框弹出
            cmd = "MYSQL_PWD=" + password + "&& mysql -u" + username + " " + self.cur_db + " < " + filename
            if os.name == 'nt':  # 判断系统类型，nt为windows
                cmd = "set " + cmd
            if not os.path.exists(filename):
                self.err_info("备份文件不存在！")
            else:
                os.system(cmd)
                self.finishDialog("恢复完成！")
                os.system("set MYSQL_PWD=")
        except Exception as e:
            self.err_info(str(e))

    # 从属性列表中读取属性个数和属性名并返回
    def get_attr(self):
        v_array = []
        attrNum = self.left_listWidget.count()
        for i in range(attrNum):
            item = self.left_listWidget.item(i).text()
            v_array.append(item)
        v_array.sort()  # 排序是为了防止在界面列表栏拖动元素的时候使元素位置变化造成结果不一样
        return attrNum, v_array

    # 右边属性列表中的元素添加到左边
    def move2left(self):
        items = []
        selected = self.right_listWidget.selectedItems()
        for item in selected:
            items.append(item.text())
            self.right_listWidget.takeItem(self.right_listWidget.row(item))
        self.left_listWidget.addItems(items)

    # 左边属性列表中的元素添加到右边
    def move2right(self):
        items = []
        selected = self.left_listWidget.selectedItems()
        for item in selected:
            items.append(item.text())
            self.left_listWidget.takeItem(self.left_listWidget.row(item))
        self.right_listWidget.addItems(items)

    def watermarkInsert(self):  # 点击添加按钮后执行此函数
        attrNum, v_array = self.get_attr()
        # 水印添加时禁用所有组件
        self.widget.setEnabled(False)
        # 使用多线程处理比较耗费时间的水印添加过程
        self.insert = InsertThread(self.scale_lineEdit.text(), attrNum, v_array, self.lsb_lineEdit.text())
        self.progressBar.setValue(0)
        # self.time_start = time.time()
        self.insert.pb_signal.connect(self.update_pb)
        self.insert.err_signal.connect(self.err_info)
        self.insert.dialogInfo_signal.connect(self.finishDialog)
        self.insert.start()

    def watermarkDetect(self):
        attrNum, v_array = self.get_attr()
        # 水印检测时禁用所有组件
        self.widget.setEnabled(False)
        # 使用多线程处理比较耗费时间的水印添加过程
        self.detect = DetectThread(self.scale_lineEdit.text(), attrNum, v_array, self.lsb_lineEdit.text(),
                                   self.threshold_lineEdit.text())
        self.progressBar.setValue(0)
        self.detect.pb_signal.connect(self.update_pb)
        self.detect.err_signal.connect(self.err_info)
        self.detect.dialogInfo_signal.connect(self.finishDialog)
        self.detect.start()

    def update_pb(self, val):
        self.progressBar.setValue(int(val))

    def err_info(self, info):
        QMessageBox.critical(self, 'Error!', info)
        self.widget.setEnabled(True)

    def finishDialog(self, info):
        QMessageBox.information(self, '操作完成', info, QMessageBox.Ok, QMessageBox.Ok)
        self.widget.setEnabled(True)  # 水印添加完成后恢复所有组件状态


# 启用水印插入多线程类
class InsertThread(QThread):
    pb_signal = pyqtSignal(str)
    err_signal = pyqtSignal(str)
    dialogInfo_signal = pyqtSignal(str)

    def __init__(self, scale, attrNum, v_array, lsb):
        super(InsertThread, self).__init__()
        self.scale = scale
        self.attrNum = attrNum
        self.lsb = lsb
        self.v_array = v_array

    def run(self):
        global cur_tb, db, pk_index, pk_name, v_dict
        time_start = time.time()
        # sql = 'desc ' + cur_tb  # 查询当前表下的所有属性
        # cursor.execute(sql)
        # res = cursor.fetchall()  # 获取查询结果
        # li = ['float', 'double', 'decimal']
        # v_array = []  # 可添加水印属性列表
        # maxAttrNum = 0  # 可用来添加水印的最大属性数量
        # for i, j in enumerate(res):
        #     if j[3] == 'PRI':
        #         pk_index = i  # 记录属性为主键的索引
        #     else:
        #         if j[1] in li:
        #             v_array.append(i)
        #             maxAttrNum += 1
        # # print('primary_key is:[' + res[pk_index][0] + '], and available attribution is:',[res[x][0] for x in v_array])
        # pk_name = res[pk_index][0]  # 主键属性名
        # self.progressBar.setValue(0)  # 进度条清空
        sql = 'SELECT * FROM ' + cur_tb
        try:
            cursor.execute(sql)
            rowcount = cursor.rowcount
            pb_val = cur_count = 0  # 与进度条相关
            pk_li = cursor.fetchall()  # 查询表中所有数据
            for value in pk_li:  # 遍历每一条数据
                # 密钥和主键值进行串接后做二次哈希运算（HMAC运算，直接套用库函数），返回字符串类型
                # print(cur_count,value)
                h = hmac.new(key, str(value[pk_index]).encode('utf-8'), digestmod='MD5').hexdigest()
                if not self.hmac_mod(h, self.scale):  # 判断哈希值对水印比例系数取模后是否为0
                    attr_index = self.hmac_mod(h, self.attrNum)
                    attr_name = self.v_array[attr_index]
                    bit_index = self.hmac_mod(h, self.lsb)
                    new_data = self.mark(value[pk_index], value[v_dict[self.v_array[attr_index]]], bit_index)
                    sql = 'UPDATE ' + cur_tb + ' SET ' + attr_name + '=' + str(
                        new_data) + ' WHERE ' + pk_name + '=' + str(value[pk_index])
                    # 为了防止对数据库误修改 初步测试时建议只输出不UPDATE
                    # print(sql)
                    self.update_db(sql)
                cur_count += 1
                # 只有在进度整数值变化时才发射信号，避免信号发射频繁造成主界面开销过大而无响应
                pb_NewVal = int(cur_count / rowcount * 100.0)
                if pb_NewVal == pb_val + 1:
                    self.pb_signal.emit(str(pb_NewVal))
                    pb_val = pb_NewVal
                # self.progressBar.setValue(cur_count / rowcount * 100)
            db.commit()
            time_end = time.time()
            self.dialogInfo_signal.emit('水印添加成功！\n总用时：%.4fs' % (time_end - time_start))
            # QMessageBox.information(self, '添加成功', '水印添加成功！\n总用时：%.4fs' % (time_end - time_start), QMessageBox.Ok,
            #                          QMessageBox.Ok)
        except Exception as e:
            self.err_signal.emit(str(e))
            # QMessageBox.critical(self, 'Error', str(e))

    def hmac_mod(self, hmac_str, mod_num):  # 对HMAC值进行取模运算
        res = 0
        for ch in hmac_str:
            res = (res * 16 + int(ch, 16)) % int(str(mod_num), 10)
        return res

    def first_hash_calc(self, pk_value):  # 密钥和主键串接后的一层哈希计算
        hash_value = hashlib.md5()
        hash_value.update(key + str(pk_value).encode('utf-8'))
        return self.hmac_mod(hash_value.hexdigest(), 2)

    def float2bin(self, f):  # 浮点数转换为64位二进制数，返回二进制字符串
        return bin(struct.unpack('!Q', struct.pack('!d', f))[0])[2:].zfill(64)

    def bin2float(self, b):  # 64位二进制字符串转换为浮点数，返回类型为float
        return struct.unpack('>d', int(b, 2).to_bytes(8, byteorder="big"))[0]

    def mark(self, pk_value, attr_value, bit_index):  # 对选中元组的对应属性的值进行修改（水印添加）
        global key
        # print(type(attr_value), attr_value, bit_index)
        # 基本思路：接收浮点数并转换为二进制字符串，将比特串按修改比特位的位置进行分割，
        # 修改对应比特位的数值后再连接，将连接后的比特串再转回浮点数并返回
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

    def update_db(self, sql):  # 执行SQL更新操作
        try:
            cursor.execute(sql)
            # db.commit()
        except Exception as e:
            self.err_signal.emit('DateBase Error:' + str(e))
            db.rollback()


# 启用水印检测多线程类
class DetectThread(QThread):
    pb_signal = pyqtSignal(str)
    err_signal = pyqtSignal(str)
    dialogInfo_signal = pyqtSignal(str)

    def __init__(self, scale, attrNum, v_array, lsb, threshold):
        super(DetectThread, self).__init__()
        self.scale = scale
        self.attrNum = attrNum
        self.v_array = v_array
        self.lsb = lsb
        self.threshold = threshold

    def run(self):
        global cur_tb, db, v_dict
        time_start = time.time()
        # sql = 'desc ' + cur_tb  # 查询当前表下的所有属性
        # cursor.execute(sql)
        # res = cursor.fetchall()  # 获取查询结果
        # li = ['float', 'double', 'decimal']
        # v_array = []  # 可添加水印属性列表
        # maxAttrNum = 0  # 可用来添加水印的最大属性数量
        # for i, j in enumerate(res):
        #     if j[3] == 'PRI':
        #         pk_index = i  # 记录属性为主键的索引
        #     else:
        #         if j[1] in li:
        #             v_array.append(i)
        #             maxAttrNum += 1
        # print('primary_key is:[' + res[pk_index][0] + '], and available attribution is:',[res[x][0] for x in v_array])
        # self.progressBar.setValue(0)  # 进度条清空
        sql = 'SELECT * FROM ' + cur_tb
        try:
            cursor.execute(sql)
            rowcount = cursor.rowcount
            totalCount = matchCount = 0  # 命中总数和命中中正确个数
            pb_val = cur_count = 0  # 与进度条有关
            pk_li = cursor.fetchall()  # 查询表中所有数据
            db.commit()
            for value in pk_li:  # 遍历每一条数据
                # 密钥和主键值进行串接后做二次哈希运算（HMAC运算，直接套用库函数），返回字符串类型
                # print(cur_count,value)
                h = hmac.new(key, str(value[pk_index]).encode('utf-8'), digestmod='MD5').hexdigest()
                if not self.hmac_mod(h, self.scale):  # 判断哈希值对水印比例系数取模后是否为0
                    attr_index = self.hmac_mod(h, self.attrNum)
                    bit_index = self.hmac_mod(h, self.lsb)
                    matchCount = matchCount + self.detect(value[pk_index], value[v_dict[self.v_array[attr_index]]],
                                                          bit_index)
                    totalCount += 1
                cur_count += 1
                # 只有在进度整数值变化时才发射信号，避免信号发射频繁造成主界面开销过大而无响应
                pb_NewVal = int(cur_count / rowcount * 100.0)
                if pb_NewVal == pb_val + 1:
                    self.pb_signal.emit(str(pb_NewVal))
                    pb_val = pb_NewVal
                # self.progressBar.setValue(cur_count / rowcount * 100.0)
        except Exception as e:
            self.err_signal.emit(str(e))
            # QMessageBox.critical(self, 'Error', str(e))
        # db.commit()
        time_end = time.time()
        matchRatio = matchCount / totalCount
        if matchRatio >= (float(self.threshold)) / 100.0:
            self.dialogInfo_signal.emit(
                '水印检测完毕！\n该数据表添加过水印！\n检测数：%d  匹配数：%d \n匹配率：%.2f%%\n总用时：%.4fs' % (
                    totalCount, matchCount, matchRatio * 100, time_end - time_start))
            # QMessageBox.information(self, '检测完成', '水印检测完毕！\n该数据表添加过水印！\n检测数：%d 匹配数： %d \n总用时：%.4fs' % (
            #     totalCount, matchCount, time_end - time_start), QMessageBox.Ok,
            #                         QMessageBox.Ok)
        else:
            self.dialogInfo_signal.emit(
                "水印检测完毕！\n该数据表未添加过水印！\n检测数：%d  匹配数：%d \n匹配率：%.2f%%\n总用时：%.4fs" % (
                    totalCount, matchCount, matchRatio * 100, time_end - time_start))
            # QMessageBox.information(self, '检测完成', '水印检测完毕！\n该数据表未添加过水印！\n检测数：%d 匹配数： %d \n总用时：%.4fs' % (
            #     totalCount, matchCount, time_end - time_start), QMessageBox.Ok,
            #                         QMessageBox.Ok)

    def detect(self, pk_value, attr_value, bit_index):
        attr_binVal = self.float2bin(attr_value)
        if self.first_hash_calc(pk_value):
            bit_val = '1'
        else:
            bit_val = '0'
        if attr_binVal[-(bit_index + 1)] == bit_val:
            return 1
        else:
            return 0

    def hmac_mod(self, hmac_str, mod_num):  # 对HMAC值进行取模运算
        res = 0
        for ch in hmac_str:
            res = (res * 16 + int(ch, 16)) % int(str(mod_num), 10)
        return res

    def first_hash_calc(self, pk_value):  # 密钥和主键串接后的一层哈希计算
        hash_value = hashlib.md5()
        hash_value.update(key + str(pk_value).encode('utf-8'))
        return self.hmac_mod(hash_value.hexdigest(), 2)

    def float2bin(self, f):  # 浮点数转换为64位二进制数，返回二进制字符串
        return bin(struct.unpack('!Q', struct.pack('!d', f))[0])[2:].zfill(64)


# 数据库登录窗口类
class LoginForm(QDialog, Ui_Login_Form):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.login)  # 槽函数，点击按钮后登陆

    def login(self):
        global db, username, hostname, password
        username = self.user_lineEdit.text()
        if not username:  # 不输入username则默认以root登陆
            self.user_lineEdit.setText('root')
            username = 'root'
        hostname = self.host_lineEdit.text()
        if not hostname:  # 不输入hostname则默认连接localhost登陆
            self.host_lineEdit.setText('localhost')
            hostname = 'localhost'
        password = self.pwd_lineEdit.text()
        # 使用pymysql模块进行数据库的连接
        try:
            db = pymysql.connect(hostname, username, password)
            QMessageBox.information(self, 'Database connection', 'Database connection success.')  # 弹出数据库连接成功提示框
            self.accept()  # 关闭登陆，并给主窗口返回True
        except pymysql.Error as e:
            QMessageBox.critical(self, 'Database Connection', e.args[1])  # 弹出数据库连接错误提示


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyMainForm()
    main.show()  # 启动主界面
    main.openForm()  # 默认启动时打开登录框
    sys.exit(app.exec_())
