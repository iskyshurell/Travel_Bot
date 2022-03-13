import telebot
import os
from database import *
from UI import UI
from dotenv import load_dotenv
from keyboards.keyboards import *


class TeleBot:
	def __init__(self, bot) -> None:
		self.__bot = bot

	def get_bot(self):
		return self.__bot


def load():

	load_dotenv('token.env')
	token = os.getenv('token')

	bot = telebot.TeleBot(token)
	return TeleBot(bot)


def ui_set():
	ui = UI()
	add_reply_keyboard(ui, 3, 'lowprice', 'highprice', 'bestdeal', 'history', 'next', 'Назад в меню', board = 'help')
	add_reply_keyboard(ui, 3, '/help', '/find-hotels', board = 'main')
	add_reply_keyboard(ui, 3, '/next', 'Назад в меню', board = 'next')
	add_remove_keyboard(ui, 'del')
	add_reply_keyboard(ui, 2, '/lowprice', '/highprice', '/bestdeal', '/history', board = 'mar')

	return ui


def load_db():
	User.create_table()
	Hotel.create_table()
	Photo.create_table()


bot_cls = load()
bot = bot_cls.get_bot()
interface = ui_set()
load_db()


if __name__ == '__main__':
	pass
