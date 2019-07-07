import constants
import telebot
from telebot import apihelper
import time
import threading
from datetime import datetime

# modules
from modules.weather import main as weather
from modules.price_checking import main as price_checking
from modules.news import main as news
from logger import logger
from modules.neuro import main as neuro
from modules.location import main as locations
# /import


def input_url(message):
    answer = price_checking.save_item_url(message)
    bot.send_message(message.chat.id,answer)
    logger.consoleLog(message, answer)

def input_index_of_url(message):
    answer = price_checking.delete_item_url(message)
    bot.send_message(message.chat.id,answer)
    logger.consoleLog(message, answer)


apihelper.proxy = {'https':'http://130.211.83.74:3128'}
#= немецкий прокси
bot = telebot.TeleBot(constants.token, threaded=False)

print(bot.get_me())

# /bot started


def tracking():
    threading.Timer(60.0, tracking).start()
    d_now = datetime.now()
    if (d_now.minute == 30):
        price_checking.send_items_prices(bot)
    if (d_now.hour % 2 == 0 and d_now.minute == 00):
        news.sendNews(bot)
    if(d_now.hour % 2 != 0 and d_now.minute == 50):
        weather.sendWeather(bot)

def makeKeyboard(obj, hide = True):
    user_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in obj:
        user_keyboard.add(i)
    return user_keyboard

def sendAnswer(message, answer):
    if (type(answer) is dict):
        if('keyboard' in answer):
            bot.send_message(message.chat.id, answer['text'], reply_markup=makeKeyboard(answer['keyboardData']))
        else:
            bot.send_message(message.chat.id, answer['text'], reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, answer, reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(commands=["start"])
def handle_command(message):
    bot.send_message(message.chat.id, "Приветствую тебя")

#==== Погода
@bot.message_handler(commands=["weather"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = weather.getWeather()
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(commands=["weather_sub"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = weather.subscribeWeather(message.chat.id)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(commands=["weather_unsub"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = weather.unsubscribeWeather(message.chat.id)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

#==== Отслеживание
@bot.message_handler(commands=["items"])
def handle_command(message):
    bot.send_chat_action(message.chat.id,"typing")
    answer = price_checking.get_items_prices(message.chat.id)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(commands=['itemadd'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Введите URL")
    bot.register_next_step_handler(msg, input_url)

@bot.message_handler(commands=['itemdel'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, "typing")
    msg = bot.send_message(message.chat.id, "Введите номер ссылки из списка")
    bot.register_next_step_handler(msg, input_index_of_url)


#==== Новости
def saveUserNewsRegion(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = locations.saveLocation('news', message)
    sendAnswer(message, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(commands=["news"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = news.getNews(message.chat.id)
    sendAnswer(message, answer)

    if(type(answer) is dict and answer['type'] == 'chooseRegion'):
        bot.register_next_step_handler(message,saveUserNewsRegion)

    logger.consoleLog(message, answer)

@bot.message_handler(commands=["news_sub"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = news.subscribeNews(message.chat.id)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(commands=["news_unsub"])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = news.unsubscribeNews(message.chat.id)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

@bot.message_handler(content_types=['text'])
def handle_command(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = neuro.openai(message)
    bot.send_message(message.chat.id, answer)
    logger.consoleLog(message, answer)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

tracking()

#bot.infinity_polling(True)
#bot.polling(none_stop=True)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.log(e)
        print(e)
        time.sleep(15)




