import connect
import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
import welcome, sign_in, sign_up
import musician_main, owner_main, admin_main
import book, cancel
import future_rehs, rehs_on_base, base_info
import add_room, add_gear, reg_base


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
        rehs = connect.get_rehs(conn, acc_id)
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
        bases = connect.get_bases(self.conn, acc_id)
        i = 0
        for base in bases:
            text = str(base[0]) + ". " + base[1] + " (адрес: " + base[2] + ")"
            self.bases_list.insertItem(i, text)
            i += 1
        self.acc_id = acc_id

        self.bases_list.clicked.connect(self.show_base)
        self.reg_button.clicked.connect(self.reg_base)

    def show_base(self):
        item = self.bases_list.currentItem()
        tmp = item.text().split(". ")
        self.window = BaseInfo(self.conn, int(tmp[0]))
        self.window.show()

    def reg_base(self):
        self.window = RegBase(self.conn, self.acc_id)
        self.window.show()

    def closeEvent(self, event):
        self.conn.close()
        print("Owner connection closed")
        event.accept()


class RegBase(QtWidgets.QMainWindow, reg_base.Ui_MainWindow):
    def __init__(self, conn, acc_id):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.acc_id = acc_id

        self.reg_button.clicked.connect(self.reg_base)

    def reg_base(self):
        base = connect.RehBase()
        base.owner_id = self.acc_id
        base.name = self.name_edit.text()
        base.address = self.adress_edit.text()
        base.phone = self.phone_edit.text()
        base.mail = self.mail_edit.text()
        if base.name == "" or base.address == "" or base.phone == "" or base.mail == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Пожалуйста, заполните все поля ввода")
            dlg.exec()
        elif connect.reg_base(self.conn, base) == 1:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Репетиционная база уже существует")
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Готово")
            dlg.setText("Репетиционная база успешно добавлена")
            dlg.exec()


class BaseInfo(QtWidgets.QMainWindow, base_info.Ui_MainWindow):
    def __init__(self, conn, base_id):
        super().__init__()
        self.setupUi(self)
        base = connect.base_info(conn, base_id)
        rooms = connect.rooms_by_base(conn, base_id)
        text = "Название базы: " + base[0][0] + "\n"
        text += "Адрес: " + base[0][1] + "\n"
        text += "Контакты: " + base[0][2] + " " + base[0][3] + "\n"
        text += "Комнаты:\n"
        i = 1
        for room in rooms:
            text += "[" + str(i) + "] " + room[1] + " (" + room[2] + ")\n"
            text += "Оборудование в этой комнате:\n"
            gear = connect.gear_by_room(conn, room[0])
            j = 1
            for g in gear:
                text += str(j) + ". " + g[0] + " - " + g[1] + " (" + str(g[2]) + " шт.)\n"
                j += 1
            i += 1
        label = QtWidgets.QLabel()
        label.setText(text)
        self.base_scroll.setWidget(label)
        self.conn = conn
        self.base_id = base_id

        self.add_room_button.clicked.connect(self.add_room)
        self.add_equip_button.clicked.connect(self.add_gear)
        self.show_button.clicked.connect(self.show_rehs)
        self.del_button.clicked.connect(self.del_base)

    def add_room(self):
        self.window = AddRoom(self.conn, self.base_id)
        self.window.show()

    def add_gear(self):
        self.window = AddGear(self.conn, self.base_id)
        self.window.show()

    def show_rehs(self):
        self.window = RehsOnBase(self.conn, self.base_id)
        self.window.show()

    def del_base(self):
        connect.del_base(self.conn, self.base_id)
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Готово")
        dlg.setText("Репетиционная база успешно удалена")
        dlg.exec()


class AddRoom(QtWidgets.QMainWindow, add_room.Ui_MainWindow):
    def __init__(self, conn, base_id):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.base_id = base_id

        self.add_button.clicked.connect(self.add_room)

    def add_room(self):
        room = connect.Room()
        room.base_id = self.base_id
        room.name = self.name_edit.text()
        if self.band_radio.isChecked():
            room.type = "band"
        elif self.vocal_radio.isChecked():
            room.type = "vocal"
        else:
            room.type = "drum"
        room.area = int(self.area_spin.text())
        room.cost = int(self.cost_spin.text())
        if room.name == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Пожалуйста, заполните все поля ввода")
            dlg.exec()
        elif connect.add_room(self.conn, room) == 1:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Комната уже существует")
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Готово")
            dlg.setText("Комната успешно добавлена")
            dlg.exec()


class AddGear(QtWidgets.QMainWindow, add_gear.Ui_MainWindow):
    def __init__(self, conn, base_id):
        super().__init__()
        self.setupUi(self)
        self.conn = conn
        self.base_id = base_id

        self.add_button.clicked.connect(self.add_gear)

    def add_gear(self):
        gear = connect.Gear()
        room_name = self.name_edit.text()
        if self.amp_radio.isChecked():
            gear.type = "amp"
        elif self.mic_radio.isChecked():
            gear.type = "mic"
        elif self.drums_radio.isChecked():
            gear.type = "drums"
        elif self.commut_radio.isChecked():
            gear.type = "commutation"
        else:
            gear.type = "pedal"
        gear.brand = self.brand_edit.text()
        gear.amount = int(self.amount_spin.text())
        if room_name == "" or gear.brand == "":
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Пожалуйста, заполните все поля ввода")
            dlg.exec()
        elif connect.add_gear(self.conn, gear, room_name, self.base_id) == 1:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка")
            dlg.setText("Такое оборудование в этой комнате уже есть")
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Готово")
            dlg.setText("Оборудование успешно добавлено")
            dlg.exec()


class RehsOnBase(QtWidgets.QMainWindow, rehs_on_base.Ui_MainWindow):
    def __init__(self, conn, base_id):
        super().__init__()
        self.setupUi(self)
        rehs = connect.rehs_by_base(conn, base_id)
        i = 0
        for reh in rehs:
            text = str(reh[0]) + ". " + str(reh[1]) + " - " + reh[2] + " (" + reh[3] + ")"
            self.rehs_list.insertItem(i, text)
            i += 1
        self.conn = conn

        self.rehs_list.clicked.connect(self.show_reh)

    def show_reh(self):
        item = self.rehs_list.currentItem()
        tmp = item.text().split(". ")
        self.window = Cancel(self.conn, int(tmp[0]))
        self.window.show()


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
