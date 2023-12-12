from telebot import types
def user_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    item1 = types.KeyboardButton('👨🏻‍💼 Ish Menu 👨🏻‍💼')
    item2 = types.KeyboardButton('💼 Ish haqida 💼')
    item3 = types.KeyboardButton('📱 Aloqa uchun 📱')
    back = types.KeyboardButton('🚪 Orqaga 🚪')

    markup.add(item1, item2, item3, back)

    return markup