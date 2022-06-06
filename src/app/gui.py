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
import future_rehs
import cancel


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
        self.show_button.clicked.connect(self.show_rehs)

    def show_room(self):
        item = self.rooms_list.currentItem()
        tmp = item.text().split(". ")
        self.window = Book(self.conn, int(tmp[0]), self.acc_id)
        self.window.show()

    def show_rehs(self):
        self.window = FutureRehs(self.conn, self.acc_id)
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
            dlg.setWindowTitle("Готово")
            dlg.setText("Репетиция успешно забронирована")
            dlg.exec()


class FutureRehs(QtWidgets.QMainWindow, future_rehs.Ui_MainWindow):
    def __init__(self, conn, acc_id):
        super().__init__()
        self.setupUi(self)
        rehs = connect.get_all_rehs(conn, acc_id)
        i = 0
        for reh in rehs:
            text = str(reh[0]) + ". " + reh[2] + " - " + str(reh[1]) + \
                   " (" + str(reh[3]) + " р. за 3 часа)"
            self.rehs_list.insertItem(i, text)
            i += 1
        self.conn = conn

        self.rehs_list.clicked.connect(self.show_reh)

    def show_reh(self):
        item = self.rehs_list.currentItem()
        tmp = item.text().split(". ")
        self.window = Cancel(self.conn, int(tmp[0]))
        self.window.show()


class Cancel(QtWidgets.QMainWindow, cancel.Ui_MainWindow):
    def __init__(self, conn, reh_id):
        super().__init__()
        self.setupUi(self)
        reh = connect.reh_info(conn, reh_id)
        text = "Дата репетиции: " + str(reh[0][0]) + "\n"
        text += "Комната: " + reh[0][1] + "\n"
        text += "Тип: " + reh[0][2] + "\n"
        text += "Площадь: " + str(reh[0][3]) + " м^2\n"
        text += "Стоимость: " + str(reh[0][4]) + " р. за 3 часа\n"
        text += "Репетиционная база: " + reh[0][5] + "\n"
        text += "Адрес: " + reh[0][6] + "\n"
        text += "Контакты: " + reh[0][7] + " " + reh[0][8]
        label = QtWidgets.QLabel()
        label.setText(text)
        self.reh_scroll.setWidget(label)
        self.conn = conn
        self.reh_id = reh_id

        self.cancel_button.clicked.connect(self.cancel)

    def cancel(self):
        connect.cancel(self.conn, self.reh_id)
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Готово")
        dlg.setText("Репетиция успешно отменена")
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
