# Form implementation generated from reading ui file 'add_gear.ui'
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
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(310, 360, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_button.setFont(font)
        self.add_button.setObjectName("add_button")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 260, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 230, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.brand_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.brand_edit.setGeometry(QtCore.QRect(310, 230, 221, 20))
        self.brand_edit.setObjectName("brand_edit")
        self.amount_spin = QtWidgets.QSpinBox(self.centralwidget)
        self.amount_spin.setGeometry(QtCore.QRect(310, 260, 41, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.amount_spin.setFont(font)
        self.amount_spin.setMinimum(1)
        self.amount_spin.setMaximum(5)
        self.amount_spin.setObjectName("amount_spin")
        self.mic_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.mic_radio.setGeometry(QtCore.QRect(310, 290, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mic_radio.setFont(font)
        self.mic_radio.setChecked(True)
        self.mic_radio.setObjectName("mic_radio")
        self.amp_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.amp_radio.setGeometry(QtCore.QRect(310, 310, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.amp_radio.setFont(font)
        self.amp_radio.setObjectName("amp_radio")
        self.drums_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.drums_radio.setGeometry(QtCore.QRect(310, 330, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.drums_radio.setFont(font)
        self.drums_radio.setObjectName("drums_radio")
        self.pedal_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.pedal_radio.setGeometry(QtCore.QRect(420, 310, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pedal_radio.setFont(font)
        self.pedal_radio.setObjectName("pedal_radio")
        self.commut_radio = QtWidgets.QRadioButton(self.centralwidget)
        self.commut_radio.setGeometry(QtCore.QRect(420, 290, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.commut_radio.setFont(font)
        self.commut_radio.setObjectName("commut_radio")
        self.name_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.name_edit.setGeometry(QtCore.QRect(310, 200, 221, 20))
        self.name_edit.setObjectName("name_edit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(170, 200, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
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
        self.add_button.setText(_translate("MainWindow", "Добавить"))
        self.label_2.setText(_translate("MainWindow", "Количество:"))
        self.label_3.setText(_translate("MainWindow", "Бренд:"))
        self.mic_radio.setText(_translate("MainWindow", "Микрофон"))
        self.amp_radio.setText(_translate("MainWindow", "Усилитель"))
        self.drums_radio.setText(_translate("MainWindow", "Ударные"))
        self.pedal_radio.setText(_translate("MainWindow", "Педаль"))
        self.commut_radio.setText(_translate("MainWindow", "Коммутация"))
        self.label_4.setText(_translate("MainWindow", "Название комнаты:"))
