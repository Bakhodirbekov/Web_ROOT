from telebot import types



def bot_haqida_():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add('🚪 Orqaga 🚪')

    return markup

bot_haqida_()