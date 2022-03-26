from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


pillskb = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="🔴", callback_data='red')).row(InlineKeyboardButton(text="🔵", callback_data='blue'))
