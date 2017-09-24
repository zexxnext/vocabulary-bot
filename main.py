import os
import requests  
from bot_handler import BotHandler

API_TOKEN = os.environ.get('API_TOKEN')
if not API_TOKEN:
    API_TOKEN = 'XXX'
        
w_bot = BotHandler(API_TOKEN)  

def main():  
    new_offset = None
    
    while True:
        w_bot.get_updates(new_offset)
        last_update = w_bot.get_last_update()

        if not last_update:
            continue

        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']

        if last_chat_text[0] == '/':
            command, *arguments = last_chat_text.split(" ")
            try:
                w_bot.cmds[command](w_bot, last_chat_id, arguments)
            except KeyError:
                w_bot.send_message(last_chat_id, "Нет такой команды.")
        else:
            words = last_chat_text.split(' ')
            w_urls = [url + (words[1] if len(words) > 1 else last_chat_text) \
                for url in w_bot.find_urls(last_chat_id, (words[0] if len(words) > 1 else None))]
            
            for url in w_urls:
                w_bot.send_message(last_chat_id, url)

        new_offset = last_update['update_id'] + 1
        
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
