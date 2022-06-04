import connect
import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
import welcome
import sign_in
import sign_up
import musician_main
import owner_main
import admin_main
import book


class Welcome(QtWidgets.QMainWindow, welcome.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.signin_button.clicked.connect(self.sign_in)
        self.signup_button.clicked.connect(self.sign_up)

    def sign_in(self):
        self.window = SignIn()
        self.window.show()

    def sign_up(self):
        self.window = SignUp()
        self.window.show()


class SignIn(QtWidgets.QMainWindow, sign_in.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.signin_button.clicked.connect(self.get_data)

    def get_data(self):
        mail = self.mail_edit.text()
        password = self.password_edit.text()
        if mail == "" or password == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Пожалуйста, заполните все поля ввода")
            dlg.exec()
        else:
            acc = connect.sign_in(mail, password)
            if acc.id == -1:
                dlg = QtWidgets.QMessageBox(self)
                dlg.setWindowTitle("Ошибка")
                dlg.setText("Неправильный email или пароль")
                dlg.exec()
            elif acc.type == "musician":
                self.window = MusicianMain(acc.id)
                self.window.show()
            elif acc.type == "owner":
                self.window = OwnerMain(acc.id)
                self.window.show()
            else:
                self.window = AdminMain(acc.id)
                self.window.show()


class SignUp(QtWidgets.QMainWindow, sign_up.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.signup_button.clicked.connect(self.get_data)

    def get_data(self):
        acc = connect.Account()
        acc.fio = self.fio_edit.text()
        acc.phone = self.phone_edit.text()
        acc.mail = self.mail_edit.text()
        acc.password = self.password_edit.text()
        if self.musician_radio.isChecked():
            acc.type = "musician"
        else:
            acc.type = "owner"
        if acc.fio == "" or acc.phone == "" or acc.mail == "" or acc.password == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Пожалуйста, заполните все поля ввода")
            dlg.exec()
        elif connect.sign_up(acc) == 1:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Аккаунт уже существует")
            dlg.exec()
        elif acc.type == "musician":
            self.window = MusicianMain(acc.id)
            self.window.show()
        else:
            self.window = OwnerMain(acc.id)
            self.window.show()


class MusicianMain(QtWidgets.QMainWindow, musician_main.Ui_MainWindow):
    def __init__(self, acc_id):
        super().__init__()
        self.setupUi(self)
        self.conn = connect.connect_musician()
        rooms = connect.get_all_rooms(self.conn)
        i = 0
        for room in rooms:
            text = str(room[0]) + ". " + room[1] + " (" + room[4] + ") - " + room[2] + ", " + \
                   str(room[3]) + " р за 3 ч"
            self.rooms_list.insertItem(i, text)
            i += 1
        self.acc_id = acc_id

        self.rooms_list.clicked.connect(self.show_room)

    def show_room(self):
        item = self.rooms_list.currentItem()
        tmp = item.text().split(". ")
        self.window = Book(self.conn, int(tmp[0]), self.acc_id)
        self.window.show()

    def closeEvent(self, event):
        self.conn.close()
        print("Musician connection closed")
        event.accept()


class Book(QtWidgets.QMainWindow, book.Ui_MainWindow):
    def __init__(self, conn, room_id, acc_id):
        super().__init__()
        self.setupUi(self)
        room = connect.room_info(conn, room_id)
        gear = connect.gear_info(conn, room_id)
        text = "Репетиционная база: " + room[0][4] + "\n"
        text += "Адрес: " + room[0][5] + "\n"
        text += "Комната: " + room[0][0] + " (" + room[0][1] + ") - " + \
                str(room[0][2]) + " м^2\n"
        text += "Стоимость: " + str(room[0][3]) + " р. за 3 часа\n"
        text += "Оборудование:\n"
        for item in gear:
            text += item[0] + " - " + item[1] + " (" + str(item[2]) + " шт)\n"
        label = QtWidgets.QLabel()
        label.setText(text)
        self.room_scroll.setWidget(label)
        self.room_id = room_id
        self.acc_id = acc_id
        self.conn = conn

        self.book_button.clicked.connect(self.book_reh)

    def book_reh(self):
        reh = connect.Rehearsal()
        reh.musician_id = self.acc_id
        reh.room_id = self.room_id
        date = self.dateTimeEdit.dateTime().date()
        right_format = str(date.year()) + "-0" + str(date.month()) + \
                       "-0" + str(date.day()) + " 0"
        time = self.dateTimeEdit.dateTime().time()
        right_format += str(time.hour()) + ":0" + str(time.minute()) + ":00"
        reh.date = right_format
        if connect.book(self.conn, reh) == 1:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Извините. Комната на это время уже занята")
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Репетиция успешно забронирована")
            dlg.exec()


class OwnerMain(QtWidgets.QMainWindow, owner_main.Ui_MainWindow):
    def __init__(self, acc_id):
        super().__init__()
        self.setupUi(self)
        self.conn = connect.connect_owner()

    def closeEvent(self, event):
        self.conn.close()
        print("Owner connection closed")
        event.accept()


class AdminMain(QtWidgets.QMainWindow, admin_main.Ui_MainWindow):
    def __init__(self, acc_id):
        super().__init__()
        self.setupUi(self)
        self.conn = connect.connect_admin()

    def closeEvent(self, event):
        self.conn.close()
        print("Admin connection closed")
        event.accept()


def main():
    #connection = connect.connect()
    app = QtWidgets.QApplication(sys.argv)
    window = Welcome()
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
    #connection.close()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


# menu(connection)
