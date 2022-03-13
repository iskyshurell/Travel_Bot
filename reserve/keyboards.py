from telebot import types


def add_reply_keyboard(ui, k: int, *args, **kwargs):
	keyboard = types.ReplyKeyboardMarkup()
	buttons = [types.KeyboardButton(i_btn) for i_btn in args]
	for i in range(0, 9, k):
		keyboard.row(*buttons[i: min(len(buttons), i + k)])
	ui.set_ui(name = kwargs['board'], value = keyboard)


def add_remove_keyboard(ui, board: str = ''):
	ui.set_ui(name = board, value = types.ReplyKeyboardRemove())


def add_inline_keyboard(iter_k, func):
	inline_keyboard = types.InlineKeyboardMarkup()

	for i_key, i_val in iter_k.items():
		inline_keyboard.add(types.InlineKeyboardButton(text = i_key, callback_data = f'{i_val}-{func}'))
	return inline_keyboard
