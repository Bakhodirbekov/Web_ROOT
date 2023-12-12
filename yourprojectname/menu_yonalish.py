from telebot import types
def user_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    item1 = types.KeyboardButton(' Fastfood ')
    item2 = types.KeyboardButton(' Kiyim Dokon ')
    item3 = types.KeyboardButton(' Mobil Opertor ')
    item4 = types.KeyboardButton(' Super Market ')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(item1, item2, item3,item4, back)

    return markup