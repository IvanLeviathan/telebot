from .constants import modulesConstants
from .constants import lang
import json
import os.path as path
from logger import logger

def getParseLink(mode, chat_id):
    chat_id = str(chat_id)
    if(not chat_id or not mode):
        return {
            "error": True,
            "msg": lang['noChatId'],
        }

    file = modulesConstants[mode]

    if (path.isfile(file)):
        jsonFile = open(file, "r+")
        contents = jsonFile.read()
        jsonFile.close()

        if contents:
            object = json.loads(contents)

            if chat_id in object:
                return {
                    "success": True,
                    "link": object[chat_id],
                    "name": getKey(modulesConstants[mode+'List'], object[chat_id])
                }
            else:
                return makeButtonsList(mode)
        else:
            return makeButtonsList(mode)
    else:
        createLocationFile(file)
        getParseLink(mode, chat_id)


def createLocationFile(name):
    open(name, 'a').close()

def makeButtonsList(mode):
    return {
        "keyboard": True,
        "keyboardData": modulesConstants[mode+'List'],
        "text": lang['chooseYourRegion'],
        "type": 'chooseRegion'
    }


def saveLocation(mode, message):
    chat_id = str(message.chat.id)
    value = message.text
    if (path.isfile(modulesConstants[mode])):
        jsonFile = open(modulesConstants[mode], "r+")
        contents = jsonFile.read()
        jsonFile.close()

        if not contents:
            object = {}
        else:
             object = json.loads(contents)

        if (value in modulesConstants[mode+'List']):

            if(chat_id in object):
                del object[chat_id]

            object[chat_id] = modulesConstants[mode + 'List'][value]
            with open(modulesConstants[mode], 'w') as outfile:
                json.dump(object, outfile)
            return {
                'success': True,
                'text': lang['locationSaved'].format(value)
            }
        else:
            return {
                'error': True,
                'text': lang['locationNotFound']
            }
    else:
        return {
            'error': True,
            'text': lang['locationSaveError']
        }

def getKey(d, value):
    for k, v in d.items():
        if v == value:
            return k