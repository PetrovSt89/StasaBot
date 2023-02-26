import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import greet_user, guess_number, send_cat_picture_two, user_coordinates, talk_to_me, planets

import settings

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
    
def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planets))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture_two))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать кота)$'), send_cat_picture_two))
    dp.add_handler(MessageHandler(Filters.regex('^(Игра)$'), guess_number))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logger.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":    
    main()    