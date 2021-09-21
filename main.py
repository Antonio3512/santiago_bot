import telebot
import time
from threading import Timer

TOKEN = "1902178099:AAFnA5mgWb9eSMD7dV2ktcinaehhPFN-MX8"

bot = telebot.TeleBot(TOKEN)

alreadyCounting = {}

poshelArray = ["пашол", "пошел", "пошёл", "пашел", "пошол"]


def count_back(id):
    for i in reversed(range(10)):
        bot.send_message(id, i + 1)
        time.sleep(1)
    alreadyCounting[id] = False
    bot.send_message(id, "ПОПИЗДОВАЛИ")
    bot.send_sticker(id, "CAACAgIAAxkBAAEC7whhSGL2N-Xr2p9pZ_j_ztCFvvh8qwACUAADi_RmLF1_8lSVNSnvIAQ")


def count_time(message):
    if message.chat.id in alreadyCounting and alreadyCounting[message.chat.id]:
        bot.send_message(message.chat.id, "Не мешай, я уже считаю, я один блядь")
        return
    if not message.text[:-1].isdigit():
        bot.send_message(message.chat.id, "Бота мне не кладите, пидоры")
        return

    mins = int(message.text[:-1])
    if mins < 1:
        bot.send_message(message.chat.id, "Меньше курить надо, побольше время введи")
        return
    if mins > 120:
        bot.send_message(message.chat.id, f"Молодец, ты покуришь через {round(mins / 60, 1)} ч. примерно")
        return

    alreadyCounting[message.chat.id] = True
    bot.send_message(message.chat.id, f'Засёк {mins} мин')

    timer = Timer(mins * 60, count_back, args=(message.chat.id, ))
    timer.start()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower == "привет":
        bot.send_message(message.chat.id, "Ну здарова, падла")
    if message.text.lower() in poshelArray:
        bot.send_message(message.chat.id, "нахуй)0), дурак кожаный")
    if message.text.endswith('!'):
        count_time(message)


bot.polling(none_stop=True, interval=0)
