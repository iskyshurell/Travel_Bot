from my_bot.loader import *
import re
from my_bot.rapidapi.get_hotels import get_city, get_hotel
from my_bot.rapidapi.sort_api import sort
from my_bot.keyboards import inline


@bot.message_handler(commands = ['find-hotels', 'lowprice', 'highprice', 'bestdeal', 'history'])
def func_choose(message, flag: bool = False, func: str = '') -> None:
	try:
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
				raise ValueError

			bot.send_message(message.from_user.id, 'Введите название города: ',
			                 reply_markup = interface.get_ui('del'))
			bot.register_next_step_handler(message, get_cities, func)

		else:
			bot.send_message(message.from_user.id, 'Введите функцию: ', reply_markup = interface.get_ui('mar'))
			bot.register_next_step_handler(message, func_choose)

	except ValueError as er:
		print(er)
		bot.send_message(message.from_user.id, 'Вы ввели неправильную функцию:')
		bot.send_message(message.from_user.id, '-- Введите новую или вернитесь в меню --',
		                 reply_markup = interface.get_ui('next'))
		bot.register_next_step_handler(message, next_h)


def get_cities(message, func1: str) -> None:

	result = re.search(r"[ \d]", message.text)
	if not result:
		cities = get_city(message.text)
		markup = inline.inline_b.add_inline_keyboard(cities, func1)
		bot.send_message(message.from_user.id, "Отлично!\nНо уточните пожалуйста откуда именно:",
		                 reply_markup = markup)

	else:
		bot.send_message(message.from_user.id, 'Введённый формат города неправильный, повторите попытку:')
		bot.register_next_step_handler(message, get_cities, func1)


@bot.callback_query_handler(func = lambda call: re.search(r'\d+', call.data))
def n_input(message) -> None:
	bot.delete_message(chat_id = message.from_user.id, message_id = message.message.message_id)
	bot.send_message(message.from_user.id, "Отлично!\nВведите количество нужных отелей: ",
	                 reply_markup = interface.get_ui('del'))

	info = str(message.data)
	info = info.split('-')
	city, func = info[0], info[1]

	if func != 'bestdeal':
		bot.register_next_step_handler(message.message, final_result, func, city)
	else:
		bot.register_next_step_handler(message.message, optional_func, func, city)


def optional_func(message, func1: str, city: str):
	result = re.search(r'[ \D]', message.text)
	if not result:
		n = int(message.text)
		bot.send_message(message.from_user.id, 'Введите максимальную стоимость остановки в отеле: ')
		bot.send_message(message.from_user.id, '<< Если стоимость не важна, введите 0 >>')
		bot.register_next_step_handler(message, optional_dist, func1, city, n)
	else:
		bot.send_message(message.from_user.id, 'Вы ввели неправильное количество отелей!')
		bot.send_message(message.from_user.id, 'Введите новое:')
		bot.register_next_step_handler(message, optional_func, func1, city)


def optional_dist(message, func1, city, n):
	result = re.search(r'[ \D]', message.text)
	if not result:
		min_ = int(message.text)
		bot.send_message(message.from_user.id, 'Введите максимальную дистанцию отеля до центра города: ')
		bot.send_message(message.from_user.id, '<< Если дистанция не важна, введите 0 >>')
		bot.register_next_step_handler(message, final_result, func1, city, int(n), min_, b_flag = True)
	else:
		bot.send_message(message.from_user.id, 'Вы ввели неправильную максимальную стоимость!')
		bot.send_message(message.from_user.id, 'Введите новую стоимость:')
		bot.register_next_step_handler(message, optional_dist, func1, city, n)


def final_result(message, func1: str, city: str, n: int = 0, min_: int = 0, dist: float = 0.0,
                 b_flag: bool = False) -> None:
	try:
		if b_flag:
			result = re.search(r'[,\d]+', message.text)
			if result:
				dist = re.sub(r'[,]', '.', message.text)
				dist = float(dist)
		else:
			result = re.search(r'[ \D]', message.text)
			if not result:
				result = True

				n = int(n)
				if n == 0:
					n = int(message.text)
				else:
					min_ = int(message.text)

		if result:
			result = get_hotel(city)
			hotels = sort(result, func1, min_, dist)

			for i in range(min(n, len(hotels))):
				temp = hotels[i]
				bot.send_message(message.from_user.id,
				                 f'Ваш отель:\n- Название отеля:  {temp[0]}\n- Адресс:  {temp[1]}\n- Расстояние до центра города:  {temp[2]}\n- Цена:  {temp[3]}',
				                 reply_markup = interface.get_ui('next'))
				for i_ph in temp[-1]:
					bot.send_message(message.from_user.id, i_ph)

			bot.register_next_step_handler(message, next_h)

	except TypeError as er:
		print(er)


def next_h(message) -> None:

	if message.text == '/next':
		bot.send_message(message.from_user.id, 'Успешно!\nПродолжаем работу',
		                 reply_markup = interface.get_ui('del'))
		func_choose(message, flag = True, func = 'find-hotels')
	elif message.text == 'Назад в меню':
		bot.send_message(message.from_user.id, 'Заканчиваем работу.')
		bot.send_message(message.from_user.id, 'Возврат в главное меню прошёл успешно.',
		                 reply_markup = interface.get_ui('main'))
