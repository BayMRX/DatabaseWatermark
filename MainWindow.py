# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 370, 681, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 691, 351))
        self.widget.setObjectName("widget")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 671, 71))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.tb_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.tb_comboBox.setGeometry(QtCore.QRect(350, 30, 111, 22))
        self.tb_comboBox.setObjectName("tb_comboBox")
        self.tb_comboBox.addItem("")
        self.login_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.login_pushButton.setGeometry(QtCore.QRect(10, 30, 71, 23))
        self.login_pushButton.setObjectName("login_pushButton")
        self.db_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.db_comboBox.setGeometry(QtCore.QRect(160, 30, 105, 20))
        self.db_comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.db_comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.db_comboBox.setObjectName("db_comboBox")
        self.db_comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(110, 33, 51, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(300, 33, 51, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(495, 33, 31, 16))
        self.label_3.setObjectName("label_3")
        self.key_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.key_lineEdit.setGeometry(QtCore.QRect(530, 30, 81, 20))
        self.key_lineEdit.setReadOnly(True)
        self.key_lineEdit.setObjectName("key_lineEdit")
        self.key_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.key_pushButton.setGeometry(QtCore.QRect(622, 29, 41, 23))
        self.key_pushButton.setObjectName("key_pushButton")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 100, 671, 61))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(20, 30, 101, 16))
        self.label_6.setObjectName("label_6")
        self.scale_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.scale_lineEdit.setGeometry(QtCore.QRect(121, 28, 51, 20))
        self.scale_lineEdit.setObjectName("scale_lineEdit")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(250, 30, 61, 16))
        self.label_7.setObjectName("label_7")
        self.attrNum_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.attrNum_lineEdit.setGeometry(QtCore.QRect(313, 28, 61, 20))
        self.attrNum_lineEdit.setObjectName("attrNum_lineEdit")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(430, 30, 81, 16))
        self.label_8.setObjectName("label_8")
        self.lsb_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lsb_lineEdit.setGeometry(QtCore.QRect(520, 27, 61, 20))
        self.lsb_lineEdit.setObjectName("lsb_lineEdit")
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 180, 671, 80))
        self.groupBox_3.setObjectName("groupBox_3")
        self.add_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.add_pushButton.setGeometry(QtCore.QRect(260, 30, 75, 23))
        self.add_pushButton.setObjectName("add_pushButton")
        self.groupBox_4 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 270, 671, 71))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(65, 30, 31, 16))
        self.label_4.setObjectName("label_4")
        self.threshold_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.threshold_lineEdit.setGeometry(QtCore.QRect(105, 28, 51, 20))
        self.threshold_lineEdit.setObjectName("threshold_lineEdit")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(160, 30, 16, 16))
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName("label_5")
        self.detect_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.detect_pushButton.setGeometry(QtCore.QRect(260, 27, 75, 23))
        self.detect_pushButton.setObjectName("detect_pushButton")
        self.widget.raise_()
        self.progressBar.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "水印添加与检测"))
        self.groupBox.setTitle(_translate("MainWindow", "选择与连接"))
        self.tb_comboBox.setItemText(0, _translate("MainWindow", "请先选择数据库"))
        self.login_pushButton.setToolTip(_translate("MainWindow", "点击登陆MySQL"))
        self.login_pushButton.setText(_translate("MainWindow", "登录MySQL"))
        self.db_comboBox.setItemText(0, _translate("MainWindow", "请先连接MySQL"))
        self.label.setText(_translate("MainWindow", "数据库："))
        self.label_2.setText(_translate("MainWindow", "数据表："))
        self.label_3.setText(_translate("MainWindow", "密钥："))
        self.key_pushButton.setText(_translate("MainWindow", "…"))
        self.groupBox_2.setTitle(_translate("MainWindow", "参数设置"))
        self.label_6.setText(_translate("MainWindow", "水印比例系数：1/"))
        self.label_7.setText(_translate("MainWindow", "属性个数："))
        self.label_8.setText(_translate("MainWindow", "不重要比特数："))
        self.groupBox_3.setTitle(_translate("MainWindow", "水印添加"))
        self.add_pushButton.setText(_translate("MainWindow", "添加"))
        self.groupBox_4.setTitle(_translate("MainWindow", "水印检测"))
        self.label_4.setText(_translate("MainWindow", "阈值："))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">%</span></p></body></html>"))
        self.detect_pushButton.setText(_translate("MainWindow", "检测"))
