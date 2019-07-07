from bs4 import BeautifulSoup as Soup
import requests
import os.path as path
import json

from .constants import modulesConstants

pricesList = modulesConstants["pricesList"]


def send_items_prices(bot):
    if (path.isfile(pricesList)):
        jsonFile = open(pricesList, "r")
        contents = jsonFile.read()
        jsonFile.close()
        if contents:
            object = json.loads(contents)
            for user_id in object:
                linksList = ""
                for key, link in enumerate(object[user_id]):
                    linksList += makeProductInList(key,link)
                if linksList:
                    bot.send_message(user_id, linksList)

        else:
            return "Нет отслеживаеммых ссылок."
    else:
        return "Нет отслеживаеммых ссылок."



def get_items_prices(chat_id):
    if (path.isfile(pricesList)):
        jsonFile = open(pricesList, "r")
        contents = jsonFile.read()
        jsonFile.close()
        if contents:
            object = json.loads(contents)
            thisChat = object[str(chat_id)]
            if thisChat:
                linksList = ""
                for key, link in enumerate(thisChat):
                    linksList += makeProductInList(key,link, False)
                if not linksList:
                    return "Изменений в ценах нет"
                else:
                    return linksList
            else:
                return "У Вас нет отслеживаеммых ссылок."
        else:
            return "У Вас нет отслеживаеммых ссылок."
    else:
        return "У Вас нет отслеживаеммых ссылок."




def save_item_url(message):

    chat_id = str(message.chat.id)
    url = str(message.text)

    if 'http' not in url:
        return '"{0}" не является ссылкой'.format(url)

    if(path.isfile(pricesList)):
        jsonFile = open(pricesList, "r+")
    else:
        jsonFile = open(pricesList, "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if not contents:
        object = {}
        object[chat_id] = []
        object[chat_id].append(url)
    else:
        object = json.loads(contents)

        if chat_id not in object:
            object[chat_id] = []

        if url not in object[chat_id]:
            object[chat_id].append(url)
        else:
            return "Ссылка {0} уже отслеживается Вами.".format(url)


    with open(pricesList, 'w') as outfile:
        json.dump(object, outfile)

    return "Ссылка {0} успешно добавлена в список отслеживаемых.".format(url)



def delete_item_url(message):
    chat_id = str(message.chat.id)
    index = message.text

    if not index.isdigit():
        return "Вы ввели НЕ число"

    if (path.isfile(pricesList)):
        jsonFile = open(pricesList, "r+")
    else:
        jsonFile = open(pricesList, "w+")

    contents = jsonFile.read()
    jsonFile.close()

    if not contents:
        return "Список ваших ссылок пуст"
    else:
        object = json.loads(contents)

        if chat_id not in object:
            return "Список ваших ссылок пуст"

        if len(object[chat_id]) >= int(index) and int(index) > 0:
            del object[chat_id][int(index) - 1]
        else:
            return index + " - нет в списке ваших отслеживаемых ссылок"

        with open(pricesList, 'w') as outfile:
            json.dump(object, outfile)

        return "Ссылка под номером " + index + " удалена из списка отслеживаемых"

def makeProductInList(key,link, save=True):
    name = ''
    price = ''

    if save:
        if (path.isfile(modulesConstants["prices"])):
            pricesFile = open(modulesConstants["prices"], "r+")
        else:
            pricesFile = open(modulesConstants["prices"], "w+")

        contents = pricesFile.read()
        pricesFile.close()

        if contents:
            object = json.loads(contents)
        else:
            object = {}

    try:
        html = Soup(requests.get(link).text, "html.parser")

        if "mvideo.ru" in link:
            price = html.find("div",class_="sel-product-tile-price").text.strip()[:-1] + " руб."
            name = html.find("h1", class_="sel-product-title").text.strip()

            html.find('div', class_="c-zoom").decompose()

            notifications = set(html.find_all("span", class_="c-notifications__title"))
            for notification in notifications:
                price += "\n❗" + notification.text.strip()

        if "eldorado.ru" in link:
            price = html.find("div", class_="product-box-price__active").text.strip()[:-3] + " руб."
            name = html.find("h1", class_="catalogItemDetailHd").text.strip()

            notifications = set(html.find_all("div", class_="cartText"))
            for notification in notifications:
                price += "\n❗" + notification.text.strip()

        if "dns-shop.ru" in link or "technopoint.ru" in link:
            price = html.find("span", class_="current-price-value").text.strip() + " руб."
            name = html.find("h1").text.strip()

            notifications = set(html.find_all("span", class_="avail-text"))
            for notification in notifications:
                price += "\n❗" + notification.text.strip()

        if "store.steampowered.com" in link:
            price = html.find("div", class_="game_purchase_price").text.strip()
            name = html.find("div", class_="apphub_AppName").text.strip()

        if "citilink.ru" in link:
            price = html.find("div", class_="price_break")
            if price:
                price = price.text.strip()
            else:
                price = "\n❗ Товара нет в наличии"

            name = html.find("h1").text.strip()

        if "onlinetrade.ru" in link:
            price = html.find("span", attrs={"itemprop":"price"}).text.strip() + " руб."
            name = html.find("h1").text.strip()

        if save:
            if link in object and object[link] == price:
                return ''
            else:
                object[link] = price
                with open(modulesConstants["prices"], 'w') as outfile:
                    json.dump(object, outfile)


        return str(key + 1) + ". " + name.strip() + "\n" + price.strip() + "\n" + link + "\n\n"
    except Exception as e:
        from logger import logger
        logger.log(e)
        return str(key + 1) + '. Не удалось распарсить ' + link + "\n\n"

