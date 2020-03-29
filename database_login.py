# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'database_login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login_Form(object):
    def setupUi(self, Login_Form):
        Login_Form.setObjectName("Login_Form")
        Login_Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Login_Form.resize(340, 150)
        Login_Form.setMinimumSize(QtCore.QSize(340, 150))
        Login_Form.setMaximumSize(QtCore.QSize(340, 150))
        self.Login = QtWidgets.QWidget(Login_Form)
        self.Login.setGeometry(QtCore.QRect(20, 20, 305, 111))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Login.sizePolicy().hasHeightForWidth())
        self.Login.setSizePolicy(sizePolicy)
        self.Login.setObjectName("Login")
        self.label = QtWidgets.QLabel(self.Login)
        self.label.setGeometry(QtCore.QRect(10, 14, 54, 12))
        self.label.setObjectName("label")
        self.user_lineEdit = QtWidgets.QLineEdit(self.Login)
        self.user_lineEdit.setGeometry(QtCore.QRect(80, 10, 113, 20))
        self.user_lineEdit.setObjectName("user_lineEdit")
        self.pwd_lineEdit = QtWidgets.QLineEdit(self.Login)
        self.pwd_lineEdit.setGeometry(QtCore.QRect(80, 73, 113, 20))
        self.pwd_lineEdit.setStatusTip("")
        self.pwd_lineEdit.setWhatsThis("")
        self.pwd_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_lineEdit.setCursorPosition(0)
        self.pwd_lineEdit.setObjectName("pwd_lineEdit")
        self.host_lineEdit = QtWidgets.QLineEdit(self.Login)
        self.host_lineEdit.setGeometry(QtCore.QRect(80, 43, 113, 20))
        self.host_lineEdit.setObjectName("host_lineEdit")
        self.login_pushButton = QtWidgets.QPushButton(self.Login)
        self.login_pushButton.setGeometry(QtCore.QRect(220, 70, 75, 23))
        self.login_pushButton.setObjectName("login_pushButton")
        self.label_3 = QtWidgets.QLabel(self.Login)
        self.label_3.setGeometry(QtCore.QRect(10, 45, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.Login)
        self.label_2.setGeometry(QtCore.QRect(10, 77, 54, 12))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Login_Form)
        self.user_lineEdit.returnPressed.connect(self.login_pushButton.click)
        self.pwd_lineEdit.returnPressed.connect(self.login_pushButton.click)
        self.host_lineEdit.returnPressed.connect(self.login_pushButton.click)
        QtCore.QMetaObject.connectSlotsByName(Login_Form)
        Login_Form.setTabOrder(self.user_lineEdit, self.host_lineEdit)
        Login_Form.setTabOrder(self.host_lineEdit, self.pwd_lineEdit)
        Login_Form.setTabOrder(self.pwd_lineEdit, self.login_pushButton)

    def retranslateUi(self, Login_Form):
        _translate = QtCore.QCoreApplication.translate
        Login_Form.setWindowTitle(_translate("Login_Form", "Login"))
        self.label.setText(_translate("Login_Form", "Username"))
        self.user_lineEdit.setPlaceholderText(_translate("Login_Form", "root"))
        self.host_lineEdit.setPlaceholderText(_translate("Login_Form", "localhost"))
        self.login_pushButton.setText(_translate("Login_Form", "Login"))
        self.label_3.setText(_translate("Login_Form", "Hostname"))
        self.label_2.setText(_translate("Login_Form", "Password"))
