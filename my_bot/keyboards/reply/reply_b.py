from telebot import types
from Interface.UI import UI


def add_reply_keyboard(ui: UI, k: int, *args, **kwargs) -> None:

	keyboard = types.ReplyKeyboardMarkup()
	buttons = [types.KeyboardButton(i_btn) for i_btn in args]

	for i in range(0, 9, k):
		keyboard.row(*buttons[i: min(len(buttons), i + k)])

	ui.set_ui(name = kwargs['board'], value = keyboard)
