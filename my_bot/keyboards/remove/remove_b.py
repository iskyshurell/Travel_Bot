from telebot import types
from Interface.UI import UI


def add_remove_keyboard(ui: UI, board: str = '') -> None:

	ui.set_ui(name = board, value = types.ReplyKeyboardRemove())
