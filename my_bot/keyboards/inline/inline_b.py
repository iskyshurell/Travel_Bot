from telebot import types
from typing import Dict


def add_inline_keyboard(iter_k: Dict, func: str) -> types.InlineKeyboardMarkup:
	inline_keyboard = types.InlineKeyboardMarkup()

	for i_key, i_val in iter_k.items():
		inline_keyboard.add(types.InlineKeyboardButton(text = i_key, callback_data = f'{i_val}-{func}'))
	return inline_keyboard
