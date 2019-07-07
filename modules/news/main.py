from bs4 import BeautifulSoup as Soup
import requests
from datetime import datetime
import os.path as path
import json
from .constants import modulesConstants
from .constants import lang
from modules.location import main as locations
import xml.etree.ElementTree as ET
from logger import logger

def sendNews(bot):
    if (path.isfile(modulesConstants["subscribersList"])):
        jsonFile = open(modulesConstants["subscribersList"], "r+")
    else:
        jsonFile = open(modulesConstants["subscribersList"], "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if contents:
        object = json.loads(contents)

        for chat_id in object:
            userLocation = locations.getParseLink('news', chat_id);
            if('link' in userLocation):
                newsList = getNews(chat_id)

                bot.send_message(chat_id, newsList)
                print("Отправили новости " + str(chat_id))


def getNews(chat_id):

    userLocation = locations.getParseLink('news', chat_id);

    if('keyboard' in userLocation):
        return userLocation

    if('link' in userLocation):
        response = requests.get(userLocation['link'])
        try:
            root = ET.fromstring(response.content)
        except Exception as e:
            logger.log(e)
        now = datetime.now()
        nowStr = now.strftime("%d.%m.%Y %H:%M")
        newsList = lang["newsListHeader"].format(nowStr,userLocation['name'])
        count = 0
        for child in root.find('channel'):
            if(child.tag == 'item'):
                newsList+=child.find('title').text
                newsList += '\n'
                newsList += child.find('link').text
                newsList += '\n\n'
                count += 1
                if(count >= 5):
                    break
    return newsList



def subscribeNews(chat_id):

    userLocation = locations.getParseLink('news', chat_id);
    if ('keyboard' in userLocation):
        return userLocation

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

def unsubscribeNews(chat_id):
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