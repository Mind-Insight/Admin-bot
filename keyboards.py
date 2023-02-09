from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import CHANNEL_ID, CHANNEL_URL

channel_btn = InlineKeyboardButton(text='Канал', url=CHANNEL_URL)
kb = InlineKeyboardMarkup(row_width=1)
kb.insert(channel_btn)