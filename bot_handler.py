import requests  
import datetime
 
class BotHandler:
    urls = {}

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

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
            if not chat_id in self.urls:
                self.urls[chat_id] = []

            fn(self, chat_id, arguments)

            for url in self.urls[chat_id]:
                self.send_message(chat_id, url)
            
        return wrapped

    @d_urls
    def add(self, chat_id, arguments):
        self.urls[chat_id].extend(arguments)

    @d_urls
    def remove(self, chat_id, arguments):
        self.urls[chat_id] = [url for url in self.urls if url not in arguments]

    @d_urls
    def get_urls(self, chat_id, arguments):
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
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()
 
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            print(get_result)
            print(len(get_result))
            last_update = get_result[len(get_result)]
 
        return last_update
