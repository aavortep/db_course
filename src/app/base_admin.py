# Form implementation generated from reading ui file 'base_admin.ui'
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
        self.base_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.base_scroll.setGeometry(QtCore.QRect(270, 120, 261, 281))
        self.base_scroll.setWidgetResizable(True)
        self.base_scroll.setObjectName("base_scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 259, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.base_scroll.setWidget(self.scrollAreaWidgetContents)
        self.del_button = QtWidgets.QPushButton(self.centralwidget)
        self.del_button.setGeometry(QtCore.QRect(270, 410, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_button.setFont(font)
        self.del_button.setStyleSheet("background-color: rgb(255, 85, 0);\n"
"color: rgb(255, 255, 255);")
        self.del_button.setObjectName("del_button")
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
        self.del_button.setText(_translate("MainWindow", "Удалить реп. базу"))
