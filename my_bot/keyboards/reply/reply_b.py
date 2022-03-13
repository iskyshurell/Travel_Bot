from telebot import types


def add_reply_keyboard(ui, k: int, *args, **kwargs):
	keyboard = types.ReplyKeyboardMarkup()
	buttons = [types.KeyboardButton(i_btn) for i_btn in args]
	for i in range(0, 9, k):
		keyboard.row(*buttons[i: min(len(buttons), i + k)])
	ui.set_ui(name = kwargs['board'], value = keyboard)
