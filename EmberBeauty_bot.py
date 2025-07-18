import telebot
from telebot import types
import sqlite3 as sq
import logging
from telebot import apihelper

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


TG_PROXY = 'https://194.44.208.62:80'
TG_BOT_TOKEN = '5942700781:AAEQTpeRjIKv4UCmu-JSeZh8Wx6kn8TRwoU'

apihelper.proxy = {'http': TG_PROXY}


bot = telebot.TeleBot('5942700781:AAEQTpeRjIKv4UCmu-JSeZh8Wx6kn8TRwoU')
list_push, record, zap_list, new_list_an, new_list_mar, new_list_anast, new_list_jul, new_list_ari= [],[],[],[],[],[],[],[]
count_yes,count_no = 0,0
vars = {}
bool_push = False
i=0

with sq.connect('date.db') as con:
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS record_manic (
    master TEXT NO NULL,
    data TEXT NO NULL,
    times TEXT NO NULL,
    name TEXT,
    tel TEXT,
    usluga TEXT
)""")
    cur.execute("""DELETE FROM record_manic WHERE data < strftime("%d/%m/%Y", 'now', '-1 day')""")
#cur.execute("DROP TABLE IF EXISTS record_manic")
with sq.connect('date.db') as con:
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS record_ped (
    master TEXT NO NULL,
    data TEXT NO NULL,
    times TEXT NO NULL,
    name TEXT,
    tel TEXT,
    usluga TEXT
)""")
    cur.execute("""DELETE FROM record_ped WHERE data < strftime("%d/%m/%Y", 'now','-1 day')""")
#cur.execute("DROP TABLE IF EXISTS record_ped")

@bot.message_handler(commands=['start','help'])
def start(message):
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    write = types.KeyboardButton('Оформить запись 📅')
    price = types.KeyboardButton('Прайс-лист услуг 📋')
    if bool_push:
        push = types.KeyboardButton('Отписаться от рассылки новостей 🔕')
    else:
        push = types.KeyboardButton('Подписаться на рассылку новостей 🔔')
    contact = types.KeyboardButton('Контактная информация 📱')
    marcup.add(write,price,push,contact)
    next_msg = bot.send_message(message.chat.id, 'Выберите пункт меню 👇', reply_markup=marcup)
    bot.register_next_step_handler(next_msg,step_1)
    
@bot.message_handler(content_types=['text'])
def usluga(message):   
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    manic = types.KeyboardButton('Маникюр 💅')
    pmanic = types.KeyboardButton('Педикюр 👡')
    back = types.KeyboardButton('Назад ⬅️')
    marcup.add(manic,pmanic,back)
    next_msg = bot.send_message(message.chat.id, "Какая услуга вас интересует?", reply_markup=marcup)
    bot.register_next_step_handler(next_msg,step_2)


@bot.message_handler(content_types=['text'])
def step_1(message):
    if message.text == 'Оформить запись 📅':
        usluga(message)
    if message.text == 'Прайс-лист услуг 📋':
        price_photo = open('img/5634323.jpg', '+rb')
        next_msg = bot.send_photo(message.chat.id, price_photo)
        bot.register_next_step_handler(next_msg,step_1)
    if message.text == 'Контактная информация 📱':
        marcup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
        adres = types.KeyboardButton('Адрес 🗺️')
        job = types.KeyboardButton('Режим работы 🕰️')
        call = types.KeyboardButton('Связь с администратором 📞')
        back = types.KeyboardButton('Назад ⬅️')
        marcup.add(adres,job,call,back)
        next_msg2 = bot.send_message(message.chat.id, "Что именно вас интересует?", reply_markup=marcup)
        bot.register_next_step_handler(next_msg2,step_2)
    if message.text == 'Подписаться на рассылку новостей 🔔' or message.text == 'Отписаться от рассылки новостей 🔕' :
        if not message.from_user.id in list_push:
            list_push.append(message.from_user.id)
            bool_push=True
            marcup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            write = types.KeyboardButton('Оформить запись 📅')
            price = types.KeyboardButton('Прайс-лист услуг 📋')
            push = types.KeyboardButton('Отписаться от рассылки новостей 🔕')
            contact = types.KeyboardButton('Контактная информация 📱')
            marcup.add(write,price,push,contact)
            next_msg = bot.send_message(message.chat.id, "Спасибо, что оформили нашу подписку 🌸", reply_markup=marcup)
            bot.register_next_step_handler(next_msg,step_1)
        else:
            list_push.remove(message.from_user.id)
            bool_push=False
            marcup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            write = types.KeyboardButton('Оформить запись 📅')
            price = types.KeyboardButton('Прайс-лист услуг 📋')
            push = types.KeyboardButton('Подписаться на рассылку новостей 🔔')
            contact = types.KeyboardButton('Контактная информация 📱')
            marcup.add(write,price,push,contact)
            next_msg = bot.send_message(message.chat.id, "Подписка успешно отменена 🔕", reply_markup=marcup)
            bot.register_next_step_handler(next_msg,step_1)
    if message.text == 'Назад ⬅️':
        start(message)

@bot.message_handler(content_types=['text'])
def uslug_manic(message):
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    a1 = types.KeyboardButton('Маникюр')
    a2 = types.KeyboardButton('Маникюр + лак')
    a3 = types.KeyboardButton('Маникюр + гель лак')
    a4 = types.KeyboardButton('Маникюр + наращивание')
    a5 = types.KeyboardButton('Коррекция')
    a6 = types.KeyboardButton('Назад ⬅️')
    marcup.add(a1).add(a2).add(a3).add(a4).add(a5).add(a6)
    next_msg = bot.send_message(message.chat.id, "Выберите подходящую услугу 💅", reply_markup=marcup)
    bot.register_next_step_handler(next_msg,step_3)

@bot.message_handler(content_types=['text'])
def uslug_ped(message):
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    p1 = types.KeyboardButton('Педикюр')
    p2 = types.KeyboardButton('Педикюр + лак')
    p3 = types.KeyboardButton('Педикюр + гель-лак')
    back = types.KeyboardButton('Назад ⬅️')
    marcup.add(p1,p2,p3,back)
    next_msg = bot.send_message(message.chat.id, "Выберите подходящую услугу 👡 ", reply_markup=marcup)
    bot.register_next_step_handler(next_msg,step_3)

@bot.message_handler(content_types=['text'])
def step_2(message):
    if message.text == 'Назад ⬅️':
        start(message)
    if message.text == 'Адрес 🗺️':
        next_msg = bot.send_message(message.chat.id, '🚩 Ул. Максима Горькова, д. 148, 2 этаж, 47.227837, 39.720663')
        bot.register_next_step_handler(next_msg,step_2)
    if message.text == 'Режим работы 🕰️':
        next_msg = bot.send_message(message.chat.id, '⏰ с 9:00 до 20:00 без выходных')
        bot.register_next_step_handler(next_msg,step_2)
    if message.text == 'Связь с администратором 📞':
        next_msg = bot.send_message(message.chat.id, '📞 +79996594626')
        bot.register_next_step_handler(next_msg,step_2)
    if message.text == 'Маникюр 💅':
        uslug_manic(message)
    if message.text == 'Педикюр 👡':
        uslug_ped(message)

@bot.message_handler(content_types=['text'])
def master_manic(message): 
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    anna = types.KeyboardButton('Анна')
    marina = types.KeyboardButton('Марина')
    anast = types.KeyboardButton('Анастасия')
    a6 = types.KeyboardButton('Назад ⬅️')
    marcup.add(anna,marina,anast,a6)
    next_msg = bot.send_message(message.chat.id, "Выберите мастера 💅 ", reply_markup=marcup)
    bot.register_next_step_handler(next_msg,nearest_places)
    
@bot.message_handler(content_types=['text'])
def master_ped(message): 
    marcup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    julia = types.KeyboardButton('Юлия')
    arina = types.KeyboardButton('Арина')
    back = types.KeyboardButton('Назад ⬅️')
    marcup.add(julia,arina,back)
    next_msg = bot.send_message(message.chat.id, "Выберите мастера 👡 ", reply_markup=marcup)
    bot.register_next_step_handler(next_msg,step_5)
   
@bot.message_handler(content_types=['text'])
def step_3(message):   
    if message.text == 'Назад ⬅️':
        usluga(message)
    if message.text == 'Маникюр':    
        zap_list.append('маникюр')
        print(zap_list)
        master_manic(message)
    if message.text == 'Маникюр + лак':
        zap_list.append('маникюр + лак')
        master_manic(message)
    if message.text == 'Маникюр + гель лак':
        zap_list.append('маникюр + гель лак')
        master_manic(message)
    if message.text == 'Маникюр + наращивание':
        zap_list.append('маникюр + наращивание')
        master_manic(message)
    if message.text == 'Коррекция':
        zap_list.append('коррекция')
        master_manic(message)
    if message.text == 'Педикюр':
        zap_list.append('педикюр')
        master_ped(message)      
    if message.text == 'Педикюр + лак':  
        zap_list.append('педикюр + лак')
        master_ped(message)  
    if message.text == 'Педикюр + гель-лак':  
        zap_list.append('педикюр + гель-лак')
        master_ped(message)        
              
        
@bot.message_handler(content_types=['text'])
def nearest_places(message):
    if message.text == 'Назад ⬅️':
        uslug_manic(message)
    if message.text == 'Анна':
        con = sq.connect('date.db')
        curs = con.cursor()
        curs.execute("""SELECT data,times from record_manic WHERE master == 'Анна' AND (name is NULL OR name == "" OR name == "NULL")
        AND (tel is NULL OR tel == "" OR tel == "NULL") AND (usluga is NULL OR usluga == "" OR usluga == "NULL") AND(data > strftime("%d/%m/%Y", 'now')) 
		AND (data > strftime("%d/%m/%Y", 'now') OR (times > strftime('%H:%M', 'now', 'localtime'))) ORDER BY data ASC LIMIT 5 """)
        records = curs.fetchall()
        record.clear()
        new_list_an.clear()
        for row in records:
            record.append(row)
        curs.close() 
        def foo(a):     
            for b in a:
                    if isinstance(b,tuple):
                        foo(b)
                    else:
                        new_list_an.append(b)
        foo(record)
        char = '.2023'
        for idx, ele in enumerate(new_list_an):
            new_list_an[idx] = ele.replace(char, '') 
        marcup=types.InlineKeyboardMarkup()
        vars.clear()
        i=0 
        while i < len(new_list_an):
            c=str(new_list_an[i])
            c1=str(new_list_an[i+1])
            vars[f"anna_{i}"] = types.InlineKeyboardButton(text = c + ' на ' + c1, callback_data= str(f'anna{i}'))
            marcup.add(vars[f"anna_{i}"])
            i+=2
        next_msg = bot.send_message(message.chat.id, 'Ближайшие свободные места',reply_markup=marcup)
        bot.register_next_step_handler(next_msg,nearest_places)
    if message.text == 'Марина':
        con = sq.connect('date.db')
        curs = con.cursor()
        curs.execute("""SELECT data,times from record_manic WHERE master == 'Марина' AND (name is NULL OR name == "" OR name == "NULL")
        AND (tel is NULL OR tel == "" OR tel == "NULL") AND (usluga is NULL OR usluga == "" OR usluga == "NULL") AND(data > strftime("%d/%m/%Y", 'now')) 
		AND (data > strftime("%d/%m/%Y", 'now') OR (times > strftime('%H:%M', 'now', 'localtime'))) ORDER BY data ASC LIMIT 5 """)
        records = curs.fetchall()
        record.clear()
        new_list_mar.clear()
        for row in records:
            record.append(row)
        curs.close() 
        def foo(a):     
            for b in a:
                    if isinstance(b,tuple):
                        foo(b)
                    else:
                        new_list_mar.append(b)
        foo(record)
        char = '.2023'
        for idx, ele in enumerate(new_list_mar):
            new_list_mar[idx] = ele.replace(char, '') 
        marcup=types.InlineKeyboardMarkup()
        vars.clear()
        i=0 
        while i < len(new_list_mar):
            c=str(new_list_mar[i])
            c1=str(new_list_mar[i+1])
            vars[f"marina_{i}"] = types.InlineKeyboardButton(text = c + ' на ' + c1, callback_data= f'marina{i}')
            marcup.add(vars[f"marina_{i}"])
            i+=2
        next_msg = bot.send_message(message.chat.id, 'Ближайшие свободные места',reply_markup=marcup)
        bot.register_next_step_handler(next_msg,nearest_places)
    if message.text == 'Анастасия':
        con = sq.connect('date.db')
        curs = con.cursor()
        curs.execute("""SELECT data,times from record_manic WHERE master == 'Анастасия' AND (name is NULL OR name == "" OR name == "NULL")
        AND (tel is NULL OR tel == "" OR tel == "NULL") AND (usluga is NULL OR usluga == "" OR usluga == "NULL") AND(data > strftime("%d/%m/%Y", 'now')) 
		AND (data > strftime("%d/%m/%Y", 'now') OR (times > strftime('%H:%M', 'now', 'localtime'))) ORDER BY data ASC LIMIT 5 """)
        records = curs.fetchall()
        record.clear()
        new_list_anast.clear()
        for row in records:
            record.append(row)
        curs.close() 
        def foo(a):     
            for b in a:
                    if isinstance(b,tuple):
                        foo(b)
                    else:
                        new_list_anast.append(b)
        foo(record)
        char = '.2023'
        for idx, ele in enumerate(new_list_anast):
            new_list_anast[idx] = ele.replace(char, '') 
        marcup=types.InlineKeyboardMarkup()
        vars.clear()
        i=0 
        while i < len(new_list_anast):
            c=str(new_list_anast[i])
            c1=str(new_list_anast[i+1])
            vars[f"anast_{i}"] = types.InlineKeyboardButton(text = c + ' на ' + c1, callback_data= f'anast{i}')
            marcup.add(vars[f"anast_{i}"])
            i+=2
        next_msg = bot.send_message(message.chat.id, 'Ближайшие свободные места',reply_markup=marcup)
        bot.register_next_step_handler(next_msg,nearest_places)
    
        
@bot.message_handler(content_types=['text'])
def step_5(message):
    if message.text == 'Назад ⬅️':
        uslug_ped(message)
    if message.text == 'Юлия':
        con = sq.connect('date.db')
        curs = con.cursor()
        curs.execute("""SELECT data,times from record_ped WHERE master == 'Юлия' AND (name is NULL OR name == "" OR name == "NULL")
        AND (tel is NULL OR tel == "" OR tel == "NULL") AND (usluga is NULL OR usluga == "" OR usluga == "NULL") AND(data > strftime("%d/%m/%Y", 'now')) 
		AND (data > strftime("%d/%m/%Y", 'now') OR (times > strftime('%H:%M', 'now', 'localtime'))) ORDER BY data ASC LIMIT 5 """)
        records = curs.fetchall()
        record.clear()
        new_list_jul.clear()
        for row in records:
            record.append(row)
        curs.close() 
        def foo(a):     
            for b in a:
                    if isinstance(b,tuple):
                        foo(b)
                    else:
                        new_list_jul.append(b)
        foo(record)
        char = '.2023'
        for idx, ele in enumerate(new_list_jul):
            new_list_jul[idx] = ele.replace(char, '') 
        marcup=types.InlineKeyboardMarkup()
        vars.clear()
        i=0 
        while i < len(new_list_jul):
            c=str(new_list_jul[i])
            c1=str(new_list_jul[i+1])
            vars[f"julia_{i}"] = types.InlineKeyboardButton(text = c + ' на ' + c1, callback_data= f'julia{i}')
            marcup.add(vars[f"julia_{i}"])
            i+=2
        next_msg = bot.send_message(message.chat.id, 'Ближайшие свободные места',reply_markup=marcup)
        bot.register_next_step_handler(next_msg,step_5)
    if message.text == 'Арина':    
        con = sq.connect('date.db')
        curs = con.cursor()
        curs.execute("""SELECT data,times from record_ped WHERE master == 'Арина' AND (name is NULL OR name == "" OR name == "NULL")
        AND (tel is NULL OR tel == "" OR tel == "NULL") AND (usluga is NULL OR usluga == "" OR usluga == "NULL") AND(data > strftime("%d/%m/%Y", 'now')) 
		AND (data > strftime("%d/%m/%Y", 'now') OR (times > strftime('%H:%M', 'now', 'localtime'))) ORDER BY data ASC LIMIT 5 """)
        records = curs.fetchall()
        record.clear()
        new_list_ari.clear()
        for row in records:
            record.append(row)
        curs.close() 
        def foo(a):     
            for b in a:
                    if isinstance(b,tuple):
                        foo(b)
                    else:
                        new_list_ari.append(b)
        foo(record)
        char = '.2023'
        for idx, ele in enumerate(new_list_ari):
            new_list_ari[idx] = ele.replace(char, '') 
        marcup=types.InlineKeyboardMarkup()
        vars.clear()
        i=0 
        while i < len(new_list_ari):
            c=str(new_list_ari[i])
            c1=str(new_list_ari[i+1])
            vars[f"arina_{i}"] = types.InlineKeyboardButton(text = c + ' на ' + c1, callback_data= f'arina{i}')
            marcup.add(vars[f"arina_{i}"])
            i+=2
        next_msg = bot.send_message(message.chat.id, 'Ближайшие свободные места',reply_markup=marcup)
        bot.register_next_step_handler(next_msg,step_5)

@bot.message_handler(content_types=['text'])
def name(message):
    next_msg = bot.send_message(message.chat.id, 'Чтобы оформить запись введите свое имя',reply_markup=types.ReplyKeyboardRemove()) 
    bot.register_next_step_handler(next_msg,message_input_step)
     
def proverka():
      if len(zap_list) > 1:
          tmp = zap_list[0]
          zap_list.clear()
          zap_list.append(tmp)  
    
@bot.callback_query_handler(func = lambda call:True)
def data_check(call):
    if call.message:
        if call.data == 'anna0':
            proverka()
            zap_list.append('Анна')
            zap_list.append(str(new_list_an[0]))
            zap_list.append(str(new_list_an[1]))
            name(call.message)
    if call.message:
        if call.data == 'marina0':
            proverka()
            zap_list.append('Марина')
            zap_list.append(str(new_list_mar[0]))
            zap_list.append(str(new_list_mar[1]))
            name(call.message)
    if call.message:
        if call.data == 'julia0':
            proverka()
            zap_list.append('Юлия')
            zap_list.append(str(new_list_jul[0]))
            zap_list.append(str(new_list_jul[1]))
            name(call.message)
    if call.message:
        if call.data == 'julia2':
            proverka()
            zap_list.append('Юлия')
            zap_list.append(str(new_list_jul[2]))
            zap_list.append(str(new_list_jul[3]))
            name(call.message)
    if call.message:
        if call.data == 'julia4':
            proverka()
            zap_list.append('Юлия')
            zap_list.append(str(new_list_jul[4]))
            zap_list.append(str(new_list_jul[5]))
            name(call.message)
    if call.message:
        if call.data == 'julia6':
            proverka()
            zap_list.append('Юлия')
            zap_list.append(str(new_list_jul[6]))
            zap_list.append(str(new_list_jul[7]))
            name(call.message)
    if call.message:
        if call.data == 'julia8':
            proverka()
            zap_list.append('Юлия')
            zap_list.append(str(new_list_jul[8]))
            zap_list.append(str(new_list_jul[9]))
            name(call.message)
    if call.message:
        if call.data == 'arina0':
            proverka()
            zap_list.append('Арина')
            zap_list.append(str(new_list_ari[0]))
            zap_list.append(str(new_list_ari[1]))
            name(call.message)
    if call.message:
        if call.data == 'arina2':
            proverka()
            zap_list.append('Арина')
            zap_list.append(str(new_list_ari[2]))
            zap_list.append(str(new_list_ari[3]))
            name(call.message)
    if call.message:
        if call.data == 'arina4':
            proverka()
            zap_list.append('Арина')
            zap_list.append(str(new_list_ari[4]))
            zap_list.append(str(new_list_ari[5]))
            name(call.message)
    if call.message:
        if call.data == 'arina6':
            proverka()
            zap_list.append('Арина')
            zap_list.append(str(new_list_ari[6]))
            zap_list.append(str(new_list_ari[7]))
            name(call.message)
    if call.message:
        if call.data == 'arina8':
            proverka()
            zap_list.append('Арина')
            zap_list.append(str(new_list_ari[8]))
            zap_list.append(str(new_list_ari[9]))
            name(call.message)
    if call.message:
        if call.data == 'anast0':
            proverka()
            zap_list.append('Анастасия')
            zap_list.append(str(new_list_anast[0]))
            zap_list.append(str(new_list_anast[1]))
            name(call.message)
    if call.message:
        if call.data == 'anna2':
            proverka()
            zap_list.append('Анна')
            zap_list.append(str(new_list_an[2]))
            zap_list.append(str(new_list_an[3]))
            name(call.message)
    if call.message:
        if call.data == 'marina2':
            proverka()
            zap_list.append('Марина')
            zap_list.append(str(new_list_mar[2]))
            zap_list.append(str(new_list_mar[3]))
            name(call.message)
    if call.message:
        if call.data == 'anast2':
            proverka()
            zap_list.append('Анастасия')
            zap_list.append(str(new_list_anast[2]))
            zap_list.append(str(new_list_anast[3]))
            name(call.message)
    if call.message:
        if call.data == 'anna4':
            proverka()
            zap_list.append('Анна')
            zap_list.append(str(new_list_an[4]))
            zap_list.append(str(new_list_an[5]))
            name(call.message)
    if call.message:
        if call.data == 'marina4':
            proverka()
            zap_list.append('Марина')
            zap_list.append(str(new_list_mar[4]))
            zap_list.append(str(new_list_mar[5]))
            name(call.message)
    if call.message:
        if call.data == 'anast4':
            proverka()
            zap_list.append('Анастасия')
            zap_list.append(str(new_list_anast[4]))
            zap_list.append(str(new_list_anast[5]))
            name(call.message)
    if call.message:
        if call.data == 'anna6':
            proverka()
            zap_list.append('Анна')
            zap_list.append(str(new_list_an[6]))
            zap_list.append(str(new_list_an[7]))
            name(call.message)
    if call.message:
        if call.data == 'marina6':
            proverka()
            zap_list.append('Марина')
            zap_list.append(str(new_list_mar[6]))
            zap_list.append(str(new_list_mar[7]))
            name(call.message)
    if call.message:
        if call.data == 'anast6':
            proverka()
            zap_list.append('Анастасия')
            zap_list.append(str(new_list_anast[6]))
            zap_list.append(str(new_list_anast[7]))
            name(call.message)
    if call.message:
        if call.data == 'anna8':
            proverka()
            zap_list.append('Анна')
            zap_list.append(str(new_list_an[8]))
            zap_list.append(str(new_list_an[9]))
            name(call.message)
    if call.message:
        if call.data == 'marina8':
            proverka()
            zap_list.append('Марина')
            zap_list.append(str(new_list_mar[8]))
            zap_list.append(str(new_list_mar[9]))
            name(call.message)
    if call.message:
        if call.data == 'anast8':
            proverka()
            zap_list.append('Анастасия')
            zap_list.append(str(new_list_anast[8]))
            zap_list.append(str(new_list_anast[9]))
            name(call.message)
    if call.message:
        if call.data == 'да':
            bot.send_message(call.message.chat.id, 'Записала 😊 Ждём вас в студии маникюра Capsula по адресу 🚩 Ул. Максима Горькова, д. 148, 2 этаж, 47.227837, 39.720663') 
            bot.send_message(call.message.chat.id, 'Телефон для связи 📞 +79996594626',reply_markup=types.ReplyKeyboardRemove())  
            insert_into_table(zap_list[0], name_us, contact,zap_list[1],zap_list[2]+'.2023',zap_list[3])
    if call.message:
        if call.data == 'нет':
            bot.send_message(call.message.chat.id, 'Запись отменена')
            insert_into_table('NULL', 'NULL', 'NULL', zap_list[1], zap_list[2]+'.2023',zap_list[3])
            start(call.message)

def insert_into_table(record_str, name_us, contact,record_str1,record_str2,record_str3):
    con = sq.connect('date.db')
    curs = con.cursor()
    sqlite_insert_with_param = """UPDATE record_manic SET name == ?, tel == ?, usluga == ? WHERE master == ? AND data == ? AND times == ?"""
    data_tuple = (name_us, contact, record_str, record_str1, record_str2, record_str3)
    curs.execute(sqlite_insert_with_param, data_tuple)
    con.commit()
    curs.close()
  
            
@bot.message_handler(content_types=['text'])  
def message_input_step(message):
    global name_us  
    name_us = message.text
    phone(message) 
    
   
@bot.message_handler(content_types=['text'])  
def phone(message):
    marcup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) 
    button_phone = types.KeyboardButton(text="Отправить номер телефон", request_contact=True) 
    marcup.add(button_phone) 
    bot.send_message(message.chat.id, 'Отправьте свой номер телефона', reply_markup=marcup)  

@bot.message_handler(content_types=['contact']) 
def contact(message):
    global contact 
    contact = message.contact.phone_number
    info_record(message)

@bot.message_handler(content_types=['text'])  
def info_record(message):
    bot.send_message(message.chat.id, 'Вы записаны на ' + str(zap_list[2]) + ' в ' + str(zap_list[3]) + ' к мастеру ' + str(zap_list[1]) + ' на ' + str(zap_list[0]),reply_markup=types.ReplyKeyboardRemove())
    marcup=types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text = 'Да', callback_data= 'да')
    no = types.InlineKeyboardButton(text = 'Нет', callback_data= 'нет')
    marcup.add(yes,no)
    bot.send_message(message.chat.id, 'Подтвердить запись',reply_markup=marcup)


       
bot.polling(non_stop=True)

