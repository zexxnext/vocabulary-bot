import requests  
from bot_handler import BotHandler

w_bot = BotHandler('439715244:AAFIfeze5ggTKd6PfVPoP6LXB0u6PD-2ojw')  

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
            command, *arguments = last_chat_text.split(" ", 1)
            w_bot.cmds[command](w_bot, last_chat_id, arguments)
        else:
            w_urls = [url + last_chat_text for url in w_bot.urls[last_chat_id]]

            for url in w_urls:
                w_bot.send_message(last_chat_id, url)

        new_offset = last_update['update_id'] + 1
        
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
