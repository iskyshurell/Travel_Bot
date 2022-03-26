import re

from telebot import types
from typing import Dict


def add_inline_keyboard(iter_k: Dict, func: str) -> types.InlineKeyboardMarkup:
	inline_keyboard = types.InlineKeyboardMarkup()

	for i_key, i_val in iter_k.items():
		short_name = re.search(r'\w+', i_key).group()

		inline_keyboard.add(types.InlineKeyboardButton(text = i_key, callback_data = f'{i_val}-{func}-{short_name}'))
	return inline_keyboard
