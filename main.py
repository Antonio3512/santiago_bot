import telebot
import time
from threading import Timer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", help="telegram bot token", dest="token", required=True)
args = parser.parse_args()

bot = telebot.TeleBot(args.token)

# Мапа чатов
chats = {}


# Класс состояний чата
class ChatState:
    def __init__(self):
        self.already_counting = False
        self.timer = None
        self.end_time = None


# массив состояний бота в разных чатах
alreadyCounting = {}

# массив таймеров по id чата
timers = {}

# массив слов для команды ping
wentArray = ["пашол", "пошел", "пошёл", "пашел", "пошол"]


# обратный отсчет
def count_back(chat_id):
    chats[chat_id].timer = None

    for i in reversed(range(10)):
        bot.send_message(chat_id, i + 1)
        time.sleep(1)

    chats[chat_id].already_counting = False

    bot.send_message(chat_id, "ПОПИЗДОВАЛИ")
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEC7whhSGL2N-Xr2p9pZ_j_ztCFvvh8qwACUAADi_RmLF1_8lSVNSnvIAQ")


def stop_counting(chat_id):
    chats[chat_id].timer.cancel()
    chats[chat_id].timer = None
    chats[chat_id].already_counting = False
    bot.send_message(chat_id, "Стою, стою...")


# обработка команды создания таймера
def count_time(message):
    if chats[message.chat.id].already_counting:
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

    chats[message.chat.id].already_counting = True
    bot.send_message(message.chat.id, f'Засёк {minutes} мин')

    chats[message.chat.id].end_time = time.time() + (minutes * 60)
    chats[message.chat.id].timer = Timer(minutes * 60, count_back, args=(message.chat.id,))
    chats[message.chat.id].timer.start()


# обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здарова, заебал)\n\n'
                                      'Я Саньтьяго, приехал с Кубы, чтобы дымить здесь.\n\n'
                                      'Скажи мне через сколько курим\n'
                                      '(10! - означает что курим через 10 минут)\n\n'
                                      'Если че не понял тебе туда /help')


# обработка команды /help
@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, 'Бля, ну ты тупой или прикидываешься?\n'
                                      'Я же сказал 10! - через 10 минут курим\n'
                                      'Включи тыкву 5! - это 5 минут\n'
                                      'А я уже посчитаю, и напомню тебе)')


# обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = message.text.lower()
    chat_id = message.chat.id

    if chat_id not in chats:
        chats[chat_id] = ChatState()

    if text == "привет":
        bot.send_message(chat_id, "Ну здарова, падла")

    if text in wentArray:
        bot.send_message(chat_id, "нахуй)0), дурак кожаный")

    if text == "стопэ":
        if chats[chat_id].already_counting and chats[chat_id].timer:
            stop_counting(chat_id)
            return
        if chats[chat_id].already_counting and chats[chat_id].timer is None:
            bot.send_message(chat_id, "Чуть чуть потерпи, заебал")
            return
        bot.send_message(chat_id, "Ты ниче не засек")

    if text == "скока":
        bot.send_message(chat_id, f"Осталось {time.strftime('%M:%S', time.gmtime(chats[chat_id].end_time - time.time()))}")

    if text.endswith('!'):
        count_time(message)


bot.polling(none_stop=True, interval=0)
