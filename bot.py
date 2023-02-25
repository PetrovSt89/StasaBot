"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
from emoji import emojize
from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import ephem

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

def greet_user(update, context):
    logger.info('Вызван /start')

    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text('Привет, пользователь! {cont}'.format(
        cont=context.user_data["emoji"]
    ))

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    
    text = update.message.text 
    logger.info(text)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}')

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']    

def planets(update, context):
    enter_text = update.message.text
    enter_text = enter_text.split()
    planet_name = enter_text[1]    
    if planet_name == 'Mars':
        planet = ephem.Mars('2023/02/16')
    elif planet_name == 'Pluto':
        planet = ephem.Pluto('2023/02/16')    
    else:
        update.message.reply_text('Я не знаю таких планет')
        return
    constel = ephem.constellation(planet) 
    logger.info('Вызван /planet')
    update.message.reply_text(constel)  

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)        

# def send_cat_picture(update, context):
#     cat_photos_list = glob('images/cat*.jp*g')
#     cat_pic_filename = choice(cat_photos_list)
#     chat_id = update.effective_chat.id
#     context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


def send_cat_picture_two(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    update.message.reply_photo(open(cat_pic_filename, 'rb'))


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planets))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture_two))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logger.info("Бот стартовал")

    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":    
    main()    