import psycopg2
from psycopg2 import sql
import telebot
from user import user_menu
from telebot import types
from bot_haqida import bot_haqida_
import re

# from fastfood import fast_food
# from superMarket import super_market
# from mobile import mobile_operator
# from uz_schoole import maktablar
# from kiyimDokon import kiyim_dokon

# Database connection
conn = psycopg2.connect(dbname='root', user='postgres', password='1234', host='localhost')
cursor = conn.cursor()

# Initialize the bot
Token = '6727767249:AAGVRtIx4UfKb7kcNh6Rm9mgHeVisVNLTNA'
bot = telebot.TeleBot(Token)

ADMIN_ID = 584323689

companiya = None
works = None

# users = []
#
# userDetailes = {"chat_id": 23132,"company": 'karzinka',"work": 'farosh'}
# users.append(userDetailes)
# print(userDetailes)


# # # Create users table if not exists
# cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                    id SERIAL PRIMARY KEY,
#                    user_name VARCHAR(255) NOT NULL,
#                    user_number VARCHAR(255) NOT NULL,
#                    file_id TEXT NOT NULL
#                    )''')
# #
# # # Create word table if not exists
# cursor.execute('''CREATE TABLE IF NOT EXISTS word (
#                    id SERIAL PRIMARY KEY,
#                    company VARCHAR(255) NOT NULL,
#                    works VARCHAR(255) NOT NULL
#                    )''')
# #
# # # Create admin table if not exists
# cursor.execute('''CREATE TABLE IF NOT EXISTS admin (
#                    id SERIAL PRIMARY KEY,
#                    number VARCHAR(255),
#                    company_id VARCHAR(255),
#                    FOREIGN KEY (company_id) REFERENCES word(id)
#                    )''')

# Add foreign key constraint for users table
# cursor.execute("SELECT 1 FROM pg_constraint WHERE conname='fk_admin_word'")
# if not cursor.fetchone():
#     cursor.execute('''ALTER TABLE users
#                       ADD CONSTRAINT fk_users_word
#                       FOREIGN KEY (id) REFERENCES word(id)''')
#
# # Add foreign key constraint for admin table
# cursor.execute('ALTER TABLE IF EXISTS admin DROP CONSTRAINT IF EXISTS fk_admin_word')
# cursor.execute('''ALTER TABLE admin
#                   ADD CONSTRAINT fk_admin_word
#                   FOREIGN KEY (company_id) REFERENCES word(id);''')

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.commit()

cursor.execute("SELECT * FROM word")
admin = cursor.fetchall()
for admins in admin:
    print(admins)

conn.commit()

# User state dictionary to keep track of user states
user_states = {}


# Commands and message handlers
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    markup = user_menu()
    first_name = message.from_user.first_name if message.from_user.first_name else "User"
    bot.send_message(chat_id, f'Salom 🙋🏿‍♂️, {first_name}!', reply_markup=markup)


# ________________________________________________________________ admin panel
@bot.message_handler(commands=['admin'])
def handle_admin(message):
    chat_id = message.chat.id
    if user_states.get(message.from_user.id):
        # Foydalanuvchi allaqachon ro'yxatdan o'tgan
        bot.send_message(chat_id, "Siz allaqachon ro'yxatdan o'tgansiz. Kirish tugmasini bosing.")
    else:
        # Ro'yxatdan o'tish uchun boshlash
        bot.send_message(chat_id, "Salom! Ro'yxatdan o'tish uchun telefon raqamingizni kiriting:")
        bot.register_next_step_handler(message, start_registration)


# Ro'yxatdan o'tish jarayoni
def start_registration(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    phone_number = message.text

    # Ma'lumotlar bazasida foydalanuvchi borligini tekshirish
    user_exists = check_user_exists(user_id)

    if user_exists:
        # Foydalanuvchi allaqachon ro'yxatdan o'tgan
        bot.send_message(chat_id, "Siz allaqachon ro'yxatdan o'tgansiz. Kirish tugmasini bosing.")
    else:
        # Foydalanuvchi ro'yxatdan o'tgan emas
        user_states[user_id] = {'state': 'phone_number', 'data': {'phone_number': phone_number}}

        # Foydalanuvchi ro'yxatdan o'tishni davom ettirish
        bot.send_message(chat_id, "Telefon raqamingizni tasdiqlang:\n\n" + phone_number,
                         reply_markup=phone_number_confirmation_markup)
        bot.register_next_step_handler(message, confirm_phone_number)


# Ma'lumotlar bazasida foydalanuvchi borligini tekshirish
def check_user_exists(user_id):
    cursor.execute("SELECT * FROM admin WHERE id = %s", (user_id,))
    return cursor.fetchone() is not None


# Foydalanuvchi telefon raqamini tasdiqlash tugmasi
phone_number_confirmation_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
phone_number_confirmation_markup.row(types.KeyboardButton("👍 Tasdiqlash"))


# Foydalanuvchi telefon raqamini tasdiqlash funksiyasi
def confirm_phone_number(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if message.text == '👍 Tasdiqlash':
        # Ro'yxatdan o'tish muvaffaqiyatli bajarildi
        # Bu yerni siz ma'lumotlarni saqlash va kirish tugmasini yuborish uchun kerakli qismlarni qo'shishingiz mumkin
        # ...

        # Foydalanuvchi ro'yxatdan o'tish jarayonini tugatish
        del user_states[user_id]

        # Kirish tugmasini yuborish
        bot.send_message(chat_id, "Ro'yxatdan o'tish muvaffaqiyatli bajarildi. Kirish tugmasini bosing.",
                         reply_markup=login_button_markup)
    else:
        bot.send_message(chat_id, "Telefon raqamingizni tasdiqlamadingiz. Iltimos, qaytadan kiriting:")
        bot.register_next_step_handler(message, confirm_phone_number)


# Kirish tugmasi
login_button_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
login_button_markup.row(types.KeyboardButton("🔐 Kirish"))


# Kirish tugmasini bosing
@bot.message_handler(func=lambda message: message.text == '🔐 Kirish')
def login(message):
    chat_id = message.chat.id

    if user_states.get(message.from_user.id):
        # Foydalanuvchi ro'yxatdan o'tish jarayonida
        bot.send_message(chat_id, "Siz hali ro'yxatdan o'tmadingiz. Ro'yxatdan o'tish tugmasini bosing.")
    else:
        # Foydalanuvchi ro'yxatdan o'tgan
        bot.send_message(chat_id, "Siz ro'yxatdan o'tgansiz. Xush kelibsiz!")


# Ma'lumotlar bazasidagi foydalanuvchi raqamini olish
def get_user_number_from_database(user_id):
    cursor.execute("SELECT number FROM admin WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None


#


# _______________________________________________________________________________________________________ishmenu

@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Ish Menu 👨🏻‍💼')
def menu_ish(message):
    chat_id = message.chat.id
    user1 = message.text

    print("salom")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    karzinak = types.KeyboardButton('Fast Food')
    magnum = types.KeyboardButton('Super Market')
    mobiluz = types.KeyboardButton('Mobile Opertor')
    ucell = types.KeyboardButton('Maktab')
    TerraPro = types.KeyboardButton('Kiyim Dokon')
    Commpass = types.KeyboardButton('Davlat Korhonlari')
    Artel = types.KeyboardButton('Korhonalar')
    SariqBola = types.KeyboardButton('Sariqbola')
    Uzum = types.KeyboardButton('Uzum')
    Hummans = types.KeyboardButton('Hummans')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(karzinak, magnum, mobiluz, ucell, TerraPro, Commpass, Artel, SariqBola, Uzum, Hummans, back)
    bot.send_message(chat_id, 'Ish menuga xush kelibsiz!', reply_markup=markup)


# ___________________________________________________________________________________________________
# from .Menu_yonalish import fastfood
# from fastfood import fast_food

# import sys
# sys.path.append('Menu_yonalish/fastfood.py')
# from Menu_yonalish.fastfood import fast_food
# @bot.message_handler(func=lambda message: message.text == 'Fast Food')
# def FastFood(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     markup = fast_food()
#
#     print(user1)
#
#
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#

import sys


# from .Menu_yonalish.fastfood import fast_food
#
#
# @bot.message_handler(func=lambda message: message.text == 'Fast Food')
# def FastFood(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     # markup = fast_food
#
#     print(user1)
#
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Super Market')
# def SuperMarket(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     markup = super_market()
#
#     print(user1)
#
#     markup.add()
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Mobile Opertor')
# def MobileOpertor(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     markup = mobile_operator()
#
#     print(user1)
#
#     markup.add()
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Maktab')
# def Maktab(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     markup = maktablar()
#     bot.send_message(message.chat.id, 'Nechanchi maktab:', reply_markup=markup)
#
#     print(user1)
#
#     markup.add()
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#
#
# @bot.message_handler(func=lambda message: message.text == 'Kiyim Dokon')
# def kiyim_dokon(message):
#     chat_id = message.chat.id
#     user1 = message.text
#
#     markup = kiyim_dokon()
#
#     print(user1)
#
#     bot.send_message(chat_id, f'Ish menuga xush kelibsiz! {user1}', reply_markup=markup)
#

# ____________________________________________________________________________________________________________________def ishmenu
@bot.message_handler(func=lambda message: message.text == 'Karzinka')  # Karzinka
def menu_Karzinka(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    Farosh = types.KeyboardButton('🧹 Farosh')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Qasob = types.KeyboardButton('🔪 Qasob')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    Hisobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    Ytashuvchi = types.KeyboardButton('👷🏻‍♂️ Yuk tashuvchi')
    COperator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Operator = types.KeyboardButton('👨🏻‍🔧 Operator')
    Qoravul = types.KeyboardButton('👮🏻‍♂️ Qorovul')
    Sotuvchi = types.KeyboardButton('👨🏻‍⚕️ Sotuvchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(Farosh, Oshpaz, Qasob, Kassir, Bugalter, IT_engener, Ytashuvchi, Hisobchi, Yurist, COperator, Operator,
               Qoravul, Sotuvchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun yo`nalish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Magnum')  # magnum
def menu_Magnum(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Farosh = types.KeyboardButton('🧹 Farosh')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Qasob = types.KeyboardButton('🔪 Qasob')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Ytashuvchi = types.KeyboardButton('👷🏻‍♂️ Yuk tashuvchi')
    COperator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Operator = types.KeyboardButton('👨🏻‍🔧 Operator')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(Farosh, Oshpaz, Qasob, Kassir, Bugalter, IT_engener, Ytashuvchi, Hisobchi, Yurist, COperator, Operator,
               Qoravul, Sotuvchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Mobiuz')  # mobiuz menu
def menu_Mobiuz(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Farosh = types.KeyboardButton('🧹 Farosh')
    COperator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Bugalter = types.KeyboardButton('👨🏻‍💼 Bugalter')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    Kuryer = types.KeyboardButton('👨🏻‍💼 Kuryer')
    haydobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Farosh, COperator, Kuryer, Kassir, Oshpaz, Yurist, Hisobchi, Qoravul, Bugalter, IT_engener, Sotuvchi,
               haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Ucell')  # Ucell menu
def menu_Ucell(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Farosh = types.KeyboardButton('🧹 Farosh')
    COperator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    Kuryer = types.KeyboardButton('👨🏻‍💼 Kuryer')
    haydobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Farosh, COperator, Kuryer, Kassir, Oshpaz, Yurist, Hisobchi, Qoravul, Bugalter, IT_engener, Sotuvchi,
               haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'TerraPro')  # TeraPro
def menu_TerraPro(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Operator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    Farosh = types.KeyboardButton('🧹 Farosh')
    Kuryer = types.KeyboardButton('👨🏻‍💼 Kuryer')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Sotuvchi, Qoravul, Operator, Kassir, Bugalter, Farosh, Kuryer, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'KFC')  # Compass menu
def menu_Commpass(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Bugalter, Qoravul, Kassir, Sotuvchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Artel')  # Artel menu
def menu_Artel(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    haydobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Ytashuvchi = types.KeyboardButton('👷🏻‍♂️ Yuk tashuvchi')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Operator = types.KeyboardButton('👨🏻‍💼 Operator')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Kassir = types.KeyboardButton('🛍 Kassir')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, Operator, Oshpaz, IT_engener, Ytashuvchi, Qoravul, Bugalter, Hisobchi, Kassir, Sotuvchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Sariqbola')  # sariq bola menu
def menu_Sariqbola(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Kuryer = types.KeyboardButton('👨🏻‍💼 Kuryer')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Ytashuvchi = types.KeyboardButton('👷🏻‍♂️ Yuk tashuvchi')
    Operator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Kuryer, Operator, Qoravul, Oshpaz, Kassir, Hisobchi, Ytashuvchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Uzum')  # Uzum menu
def menu_Uzum(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    haydobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    Farosh = types.KeyboardButton('🧹 Farosh')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Operator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Ytashuvchi = types.KeyboardButton('👨🏻‍💼 Yuk tashuvchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(Ytashuvchi, Yurist, haydobchi, Farosh, IT_engener, Hisobchi, Qoravul, Bugalter, Operator, Oshpaz, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Hummans')  # Hummans menu
def menu_Hummans(message):
    global companiya

    chat_id = message.chat.id
    companiya = message.text
    print(companiya)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    haydobchi = types.KeyboardButton('👨🏻‍✈️ Haydovchi')
    Kuryer = types.KeyboardButton('👨🏻‍💼 Kuryer')
    Farosh = types.KeyboardButton('🧹 Farosh')
    Oshpaz = types.KeyboardButton('👨🏻‍🍳 Oshpaz')
    Qasob = types.KeyboardButton('🔪 Qasob')
    Kassir = types.KeyboardButton('🛍 Kassir')
    Bugalter = types.KeyboardButton('🤵🏻‍♂️ Bugalter')
    IT_engener = types.KeyboardButton('👨🏻‍💻 IT engener')
    Yurist = types.KeyboardButton('👨🏻‍💼 Yurist')
    Hisobchi = types.KeyboardButton('👨🏻‍💼 Hisobchi')
    Ytashuvchi = types.KeyboardButton('👷🏻‍♂️ Yuk tashuvchi')
    COperator = types.KeyboardButton('👨🏻‍🚀 Call Operator')
    Operator = types.KeyboardButton('👨🏻‍🔧 Operator')
    Qoravul = types.KeyboardButton('👨🏻‍💼 Qorovul')
    Sotuvchi = types.KeyboardButton('👨🏻‍💼 Sotuvchi')
    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, Kassir, Kuryer, Farosh, Oshpaz, Qasob, Bugalter, IT_engener, Ytashuvchi, Yurist, Hisobchi,
               Operator, Qoravul, Sotuvchi, COperator, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Kasp tanlang!', reply_markup=markup)


# _________________________________________________________________________________________________________________________  ishchi menu 2

@bot.message_handler(func=lambda message: message.text == '👨🏻‍✈️ Haydovchi')
def katigoriyaH(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchu Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Kuryer')
def katigoriyaK(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🧹 Farosh')
def katigoriyaF(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍🍳 Oshpaz')
def katigoriyaO(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🔪 Qasob')
def katigoriyaQ(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🛍 Kassir')
def katigoriyaK(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🤵🏻‍♂️ Bugalter')
def katigoriyaB(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍🔧 Operator')
def katigoriyaI(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍💻 IT engener')
def katigoriyaI(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Yurist')
def katigoriyaY(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👷🏻‍♂️ Yuk tashuvchi')
def katigoriyay(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍🚀 Call Operator')
def katigoriyac(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Qorovul')
def katigoriyaq(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Sotuvchi')
def katigoriyas(message):
    global works

    chat_id = message.chat.id
    works = message.text
    print(works)

    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    haydobchi = types.KeyboardButton('👨🏻‍💼 Yuborish 👨🏻‍💼')

    back = types.KeyboardButton('🚪 Orqaga 🚪')
    markup.add(haydobchi, back)
    bot.send_message(chat_id, 'Resume jo`natish uchun Yuborish tanlang!', reply_markup=markup)


def save_company(company, work):
    cursor.execute("insert into word(company,works) values('?','?')", (company, work))
    conn.commit()
    print(companiya)
    print(works)
    conn.commit()


# _____________________________________________________________________________________________________________________
@bot.message_handler(func=lambda message: message.text == '👨🏻‍💼 Yuborish 👨🏻‍💼')
def yuborish(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user))

    try:
        bot.send_message(chat_id, "Salom! Ismingizni kiriting:")
        bot.register_next_step_handler(message, save_full_name)
    except Exception as e:

        print(e + "")


def save_full_name(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.text

    try:
        # Update the user's state
        user_states[user_id] = {'state': 'full_name', 'data': {'user_name': user_name}}

        # Prompt the user for their phone number
        bot.send_message(chat_id, "Iltimos, telefon raqamingizni kiriting \t" + "misol : +(998)97-707-77-77")
        bot.register_next_step_handler(message, save_phone_number)
    except Exception as e:
        print(e)


def save_phone_number(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    phone_number = message.text

    if not phone_number.isdigit():
        bot.send_message(chat_id, "Telefon raqamingiz faqat raqamlardan iborat bo'lishi kerak.")
        return save_phone_number()

    # Update the user's state
    user_states[user_id]['data']['phone_number'] = phone_number
    bot.send_message(chat_id, "Iltimos, Resume file kiriting: ")
    bot.register_next_step_handler(message, save_file)


def save_file(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    file_type = message.content_type

    if file_type in ['photo', 'audio', 'video', 'voice', 'text']:
        bot.reply_to(message, "Noto'g'ri fayl turi. Faqat dokument, rasm, ovoz, video yoki audio fayllarni yuboring.")
        return

    try:

        file_name = message.document.file_name
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Faylni "zaz/" papkasiga saqlash
        with open("zaz/" + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Faylni ma'lumotlar bazasiga qo'shish
        insert_query = sql.SQL("INSERT INTO users (user_name, user_number, file_id) VALUES (%s, %s, %s) RETURNING id")
        cursor.execute(insert_query, (
            user_states[user_id]['data']['user_name'], user_states[user_id]['data']['phone_number'], file_name))
        inserted_id = cursor.fetchone()[0]

        print(works)
        print(companiya)

        # Bog'lanishni saqlash
        conn.commit()

        # Foydalanuvchiga habar berish
        bot.reply_to(message,
                     f"Fayl muvaffaqiyatli qabul qilindi va ma'lumotlar bazasiga saqlandi. (ID: {inserted_id})")

        back = types.KeyboardButton('🚪 Orqaga 🚪')
        # Menuni qaytarish
        bot.send_message(chat_id, "Bosh menuga qaytish uchun /start ni bosing.", reply_markup=back)
        cursor.close()
        conn.close()


    except Exception as e:
        print(e)
        bot.send_message(chat_id, "File qaytadan yuklang  !!!!!!!")
        bot.send_message(chat_id, "Iltimos button menu dan malumot qaytadan kiriting 👇🏻")

        print(1111111111111111111)


# ___________________________________________________________________


@bot.message_handler(func=lambda message: message.text == '💼 Ish haqida 💼')
def ish_haqid(message):
    chat_id = message.chat.id
    markup = bot_haqida_()
    bot.send_message(chat_id, 'Ish haqida', reply_markup=markup)
    bot.reply_to(message, "Biz Kirta oladigan ishalar\n"
                          " Menu\n"
                          "<-----------<0>---------->\n"
                          "1. IT sohasi (Information Technology)\n"
                          "2. Marketing\n"
                          "3. Xususiy va korporativ moliyaviy tashkilotlar\n"
                          "4. Turizm va mehmonxona boshqarmasi\n"
                          "5. Bank va moliya institutlari\n"
                          "6. Xususiy bog'lanishlar va kommunikatsiya\n"
                          "7. Xususiy bog'lanishlar va marketing\n"
                          "8. Xususiy madad va xizmat\n"
                          "9. Transport va logistika\n"
                          "11. Madaniyat va san'at\n"
                          "12. Xususiy bog'lanishlar va ko'p tilli xizmatlar\n"
                          "13. Maishiy xizmatlar va kasb-hunar ishlari\n"
                          "14. Xususiy bog'lanishlar va xalqaro iqtisodiyot\n"
                          "15. Xususiy bog'lanishlar va sifatli xizmatlar\n"
                          "16. Xususiy bog'lanishlar va xususiy tadbirkorlik\n"
                          "17. Xususiy bog'lanishlar va jismoniy kasb-hunar ishlari\n"
                          "20. Xususiy bog'lanishlar va telekommunikatsiya\n"

                          "🚪 Orqaga 🚪")
    first_name = message.from_user.first_name if message.from_user.first_name else "User"
    bot.send_message(chat_id, f'Rahmat 🥰, {first_name}!', reply_markup=markup)
    print()


@bot.message_handler(func=lambda message: message.text == '📱 Aloqa uchun 📱')
def aloqa_uchun(message):
    chat_id = message.chat.id
    markup = bot_haqida_()

    bot.send_message(chat_id, 'Siz Aloqa uchun menusiga kirdingiz', reply_markup=markup)
    bot.reply_to(message, "Salom! Sizda qanday dir savollar tug`ilgan bo`lsa bizga murojat qiling.\n"
                          "Bizning shaxsiy Call sizga 24/7 yordam berishadi.\n"
                          "Aloqa uchun : +(998)97-777-77-77.\n"
                          "Email : Root@gmail.com.\n")
    first_name = message.from_user.first_name if message.from_user.first_name else "User"
    bot.send_message(chat_id, f'Rahmat 🥰, {first_name}!', reply_markup=markup)
    print()


@bot.message_handler(func=lambda message: message.text == '🚪 Orqaga 🚪')
def ortga(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton('👨🏻‍💼 Ish Menu 👨🏻‍💼')
    item2 = types.KeyboardButton('💼 Ish haqida 💼')
    item3 = types.KeyboardButton('📱 Aloqa uchun 📱')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(item1, item2, item3, back)
    bot.send_message(chat_id, 'Salom 🙋🏿‍♂️, {0.first_name}!'.format(message.from_user), reply_markup=markup)


# Polling loop
bot.polling()