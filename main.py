import telebot
from telebot import types
import database
from dotenv import load_dotenv
import os
from telegram_bot_pagination import InlineKeyboardPaginator

load_dotenv()

secret = os.getenv('TOKEN')

bot = telebot.TeleBot(secret)
database.create_table()
# database.add_my_movies()

new_movie = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Выбрать из библиотеки', callback_data='choose')
    btn2 = types.InlineKeyboardButton('Добавить новую идею', callback_data='add')
    btn3 = types.InlineKeyboardButton('Случайный фильм', callback_data='random')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Я помогу тебе выбрать, что посмотреть. Что ты хочешь сделать?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'choose':
        info = database.get_movies()
        bot.send_message(call.message.chat.id, 'Напишите номер понравившегося фильма:')
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
        markup.add(btn1)
        bot.send_message(call.message.chat.id, info, reply_markup=markup)
    if call.data == 'back':
        send_welcome(call.message)
    if call.data == 'add':
        add_new_movie(call.message)
    if call.data.startswith('delete_'):
        chosen_id = int(call.data.split('_')[1])
        database.delete_movie(chosen_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
        markup.add(btn1)
        bot.send_message(call.message.chat.id, 'Фильм удален из библиотеки просмотров', reply_markup=markup)
    if call.data == 'random':
        res, chosen_id = database.get_random_movie()
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
        btn2 = types.InlineKeyboardButton('Другой фильм', callback_data='random')
        btn3 = types.InlineKeyboardButton('Буду смотреть!', callback_data=f'watch_{chosen_id}')
        markup.add(btn1, btn2, btn3)
        bot.send_message(call.message.chat.id, res, reply_markup=markup)
    if call.data.startswith('watch'):
        chosen_id = int(call.data.split('_')[1])
        movie = database.get_movie_id(chosen_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
        btn2 = types.InlineKeyboardButton('Удалить фильм из библиотеки', callback_data=f'delete_{chosen_id}')
        markup.add(btn1, btn2)
        bot.send_message(call.message.chat.id, f"Вы выбрали \"{movie}\". Приятного просмотра!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choose_movie(message):
    chosen_id = int(message.text)
    try:
        movie = database.get_movie_id(chosen_id)
        if movie:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
            btn2 = types.InlineKeyboardButton('Удалить фильм из библиотеки', callback_data=f'delete_{chosen_id}')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, f"Вы выбрали \"{movie}\". Приятного просмотра!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неверный номер. Попробуйте еще раз.')
    except ValueError:
        bot.send_message(message.chat.id, 'Введите верное значение.')


@bot.message_handler(content_types=['text'])
def add_new_movie(message):
    global new_movie
    bot.send_message(message.chat.id, 'Напишите название фильма')
    bot.register_next_step_handler(message, add_movie_name)


def add_movie_name(message):
    global new_movie
    bot.send_message(message.chat.id, 'Напишите тип фильма (сериал, мультфильм, детектив и т.п.)')
    new_movie.append(message.text)
    bot.register_next_step_handler(message, add_movie_type)


def add_movie_type(message):
    global new_movie
    bot.send_message(message.chat.id, 'Напишите краткое описание фильма')
    new_movie.append(message.text.lower())
    bot.register_next_step_handler(message, add_movie_desc)


def add_movie_desc(message):
    global new_movie
    new_movie.append(message.text)
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вернуться в начало', callback_data='back')
    markup.add(btn1)
    database.add_new_movie(new_movie)
    bot.send_message(message.chat.id, 'Спасибо! Фильм добавлен в ваш список просмотров.', reply_markup=markup)
    new_movie.clear()


bot.infinity_polling()

