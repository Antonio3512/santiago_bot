import telebot
import time
from threading import Timer
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--token', help='telegram bot token', dest='token', required=True)
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

# массивы слов
wentArray = ['пашол', 'пошел', 'пошёл', 'пашел', 'пошол']
helloArray = ['привет', 'здарова']
stopArray = ['стопэ', 'остановись']
howManyArray = ['скока', 'скоро']
nameArray = ['падла', 'дурак кожаный', 'псина']
stickerArray = ['CAACAgIAAxkBAAEC7whhSGL2N-Xr2p9pZ_j_ztCFvvh8qwACUAADi_RmLF1_8lSVNSnvIAQ']


# случайное обращение
def name():
    return random.choice(nameArray)


# случайный стикер
def sticker():
    return random.choice(stickerArray)


# обратный отсчет
def count_back(chat_id):
    chats[chat_id].timer = None

    for i in reversed(range(10)):
        bot.send_message(chat_id, i + 1)
        time.sleep(1)

    chats[chat_id].already_counting = False

    bot.send_message(chat_id, 'ПОПИЗДОВАЛИ')
    bot.send_sticker(chat_id, sticker())


# остановка таймера
def stop_counting(chat_id):
    chats[chat_id].timer.cancel()
    chats[chat_id].timer = None
    chats[chat_id].already_counting = False
    bot.send_message(chat_id, 'Стою, стою...')


# обработка команды создания таймера
def count_time(message):
    chat_id = message.chat.id

    if chats[chat_id].already_counting:
        bot.send_message(chat_id, 'Не мешай, я уже считаю, я один блядь')
        return

    if not message.text[:-1].isdigit():
        bot.send_message(chat_id, f'Бота мне не клади, {name()}')
        return

    minutes = int(message.text[:-1])

    if minutes < 1:
        bot.send_message(chat_id, 'Меньше курить надо, побольше время введи')
        return

    if minutes > 120:
        bot.send_message(chat_id, f'Молодец, ты покуришь через {round(minutes / 60, 1)} ч. примерно')
        return

    chats[chat_id].already_counting = True
    bot.send_message(chat_id, f'Засёк {minutes} мин')

    chats[chat_id].end_time = time.time() + (minutes * 60)
    chats[chat_id].timer = Timer(minutes * 60, count_back, args=(chat_id,))
    chats[chat_id].timer.start()


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

    if text in helloArray:
        bot.send_message(chat_id, f'Ну здарова, {name()}')

    if text in wentArray:
        bot.send_message(chat_id, f'нахуй)0), {name()}')

    if text in stopArray:
        if chats[chat_id].already_counting and chats[chat_id].timer:
            stop_counting(chat_id)
            return
        if chats[chat_id].already_counting and chats[chat_id].timer is None:
            bot.send_message(chat_id, 'Чуть чуть потерпи, заебал')
            return
        bot.send_message(chat_id, 'Ты ниче не засек')

    if text in howManyArray:
        time_text = time.strftime('%M:%S', time.gmtime(chats[chat_id].end_time - time.time()))
        bot.send_message(chat_id, f'Осталось {time_text}')

    if text.endswith('!'):
        count_time(message)


bot.polling(none_stop=True, interval=0)
