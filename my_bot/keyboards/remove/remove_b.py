from telebot import types


def add_remove_keyboard(ui, board: str = ''):
	ui.set_ui(name = board, value = types.ReplyKeyboardRemove())

