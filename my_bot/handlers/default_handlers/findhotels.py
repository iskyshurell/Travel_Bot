import time
import telebot.types as tp
from typing import Union, List
from loader import bot, interface
import re
from database import *
from rapidapi.get_hotels import get_city, get_hotel
from rapidapi.sort_api import sort
from keyboards import inline
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar
from itranslate import itranslate


@bot.message_handler(commands = ['find-hotels', 'lowprice', 'highprice', 'bestdeal', 'history'])
def func_choose(message: tp.Message, flag: bool = False, func: str = '') -> None:

	if flag:
		result = func

	else:
		result = re.search(r'[^/]+', message.text)
		result = result.group()

	if result != 'find-hotels':

		if result == 'lowprice':

			func = 'lowprice'
		elif result == 'highprice':

			func = 'highprice'
		elif result == 'bestdeal':

			func = 'bestdeal'
		elif result == 'history':

			func = 'history'

		else:

			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Вы ввели неправильную функцию:'
			)
			bot.send_message(
				message.from_user.id,
				'-- Введите новую или вернитесь в меню --',
				reply_markup = interface.get_ui('next')
			)

			bot.register_next_step_handler(message, next_h)

		if func == 'history':

			history(message)
		elif func != '':

			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Введите название города: ',
				reply_markup = interface.get_ui('del')
			)
			bot.register_next_step_handler(message, get_cities, func)

	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введите функцию: ',
			reply_markup = interface.get_ui('mar')
		)
		bot.register_next_step_handler(message, func_choose)


def history(message: tp.Message) -> None:

	with db:

		user = message.from_user
		try:

			if User.select().where(User.id == user.id and User.username == user.username).get():

				for i_h in all_user_info(user.id):

					time.sleep(1)
					bot.send_message(
						chat_id = user.id,
						text = f'Ваш отель:\n- Название отеля:  {i_h[0]}\n- Адресс:  {i_h[1]}'
						f'\n- Расстояние до центра города: {i_h[2]}\n- Цена: {i_h[3]}\n- Полная цена: {i_h[4]} RUB'
					)

					for i_ph in i_h[5]:
						bot.send_message(user.id, i_ph)

				bot.send_message(
					chat_id = user.id,
					text = 'Отлично! Операция прошла успешно.',
					reply_markup = interface.get_ui('next')
				)
				bot.register_next_step_handler(message, next_h)

		except (DoesNotExist, OperationalError):

			bot.send_message(
				chat_id = user.id,
				text = 'Похоже вы ещё не делали запросов(',
				reply_markup = interface.get_ui('next')
			)
			bot.register_next_step_handler(message, next_h)


def get_cities(message: tp.Message, func1: str) -> None:

	result = re.search(r"[ \d]", message.text)

	if not result:

		cities = get_city(message.text)
		markup = inline.inline_b.add_inline_keyboard(cities, func1)

		bot.send_message(
			chat_id = message.from_user.id,
			text = "Отлично!\nНо уточните пожалуйста откуда именно:",
			reply_markup = markup
		)

	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введённый формат города неправильный, повторите попытку:'
		)
		bot.register_next_step_handler(message, get_cities, func1)


@bot.callback_query_handler(func = lambda call: len(call.data.split('-')) == 3)
def dates(message: tp.CallbackQuery) -> None:

	info = str(message.data)
	info = info.split('-')
	city, func, name = info[0], info[1], info[2]

	bot.edit_message_text(
		text = f'Вы выбрали {name}',
		chat_id = message.message.chat.id,
		message_id = message.message.message_id
	)

	with db:

		user = message.message.chat

		User.get_or_create(
			username = user.username,
			first_name = user.first_name,
			surname = user.last_name,
			id = user.id
		)

		request_update(user.id, func = func, city = city)

	call, step = DetailedTelegramCalendar().build()

	bot.send_message(
		chat_id = message.from_user.id,
		text = f'Выберите дату заезда: '
	)
	bot.send_message(
		chat_id = message.from_user.id,
		text = f'Выберите {itranslate(LSTEP[step], to_lang = "ru")}',
		reply_markup = call
	)


@bot.callback_query_handler(func = DetailedTelegramCalendar.func())
def cal(message: tp.CallbackQuery) -> None:

	result, key, step = DetailedTelegramCalendar().process(message.data)

	if not result:

		bot.edit_message_text(
			text = f"Выберите {itranslate(LSTEP[step], to_lang = 'ru')}",
			chat_id = message.message.chat.id,
			message_id = message.message.message_id,
			reply_markup = key
		)
	elif result:

		bot.edit_message_text(
			text = f'Вы выбрали {result}',
			chat_id = message.message.chat.id,
			message_id = message.message.message_id
		)

		with db:

			user = message.message.chat

			req = get_last_req(user.id)

			func = req.func
			city = req.city
	
			if not req.s_date:

				req.s_date = result
				req.save()

				call, step = DetailedTelegramCalendar().build()

				bot.send_message(
					chat_id = message.from_user.id,
					text = f'Выберите дату отьезда: '
				)
				bot.send_message(
					chat_id = message.from_user.id,
					text = f'Выберите {itranslate(LSTEP[step], to_lang = "ru")}',
					reply_markup = call
				)

			else:

				req.f_date = result
				req.save()

				bot.send_message(
					chat_id = message.from_user.id,
					text = "Отлично!\nВведите количество нужных отелей: ",
					reply_markup = interface.get_ui('del')
				)

				if req.func != 'bestdeal':

					bot.register_next_step_handler(message.message, best_deal_check, func, city)
				else:

					bot.register_next_step_handler(message.message, optional_price, func, city)


def optional_price(message: tp.Message, func: str, city: str) -> None:

	result = re.search(r'[ \D]', message.text)

	if not result:

		n = int(message.text)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введите максимальную стоимость остановки в отеле: '
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = '<< Если стоимость не важна, введите 0 >>'
		)

		bot.register_next_step_handler(message, optional_dist, func, city, n)
	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Вы ввели неправильное количество отелей!'
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введите новое:'
		)

		bot.register_next_step_handler(message, optional_price, func, city)


def optional_dist(message: tp.Message, func: str, city: str, n: int):

	result = re.search(r'[ \D]', message.text)
	if not result:

		min_ = int(message.text)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введите максимальную дистанцию отеля до центра города: '
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = '<< Если дистанция не важна, введите 0 >>'
		)

		bot.register_next_step_handler(message, best_deal_check, func, city, int(n), min_, bd_flag = True)
	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Вы ввели неправильную максимальную стоимость!'
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Введите новую стоимость:'
		)

		bot.register_next_step_handler(message, optional_dist, func, city, n)

# def n_photos(
# 		message: tp.Message,
# 		func: str,
# 		city: str,
# 		n: int = 0,
# 		min_: int = 0,
# 		bd_flag: bool = False
# 	):
#
#

def best_deal_check(
		message: tp.Message,
		func: str,
		city: str,
		n: int = 0,
		min_: int = 0,
		bd_flag: bool = False
	):

	if bd_flag:

		result = re.search(r'[,\d]+', message.text)

		if result:

			dist = re.sub(r'[,]', '.', message.text)
			dist = float(dist)

			result_check(message, result, func, city, n, min_, dist)
	else:

		message_check(message, func, city, n, min_)


def message_check(message: tp.Message, func: str, city: str, n: int = 0, min_: int = 0):

	result = re.search(r'[ \D]', message.text)

	if not result:

		result = True

		n = int(n)
		if n == 0:

			n = int(message.text)
		else:

			min_ = int(message.text)

		result_check(message, result, func, city, n, min_)
	else:

		if n == 0:

			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Вы ввели неправильное количество отелей!'
			)
			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Введите новое:'
			)

			bot.register_next_step_handler(message, message_check, func, city)
		else:

			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Вы ввели неправильную максимальную дистанцию отеля до центра города!'
			)
			bot.send_message(
				chat_id = message.from_user.id,
				text = 'Введите новую дистанцию отеля до центра города:'
			)

			bot.register_next_step_handler(message, message_check, func, city, n)


def result_check(
		message: tp.Message,
		result: Union[bool, re.search],
		func: str,
		city: str,
		n: int = 0,
		min_: int = 0,
		dist: float = 0.0
	):

	if result:
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Ожидайте! Вскоре мы сможем показать вам ваши отели.'
		)

		result = get_hotel(city)

		with db:

			request = get_last_req(message.chat.id)
			days = dates_difference(request.s_date, request.f_date)
			days = max(int(days.days), 1)
			
		send_info(message, result, func, n, min_, dist, days)


def send_info(message: tp.Message, result: List, func: str, n: int, min_: int, dist: float, days: int):

	new_hotels = []
	u_hotels = sort(result, func, min_, dist)

	if len(u_hotels) > 0:

		for temp in u_hotels:

			if n == 0:

				break
			n -= 1

			time.sleep(1)

			if temp[3] != 'Error not found':

				total_p = int(re.sub(r"[RUB, ]", "", temp[3])) * days
			else:

				total_p = "Error not found"

			bot.send_message(
				chat_id = message.from_user.id,
				text =
				f'Ваш отель:'
				f'\n- Название отеля:  {temp[0]}'
				f'\n- Адресс:  {temp[1]}'
				f'\n- Расстояние до центра города: {temp[2]}'
				f'\n- Цена: {temp[3]}'
				f'\n- Полная цена за {days} дней: {total_p} RUB',

				reply_markup = interface.get_ui('next')
			)

			for i_ph in temp[-1]:

				bot.send_message(
					chat_id = message.from_user.id,
					text = i_ph)

			new_hotels.append(
				(temp[0], temp[1], temp[2], temp[3], total_p, temp[-1])
			)

		save_info(message, new_hotels[:])
	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Упс, похоже по вашему запросу ничего не нашлось :('
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Попробуйте ещё раз или вернитесь в главное меню:',
			reply_markup = interface.get_ui('next')
		)

		bot.register_next_step_handler(message, next_h)

	
def save_info(message: tp.Message, new_hotels):

	with db:

		user = message.from_user
		User.get_or_create(
			username = user.username,
			first_name = user.first_name,
			surname = user.last_name,
			id = user.id
		)

		r_id = get_last_req(user.id)

		for i_h in new_hotels:

			db_update(r_id, i_h)

	bot.send_message(
		chat_id = user.id,
		text = 'Отлично! Операция прошла успешно.',
		reply_markup = interface.get_ui('next')
	)

	bot.register_next_step_handler(message, next_h)


def next_h(message: tp.Message) -> None:

	if message.text == '/next':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Успешно!\nПродолжаем работу',
			reply_markup = interface.get_ui('del')
		)

		func_choose(message, flag = True, func = 'find-hotels')
	elif message.text == 'Назад в меню':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Заканчиваем работу.'
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Возврат в главное меню прошёл успешно.',
			reply_markup = interface.get_ui('main')
		)
