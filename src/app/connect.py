import psycopg2
from psycopg2 import OperationalError
from datetime import datetime


class Account:
    id = -1
    fio = ""
    phone = ""
    mail = ""
    password = ""
    type = ""


class Rehearsal:
    id = -1
    musician_id = -1
    room_id = -1
    date = None


class Room:
    id = -1
    base_id = -1
    name = ""
    type = ""
    area = 0
    cost = 0


class Gear:
    id = -1
    room_id = -1
    type = ""
    brand = ""
    amount = 0


class RehBase:
    id = -1
    owner_id = -1
    name = ""
    address = ""
    phone = ""
    mail = ""


storedProc = '''
CALL change_status('web-site', 'wip', 'done');
SELECT *
FROM sch.Projects WHERE sch.Projects.ProjectType = 'web-site'
'''


def sign_in(mail, password):
    conn = connect()
    cur = conn.cursor()
    query = "select * from account where mail = %s and password = %s"
    cur.execute(query, (mail, password,))
    res = cur.fetchall()
    acc = Account()
    if len(res) != 0:
        acc.id = res[0][0]
        acc.fio = res[0][1]
        acc.phone = res[0][2]
        acc.mail = res[0][3]
        acc.password = res[0][4]
        acc.type = res[0][5]
    cur.close()
    conn.close()
    return acc


def sign_up(acc):
    conn = connect()
    cur = conn.cursor()
    query = "select * from account where mail = %s"
    cur.execute(query, (acc.mail,))
    res = cur.fetchall()
    if len(res) != 0:  # если аккаунт уже существует
        return 1

    query = "select * from account"
    cur.execute(query)
    res = cur.fetchall()
    acc.id = len(res) + 1

    query = "insert into account values (%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (acc.id, acc.fio, acc.phone, acc.mail, acc.password, acc.type,))
    conn.commit()
    cur.close()
    conn.close()
    return 0


def add_room(conn, room):
    cur = conn.cursor()
    query = "select * from room where baseid = %s and name = %s"
    cur.execute(query, (room.base_id, room.name,))
    res = cur.fetchall()
    if len(res) != 0:  # если комната уже существует
        return 1

    query = "select * from room"
    cur.execute(query)
    res = cur.fetchall()
    room.id = len(res) + 1

    query = "insert into room values (%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (room.id, room.base_id, room.name, room.type, room.area, room.cost,))
    conn.commit()
    cur.close()
    return 0


def add_gear(conn, gear, room_name, base_id):
    cur = conn.cursor()

    query = "select id from room where name = %s and baseid = %s"
    cur.execute(query, (room_name, base_id,))
    res = cur.fetchall()
    if len(res) == 0:  # если такой комнаты не существует
        return 2

    gear.room_id = res[0][0]

    query = "select * from equipment " \
            "where equipment.type = %s and equipment.brand = %s " \
            "and equipment.roomid = %s"
    cur.execute(query, (gear.type, gear.brand, gear.room_id,))
    res = cur.fetchall()
    if len(res) != 0:  # если такое оборудование в этой комнате уже существует
        return 1

    query = "select * from equipment"
    cur.execute(query)
    res = cur.fetchall()
    gear.id = len(res) + 1

    query = "insert into equipment values (%s, %s, %s, %s, %s)"
    cur.execute(query, (gear.id, gear.room_id, gear.type, gear.brand, gear.amount,))
    conn.commit()
    cur.close()
    return 0


def reg_base(conn, base):
    cur = conn.cursor()
    query = "select * from reh_base where address = %s and name = %s"
    cur.execute(query, (base.address, base.name,))
    res = cur.fetchall()
    if len(res) != 0:  # если репбаза уже существует
        return 1
    query = "select * from reh_base where mail = %s"
    cur.execute(query, (base.mail,))
    res = cur.fetchall()
    if len(res) != 0:  # если репбаза уже существует
        return 1

    query = "select * from reh_base"
    cur.execute(query)
    res = cur.fetchall()
    base.id = len(res) + 1

    query = "insert into reh_base values (%s, %s, %s, %s, %s, %s)"
    cur.execute(query, (base.id, base.owner_id, base.name, base.address,
                        base.phone, base.mail,))
    conn.commit()
    cur.close()
    return 0


def del_base(conn, base_id):
    cur = conn.cursor()
    query = "delete from reh_base where id = %s"
    cur.execute(query, (base_id,))
    conn.commit()
    cur.close()


def get_all_rooms(conn):
    cur = conn.cursor()
    query = "select room.id, room.name, room.type, room.cost, reh_base.name " \
            "from room join reh_base on room.baseid = reh_base.id"
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    return res


def get_rehs(conn, acc_id):
    cur = conn.cursor()
    query = "select rehearsal.id, rehearsal.rehdate, room.name, room.cost " \
            "from rehearsal join room on rehearsal.roomid = room.id " \
            "where rehearsal.musicianid = %s and rehearsal.rehdate >= current_timestamp"
    cur.execute(query, (acc_id,))
    res = cur.fetchall()
    cur.close()
    return res


def rehs_by_base(conn, base_id):
    cur = conn.cursor()
    query = "select rehearsal.id, rehearsal.rehdate, room.name, account.fio " \
            "from rehearsal join room on rehearsal.roomid = room.id " \
            "join account on rehearsal.musicianid = account.id " \
            "join reh_base on room.baseid = reh_base.id " \
            "where reh_base.id = %s and rehearsal.rehdate >= current_timestamp"
    cur.execute(query, (base_id,))
    res = cur.fetchall()
    cur.close()
    return res


def get_bases(conn, acc_id):
    cur = conn.cursor()
    query = "select id, name, address from reh_base where ownerid = %s"
    cur.execute(query, (acc_id,))
    res = cur.fetchall()
    cur.close()
    return res


def bases_by_name(conn, base_name):
    cur = conn.cursor()
    query = "select * from reh_base where name = %s"
    cur.execute(query, (base_name,))
    res = cur.fetchall()
    cur.close()
    return res


def rehs_by_date(conn, date):
    cur = conn.cursor()
    query = "select rehearsal.id, rehearsal.rehdate, room.name " \
            "from rehearsal join room on rehearsal.roomid = room.id " \
            "where rehearsal.rehdate = %s"
    cur.execute(query, (date,))
    res = cur.fetchall()
    cur.close()
    return res


def room_info(conn, room_id):
    cur = conn.cursor()
    query = "select room.name, room.type, room.area, room.cost, " \
            "reh_base.name, reh_base.address " \
            "from room join reh_base on room.baseid = reh_base.id " \
            "where room.id = %s"
    cur.execute(query, (room_id,))
    res = cur.fetchall()
    cur.close()
    return res


def gear_info(conn, room_id):
    cur = conn.cursor()
    query = "select eq.type, eq.brand, eq.amount " \
            "from equipment as eq " \
            "where eq.roomid = %s"
    cur.execute(query, (room_id,))
    res = cur.fetchall()
    cur.close()
    return res


def reh_info(conn, reh_id):
    cur = conn.cursor()
    query = "select rehearsal.rehdate, room.name, room.type, room.area, room.cost, " \
            "reh_base.name, reh_base.address, reh_base.phone, reh_base.mail " \
            "from rehearsal join room on rehearsal.roomid = room.id " \
            "join reh_base on room.baseid = reh_base.id " \
            "where rehearsal.id = %s"
    cur.execute(query, (reh_id,))
    res = cur.fetchall()
    cur.close()
    return res


def base_info(conn, base_id):
    cur = conn.cursor()
    query = "select name, address, phone, mail from reh_base where id = %s"
    cur.execute(query, (base_id,))
    res = cur.fetchall()
    cur.close()
    return res


def rooms_by_base(conn, base_id):
    cur = conn.cursor()
    query = "select id, name, type from room where baseid = %s"
    cur.execute(query, (base_id,))
    res = cur.fetchall()
    cur.close()
    return res


def gear_by_room(conn, room_id):
    cur = conn.cursor()
    query = "select type, brand, amount from equipment where roomid = %s"
    cur.execute(query, (room_id,))
    res = cur.fetchall()
    cur.close()
    return res


def book(conn, reh):
    cur = conn.cursor()

    if datetime.strptime(reh.date, "%Y-%m-%d %H:%M:%S") < datetime.now():
        return 2

    query = "select * from rehearsal where rehdate =  %s and roomid = %s"
    cur.execute(query, (reh.date, reh.room_id,))
    res = cur.fetchall()
    if len(res) != 0:  # если репетиция в этой комнате на это время уже забронирована
        return 1

    query = "select * from rehearsal"
    cur.execute(query)
    res = cur.fetchall()
    reh.id = len(res) + 1

    query = "insert into rehearsal values (%s, %s, %s, %s)"
    cur.execute(query, (reh.id, reh.musician_id, reh.room_id, reh.date,))
    conn.commit()
    cur.close()
    return 0


def cancel(conn, reh_id):
    cur = conn.cursor()
    query = "delete from rehearsal where id = %s"
    cur.execute(query, (reh_id,))
    conn.commit()
    cur.close()


def test_query(conn):
    cur = conn.cursor()
    query = "select rehearsal.rehdate, room.name, room.type, room.area, room.cost, " \
            "reh_base.name, reh_base.address, reh_base.phone, reh_base.mail " \
            "from rehearsal join room on rehearsal.roomid = room.id " \
            "join account on rehearsal.musicianid = account.id " \
            "join reh_base on room.baseid = reh_base.id"
    cur.execute(query)
    res = cur.fetchall()
    cur.close()
    return res


def connect():
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", database="DB_course",
                                      user="postgres", password="LinkinPark20")
        # print("Connection to PostgreSQL DB successful")

    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def connect_musician():
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", database="DB_course",
                                      user="musician", password="muse")
        print("Connection of musician successful")

    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def connect_owner():
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", database="DB_course",
                                      user="base_owner", password="belldom")
        print("Connection of owner successful")

    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def connect_admin():
    connection = None
    try:
        connection = psycopg2.connect(host="localhost", database="DB_course",
                                      user="app_admin", password="linkinpark")
        print("Connection of admin successful")

    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection
