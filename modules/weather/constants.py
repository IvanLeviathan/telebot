import sys
modulesConstants = {
    "weather_url" : "http://api.openweathermap.org/data/2.5/weather",
    "weather_region":   "Volgograd,RU",
    "APPID":    "e60e657295a8f228b0df7fe40c000b89",
    "weather_emoji" : {
        "Clear": "☀",
        "Clouds":"☁",
        "Rain":"🌧"
    },
    "subscribersList" : sys.path[0] + "/modules/weather/files/subscribersList.json"
}

lang = {
    "alreadySubscribed": "Вы уже подписаны на рассылку погоды",
    "successSubscribed": "Вы успешно подписались на рассылку погоды",
    "notSubscribed": "Вы не подписаны на рассылку погоды",
    "successUnsubscribed":"Вы успешно отписались от рассылки погоды"
}