import random
import string


def gen_str(length):
    let = string.ascii_lowercase
    s = ''.join(random.choice(let) for i in range(length))
    return s


def gen_mail(mails):
    mail = gen_str(random.randint(3, 10)) + '@' + mails[random.randint(0, 2)]
    return mail


def gen_phone():
    phone = '+7-9'
    phone += str(random.randint(0, 9))
    phone += str(random.randint(0, 9))
    phone += '-'
    phone += str(random.randint(0, 9))
    phone += str(random.randint(0, 9))
    phone += str(random.randint(0, 9))
    phone += '-'
    phone += str(random.randint(0, 9))
    phone += str(random.randint(0, 9))
    phone += '-'
    phone += str(random.randint(0, 9))
    phone += str(random.randint(0, 9))
    return phone


def gen_date(year_lim1, year_lim2):
    date = str(random.randint(year_lim1, year_lim2)) + '-'

    # month
    first = random.randint(0, 1)
    if first == 0:
        sec = random.randint(1, 9)
    else:
        sec = random.randint(0, 2)
    date += str(first) + str(sec) + '-'

    # day
    first = random.randint(0, 2)
    if first != 0:
        sec = random.randint(0, 8)
    else:
        sec = random.randint(1, 9)
    date += str(first) + str(sec) + ' '

    # time
    first = random.randint(0, 2)
    if first != 2:
        sec = random.randint(0, 9)
    else:
        sec = random.randint(0, 3)
    date += str(first) + str(sec) + ':00:00'

    return date


names = ['Aaliyah', 'Abigail', 'Ada', 'Adelina', 'Agatha', 'Alexa', 'Alexandra', 'Alexis', 'Alise',
         'Bailey', 'Barbara', 'Beatrice', 'Belinda', 'Brianna', 'Bridjet', 'Brooke', 'Caroline',
         'Catherine', 'Cecilia', 'Celia', 'Chloe', 'Christine', 'Claire', 'Daisy', 'Danielle',
         'Deborah', 'Delia', 'Destiny', 'Diana', 'Dorothy', 'Eleanor', 'Elizabeth', 'Ella', 'Emily',
         'Emma', 'Erin', 'Aaron', 'Abraham', 'Adam', 'Adrian', 'Aidan', 'Alan', 'Albert', 'Alejandro',
         'Alex', 'Alexander', 'Alfred', 'Andrew', 'Benjamin', 'Bernard', 'Blake', 'Brandon', 'Brian',
         'Bruce', 'Bryan', 'Cameron', 'Carl', 'Carlos', 'Charles', 'Christopher', 'Daniel', 'David',
         'Dennis', 'Devin', 'Diego', 'Dominic', 'Donald', 'Douglas', 'Dylan', 'Edward', 'Elijah', 'Eric']
mails = ['yandex.ru', 'mail.ru', 'gmail.com']

acc = open('accs.txt', 'w')
acc_type = ['musician', 'owner']
owners = []
musicians = []
for i in range(1, 1001):
    acc.write(str(i) + '|')  # ID
    acc.write(names[random.randint(0, 71)] + '|')  # fio
    acc.write(gen_phone() + '|')  # phone
    acc.write(gen_mail(mails) + '|')  # mail
    acc.write(gen_str(5) + '|')  # password
    tmp = acc_type[random.randint(0, 1)]
    acc.write(tmp + '\n')  # type
    if tmp == 'musician':
        musicians.append(i)
    else:
        owners.append(i)
acc.close()

bases = open('bases.txt', 'w')
for i in range(1, 1001):
    bases.write(str(i) + '|')  # ID
    rand = random.randint(1, 1000)
    while rand not in owners:
        rand = random.randint(1, 1000)
    bases.write(str(rand) + '|')  # ownerID
    bases.write(gen_str(5) + '|')  # name
    bases.write(gen_str(10) + '|')  # address
    bases.write(gen_phone() + '|')  # phone
    bases.write(gen_mail(mails) + '\n')  # mail
bases.close()

rooms = open('rooms.txt', 'w')
room_type = ['band', 'vocal', 'drum']
for i in range(1, 1001):
    rooms.write(str(i) + '|')  # ID
    rooms.write(str(random.randint(1, 1000)) + '|')  # baseID
    rooms.write(gen_str(5) + '|')  # name
    rooms.write(room_type[random.randint(0, 2)] + '|')  # type
    rooms.write(str(random.randint(15, 40)) + '|')  # area
    rooms.write(str(random.randint(450, 2000)) + '\n')  # cost
rooms.close()

equip = open('equip.txt', 'w')
equip_type = ['amp', 'mic', 'drums', 'commutation', 'pedal']
for i in range(1, 1001):
    equip.write(str(i) + '|')  # ID
    equip.write(str(random.randint(1, 1000)) + '|')  # roomID
    equip.write(equip_type[random.randint(0, 4)] + '|')  # type
    equip.write(gen_str(5) + '|')  # brand
    equip.write(str(random.randint(1, 3)) + '\n')  # amount
equip.close()

rehs = open('rehs.txt', 'w')
dates = []
for i in range(1, 1001):
    rehs.write(str(i) + '|')  # ID
    rand = random.randint(1, 1000)
    while rand not in musicians:
        rand = random.randint(1, 1000)
    rehs.write(str(rand) + '|')  # musicianID
    rehs.write(str(random.randint(1, 1000)) + '|')  # roomID
    date = gen_date(2019, 2022)
    while date in dates:
        date = gen_date(2019, 2022)
    dates.append(date)
    rehs.write(date + '\n')  # date
rehs.close()
