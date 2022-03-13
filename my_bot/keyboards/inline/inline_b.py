from telebot import types


def add_inline_keyboard(iter_k, func):
	inline_keyboard = types.InlineKeyboardMarkup()

	for i_key, i_val in iter_k.items():
		inline_keyboard.add(types.InlineKeyboardButton(text = i_key, callback_data = f'{i_val}-{func}'))
	return inline_keyboard
