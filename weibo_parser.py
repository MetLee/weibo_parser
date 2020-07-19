from telegram.ext import Updater

from config import config
from handlers import handlers

def main():
    updater = Updater(token=config['token'], use_context=True)
    dispatcher = updater.dispatcher
    for handler in handlers:
        dispatcher.add_handler(handler)
    updater.start_polling()
    
if __name__ == '__main__':
    main()
