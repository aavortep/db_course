# Form implementation generated from reading ui file 'admin_main.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mail_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.mail_edit.setGeometry(QtCore.QRect(260, 240, 171, 20))
        self.mail_edit.setObjectName("mail_edit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 240, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.find_acc_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_acc_button.setGeometry(QtCore.QRect(450, 240, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.find_acc_button.setFont(font)
        self.find_acc_button.setObjectName("find_acc_button")
        self.find_base_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_base_button.setGeometry(QtCore.QRect(450, 270, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.find_base_button.setFont(font)
        self.find_base_button.setObjectName("find_base_button")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 270, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.name_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.name_edit.setGeometry(QtCore.QRect(260, 270, 171, 20))
        self.name_edit.setObjectName("name_edit")
        self.date_edit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.date_edit.setGeometry(QtCore.QRect(260, 300, 171, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.date_edit.setFont(font)
        self.date_edit.setDate(QtCore.QDate(2022, 6, 1))
        self.date_edit.setObjectName("date_edit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 300, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.find_reh_button = QtWidgets.QPushButton(self.centralwidget)
        self.find_reh_button.setGeometry(QtCore.QRect(450, 300, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.find_reh_button.setFont(font)
        self.find_reh_button.setObjectName("find_reh_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
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
        self.label.setText(_translate("MainWindow", "Почта:"))
        self.find_acc_button.setText(_translate("MainWindow", "Найти аккаунт"))
        self.find_base_button.setText(_translate("MainWindow", "Найти реп. базу"))
        self.label_2.setText(_translate("MainWindow", "Название:"))
        self.label_3.setText(_translate("MainWindow", "Дата:"))
        self.find_reh_button.setText(_translate("MainWindow", "Найти репетицию"))