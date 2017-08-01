import os
import requests  
import datetime
from pymongo import MongoClient

class BotHandler:

    MONGO_URL = os.environ.get('MONGO_URL')
    if not MONGO_URL:
        MONGO_URL = 'mongodb://localhost:27017/rest';
    
    client = MongoClient(MONGO_URL)
    urls = client.vocabulary_bot.urls

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        return requests.post(self.api_url + method, params)

    def start_message(self, chat_id, arguments):
        text = "Бот-словарь. Бот хранит список ссылок, куда подставляет слова, \
которые посылает пользователь. Например: хранится url - http://wooordhunt.ru/word/, пользователь \
посылает слово - love и получает в ответ ссылку - http://wooordhunt.ru/word/love."
        return self.send_message(chat_id, text)

    def help_message(self, chat_id, arguments):
        text = '''/help - помощь,
/start - о боте,
/add url - добавить url,
/remove url - удалить url,
/list - список url
        '''
        return self.send_message(chat_id, text)

    def d_urls(fn):
        def wrapped(self, chat_id, arguments):
            if not self.find(chat_id):
                self.urls.insert_one({'chat_id': chat_id, 'urls': []})

            find_urls = self.find(chat_id)['urls']
            
            fn(self, find_urls, arguments)

            self.urls.replace_one({'chat_id': chat_id}, {'chat_id': chat_id, 'urls': find_urls})

            for url in find_urls:
                self.send_message(chat_id, url)
            
        return wrapped

    def find(self, chat_id):
        return self.urls.find_one({'chat_id': chat_id})

    @d_urls
    def add(self, find_urls, arguments):
        find_urls.extend(arguments)

    @d_urls
    def remove(self, find_urls, arguments):
        find_urls = [url for url in find_urls if url not in arguments]

    @d_urls
    def get_urls(self, find_urls, arguments):
        pass
     
    cmds = {
        '/help': help_message,
        '/start': start_message,
        '/add': add,
        '/remove': remove,
        '/list': get_urls
    }

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
 
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        return requests.get(self.api_url + method, params).json()['result']

    def get_last_update(self):
        get_result = self.get_updates()
 
        if len(get_result) > 0:
            return get_result[-1]
        return {}
