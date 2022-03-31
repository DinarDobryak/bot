from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


requsetbutton = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отправить номер телефона', request_contact=True))

endsbutton = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/О компании')).row(KeyboardButton('/Наш сайт'))