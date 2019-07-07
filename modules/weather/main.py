from .constants import modulesConstants
from .constants import lang
import requests
import json
import os.path as path
from datetime import datetime

def sendWeather(bot):
    weatherMsg = makeWeatherMsg(loadWeather())
    if (path.isfile(modulesConstants["subscribersList"])):
        jsonFile = open(modulesConstants["subscribersList"], "r+")
    else:
        jsonFile = open(modulesConstants["subscribersList"], "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if contents:
        object = json.loads(contents)
        for chat_id in object:
            bot.send_message(chat_id, weatherMsg)
            print("Отправили погоду " + str(chat_id))


def subscribeWeather(chat_id):
    if (path.isfile(modulesConstants["subscribersList"])):
        jsonFile = open(modulesConstants["subscribersList"], "r+")
    else:
        jsonFile = open(modulesConstants["subscribersList"], "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if not contents:
        object = []
        object.append(chat_id)
    else:
        object = json.loads(contents)

        if chat_id in object:
            return lang["alreadySubscribed"]
        else:
            object.append(chat_id)

    with open(modulesConstants["subscribersList"], 'w') as outfile:
        json.dump(object, outfile)

    return lang["successSubscribed"]

def unsubscribeWeather(chat_id):
    if (path.isfile(modulesConstants["subscribersList"])):
        jsonFile = open(modulesConstants["subscribersList"], "r+")
    else:
        jsonFile = open(modulesConstants["subscribersList"], "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if not contents:
        return lang["notSubscribed"]
    else:
        object = json.loads(contents)

        if chat_id in object:
            object.remove(chat_id)
        else:
            return lang["notSubscribed"]


    with open(modulesConstants["subscribersList"], 'w') as outfile:
        json.dump(object, outfile)

    return lang["successUnsubscribed"]



def loadWeather():
    url = modulesConstants["weather_url"] + "?q={0}&units=metric&lang=ru&APPID={1}".format(modulesConstants["weather_region"],modulesConstants["APPID"])
    res = requests.get(url)
    return res.json()

def makeWeatherMsg(data):
    now = datetime.now()
    nowStr = now.strftime("%d.%m.%Y %H:%M")
    weather = "Погода в Волгограде на {0}\n".format(nowStr)
    weather += str(round(data['main']['temp'])) + "°, " + data['weather'][0]['description'] + " " + modulesConstants["weather_emoji"][data['weather'][0]['main']]

    return weather


def getWeather():
    return makeWeatherMsg(loadWeather())