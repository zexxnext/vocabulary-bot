import os
import requests  
import datetime

import converter

from pymongo import MongoClient

class BotHandler:
    MONGODB_URI = os.environ.get('MONGODB_URI')
    if not MONGODB_URI:
        MONGODB_URI = 'mongodb://localhost:27017/heroku_hrltjgtb';
    
    client = MongoClient(MONGODB_URI)
    urls = client.heroku_hrltjgtb.urls
    not_service_args = lambda x: x not in ['_id', 'chat_id']
    default_category = 'default'
    
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
        text = '''/help - помощь
/start - о боте
/add [category] url - добавить url
/remove [category] url - удалить url
/list [category] - список url
/cremove category - удалить категорию
/cadd category - добавить категорию
/clist - список категорий
        '''
        return self.send_message(chat_id, text)
        
    @converter.not_empty
    def find(self, chat_id, create_from, filter):
        return [create_from(item, filter) for item in self.urls.find({'chat_id': chat_id})]

    def find_list(self, chat_id, category):
        return [category + ':'] + self.find(chat_id, converter.from_values, lambda x: x == category) + ['']

    def replace(self, chat_id, category, find_urls):
        self.urls.replace_one({'chat_id': chat_id, str(category): {'$exists': True}}, \
                  {'chat_id': chat_id, category: find_urls}, upsert=True)
                  
    def send(fn):
        def wrapped(self, chat_id, arguments):
            answer = fn(self, chat_id, arguments)                   
            self.send_message(chat_id, converter.to_string(answer))
        return wrapped
    
    def change_urls(fn):
        def wrapped(self, chat_id, arguments):
            category = arguments[0] if len(arguments) > 1 else self.default_category
            arguments = arguments[1:] if len(arguments) > 1 else arguments
           
            find_urls = self.find(chat_id, converter.from_values, lambda x: x == category)   
            
            if len(find_urls) > 0:
                find_urls = converter.from_string(find_urls[0])        
            find_urls, message = fn(self, find_urls, arguments)   
            self.replace(chat_id, category, find_urls)
          
            return message
        return wrapped

    @send
    @change_urls
    def add_message(self, find_urls, arguments):
        return find_urls + [url for url in arguments if url not in find_urls], \
            'Добавлено успешно!'

    @send
    @change_urls
    def remove_message(self, find_urls, arguments):
        return [url for url in find_urls if url not in arguments], \
            'Удалено успешно!'

    @send
    def get_urls_message(self, chat_id, arguments):
        if len(arguments) > 0:
            return self.find_list(chat_id, arguments[0])
        else:
            categories = self.find(chat_id, converter.from_keys, BotHandler.not_service_args)
            return [converter.to_string(self.find_list(chat_id, category)) \
                    for category in categories]

    def to_string(find):
        def wrapped(self, chat_id, category):
            return converter.to_string(find(self, chat_id, category)).split('\n')
        return wrapped              
                    
                    
    @to_string              
    def find_urls(self, chat_id, category):
        return self.find(chat_id, converter.from_values, \
            lambda x: x == category if category else BotHandler.not_service_args)

    @send
    def get_categories_message(self, chat_id, arguments):
        return self.find(chat_id, converter.from_keys, BotHandler.not_service_args)

    @send
    @change_urls
    def add_category_message(self, find_urls, arguments):
        return [], 'Категория добавлена успешно!'

    @send
    @change_urls
    def remove_category_message(self, find_urls, arguments):
        return [], 'Категория удалена успешно!'
    
    cmds = {
        '/help': help_message,
        '/start': start_message,
        '/add': add_message,
        '/remove': remove_message,
        '/list': get_urls_message,
        '/clist': get_categories_message,
        '/cadd': add_category_message,
        '/cremove': remove_category_message,
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
