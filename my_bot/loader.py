import telebot
from database import *
from Interface.UI import *
from keyboards.reply import *
from keyboards.remove import *
from config.load_data import token
from googletrans import Translator


def load(token: str) -> telebot.TeleBot:

	bot = telebot.TeleBot(token)
	return bot


def load_db() -> None:
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
load_db()
translator = Translator()


if __name__ == '__main__':
	pass
