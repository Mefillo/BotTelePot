import sqlite3
import telepot
import datetime
from telepot.loop import MessageLoop
#Определяем бота
TOKEN = TOKEN
bot = telepot.Bot(TOKEN)
step = 1
firstt = 1
adhi = """
        Я помогу составить Ваш запрос и направлю его разработчикам :)
        Для начала - расскажите, что Вам нужно - что должен делать и как должен выглядеть бот Вашей мечты:"""
adhiagain = """ Хотите отправить ещё один запрос? Отлично, опишите функционал:
    """

#Подключаем БД
conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

def say_hi (adhi,chat_id):
        now = datetime.datetime.now()
        today5am = now.replace(hour=6, minute=0, second=0, microsecond=0)
        today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)
        today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)

        if today5pm <= now:
            bot.sendMessage(chat_id, ("Добрый вечер!"+adhi))
        if today5pm > now >= today11am:
            bot.sendMessage(chat_id, ("Добрый день!"+adhi))
        if today11am > now >= today5am:
            bot.sendMessage(chat_id, ("Доброе утро!"+adhi))
        if today5am >= now:
            bot.sendMessage(chat_id, ("Доброй ночи!"+adhi))

def ssticker(file_name,chat_id):
        bot.sendSticker(chat_id, open(file_name, 'rb'))
#        examine(r, telepot.namedtuple.Message)
#        file_id = r['sticker']['file_id']
#        bot.sendSticker(chat_id, file_id, reply_to_message_id=msg_id, reply_markup=show_keyboard)
    #    bot.sendSticker(chat_id, file_id, reply_markup=nt_remove_keyboard)

def checker(uname):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM clients WHERE name = ?",(uname,))
        g=cursor.fetchall()
        if not g:
            return(0)
        else:
            return (1)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def inserter_clients(uname,firstt,step):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients VALUES (?,?,?,?)",(None,uname,firstt,step))
        conn.commit()

    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def get_step(uname):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT step FROM clients WHERE name = ?",(uname,))
        g=cursor.fetchall()
        g=g[0]
        g=g[0]
        print(g)
        return (g)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def upd_step(uname,num):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE clients SET step = ?  WHERE name = ?",(num, uname))
        conn.commit()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def upd_firstt(uname):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE clients SET firstt = 0  WHERE name = ?",(uname,))
        conn.commit()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def get_firstt(uname):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT firstt FROM clients WHERE name = ?",(uname,))
        g=cursor.fetchall()
        g=g[0]
        g=g[0]
        print(g)
        return (g)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def insert_orders (client_name):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orders VALUES (?,?,?)",(None,client_name,"Заказ:"))
        conn.commit()

    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def upd_orders (client_name, text):
    conn = sqlite3.connect("mybd.bd") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT order_text FROM orders WHERE client_name = ?", (client_name,))
        oldtext = cursor.fetchall()
        oldtext = oldtext[0]
        print(oldtext)
        print(oldtext[0])
        cursor.execute("UPDATE orders SET order_text = ? WHERE client_name = ?",((oldtext[0]+". "+text), client_name))
        conn.commit()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


#Главная функция
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global step, firstt

    from_who = msg.get('from')
    uname= from_who.get('username')

    if(checker(uname)):
        print("We got him!")
    else:
        inserter_clients(uname,1,1)
        insert_orders(uname)
    get_step(uname)

    if get_step(uname) == 1:
        if get_firstt(uname):
            ssticker("temach1.png", chat_id)
            say_hi(adhi, chat_id)
            upd_firstt(uname)
            upd_step(uname, (get_step(uname)+1))
            upd_orders(uname,("Greetings: "+msg.get('text')))
        else:
#            say_hi(adhiagain,chat_id)
#            step+=1
            step = 4
    elif get_step(uname) == 2:
        bot.sendMessage(chat_id, ("Когда Вы ожидаете увидеть готового бота?"))
        upd_orders(uname,("What: "+msg.get('text')))
        upd_step(uname, (get_step(uname)+1))
    elif get_step(uname) == 3:
        bot.sendMessage(chat_id, ("Во сколько Вы оцениваете такую работу?"))
        upd_orders(uname,("When: "+msg.get('text')))
        upd_step(uname, (get_step(uname)+1))
    elif get_step(uname) == 4:
        bot.sendMessage(chat_id, ("Спасибо, Ваш заказ передан разработчикам, приятного дня..."))
        upd_orders(uname,("How much: "+msg.get('text')))
        upd_step(uname, (get_step(uname)+1))









MessageLoop(bot, handle).run_as_thread()

while True:
    n = input('To stop enter "stop":')
    if n.strip() == 'stop':
        break
