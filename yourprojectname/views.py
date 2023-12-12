from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import telebot

TELEGRAM_BOT_TOKEN = 'SIZNING_TELEGRAM_BOT_TOKENINGIZ'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@csrf_exempt
def your_bot_command(request):
    json_str = request.body.decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return JsonResponse({'status': 'ok'})