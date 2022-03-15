import telebot
import os
from database import *
from Interface.UI import *
from dotenv import load_dotenv
from keyboards.reply import *
from keyboards.remove import *


def load():

	load_dotenv('token.env')
	token = os.getenv('token')

	bot = telebot.TeleBot(token)
	return bot


def load_db():
	with db:
		User.create_table()
		Hotel.create_table()
		Photo.create_table()


ui = UI()
add_reply_keyboard(ui, 3, 'lowprice', 'highprice', 'bestdeal', 'history', 'next', 'Назад в меню', board = 'help')
add_reply_keyboard(ui, 3, '/help', '/find-hotels', board = 'main')
add_reply_keyboard(ui, 3, '/next', 'Назад в меню', board = 'next')
add_remove_keyboard(ui, 'del')
add_reply_keyboard(ui, 2, '/lowprice', '/highprice', '/bestdeal', '/history', board = 'mar')
interface = ui

bot = load()
load_db()


if __name__ == '__main__':
	pass
