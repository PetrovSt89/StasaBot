import logging
from glob import glob
from random import choice

import ephem


from utils import get_smile, play_random_numbers, main_keyboard

logger = logging.getLogger(__name__)

def greet_user(update, context):
    logger.info('Вызван /start')

    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text('Привет, пользователь! {cont}'.format(
        cont=context.user_data["emoji"]), reply_markup=main_keyboard())
    
def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    
    text = update.message.text 
    logger.info(text)
    update.message.reply_text(f'{text} {context.user_data["emoji"]}', reply_markup=main_keyboard())       
    
def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число, пример: '/guess 7'"
    else:
        message = "Введите целое число, пример: '/guess 7'"
    update.message.reply_text(message, reply_markup=main_keyboard())  
 
def send_cat_picture_two(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    update.message.reply_photo(open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())    

# def send_cat_picture(update, context):
#     cat_photos_list = glob('images/cat*.jp*g')
#     cat_pic_filename = choice(cat_photos_list)
#     chat_id = update.effective_chat.id
#     context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))    

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )    

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
    update.message.reply_text(f'это координаты Марса {constel} что бы это не значило',reply_markup=main_keyboard())  







