import telebot
import time
from threading import Timer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", help="telegram bot token", dest="<TOKEN>", required=True)
args = parser.parse_args()

bot = telebot.TeleBot(args.token)

# массив состояний бота в разных чатах
alreadyCounting = {}

# массив слов для команды ping
wentArray = ["пашол", "пошел", "пошёл", "пашел", "пошол"]


# обратный отсчет
def count_back(chat_id):
    for i in reversed(range(10)):
        bot.send_message(chat_id, i + 1)
        time.sleep(1)
    alreadyCounting[chat_id] = False
    bot.send_message(chat_id, "ПОПИЗДОВАЛИ")
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEC7whhSGL2N-Xr2p9pZ_j_ztCFvvh8qwACUAADi_RmLF1_8lSVNSnvIAQ")


# обработка команды создания таймера
def count_time(message):
    if message.chat.id in alreadyCounting and alreadyCounting[message.chat.id]:
        bot.send_message(message.chat.id, "Не мешай, я уже считаю, я один блядь")
        return
    if not message.text[:-1].isdigit():
        bot.send_message(message.chat.id, "Бота мне не кладите, пидоры")
        return

    minutes = int(message.text[:-1])
    if minutes < 1:
        bot.send_message(message.chat.id, "Меньше курить надо, побольше время введи")
        return
    if minutes > 120:
        bot.send_message(message.chat.id, f"Молодец, ты покуришь через {round(minutes / 60, 1)} ч. примерно")
        return

    alreadyCounting[message.chat.id] = True
    bot.send_message(message.chat.id, f'Засёк {minutes} мин')

    timer = Timer(minutes * 60, count_back, args=(message.chat.id,))
    timer.start()


# обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.lower()

    if text == "привет":
        bot.send_message(message.chat.id, "Ну здарова, падла")

    if text in wentArray:
        bot.send_message(message.chat.id, "нахуй)0), дурак кожаный")

    if text.endswith('!'):
        count_time(message)


bot.polling(none_stop=True, interval=0)
