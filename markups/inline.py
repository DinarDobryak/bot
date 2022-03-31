from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#pillskb = InlineKeyboardMarkup(row_width=2).row(InlineKeyboardButton(text="🔴", callback_data='red')).row(InlineKeyboardButton(text="🔵", callback_data='blue'))

redbut = InlineKeyboardButton(text="🔴", callback_data='red')
bluebut = InlineKeyboardButton(text="🔵", callback_data='blue')
pillskb = InlineKeyboardMarkup(row_width=2).row(redbut, bluebut)


company = InlineKeyboardButton(text = "О Компании", callback_data='О компании')
Url = InlineKeyboardButton(text = "Наш сайт", url='http://style-models.ru' )
lastbut = InlineKeyboardMarkup(row_width=2).row(company, Url).row(redbut,bluebut)