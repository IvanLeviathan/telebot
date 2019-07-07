import sys
modulesConstants = {
    "newsSite": "https://yandex.ru/",
    "subscribersList" : sys.path[0] + "/modules/news/files/subscribersList.json",
    "customersNewsCitys": sys.path[0] + "/modules/news/files/customersCitys.json",
}

lang = {
    "newsListHeader": "Новости на\n{0}\n{1} \n\n",
    "alreadySubscribed": "Вы уже подписаны на рассылку новостей",
    "successSubscribed": "Вы успешно подписались на рассылку новостей",
    "notSubscribed": "Вы не подписаны на рассылку новостей",
    "successUnsubscribed":"Вы успешно отписались от рассылки новостей"
}