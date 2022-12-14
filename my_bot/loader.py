import telebot
from database import *
from Interface.UI import *
from keyboards.reply import *
from keyboards.remove import *
from config.load_data import token


def load(b_token: str) -> telebot.TeleBot:
	"""
	Функция load:

	принимает 1 аргумент:
	-- b_token = str(), токен для бота

	Возвращает самого бота для подальшей работы с ним.
	"""

	tele_bot = telebot.TeleBot(b_token)
	return tele_bot


def load_db() -> None:
	"""
	>> Подгружает базу данных db <<
	"""
	with db:
		User.create_table()
		Hotel.create_table()
		Photo.create_table()
		Request.create_table()


ui = UI()
add_reply_keyboard(ui, 3, 'lowprice', 'highprice', 'bestdeal', 'history', 'next', 'Назад в меню', board = 'help')
add_reply_keyboard(ui, 3, '/help', '/find-hotels', board = 'main')
add_reply_keyboard(ui, 3, '/next', 'Назад в меню', board = 'next')
add_remove_keyboard(ui, 'del')
add_reply_keyboard(ui, 2, '/lowprice', '/highprice', '/bestdeal', '/history', board = 'mar')
interface = ui

bot = load(token)
bot.enable_save_next_step_handlers(delay=2)
load_db()


if __name__ == '__main__':
	pass
