from my_bot.loader import bot



@bot.message_handler(commands = ['help'])
def help_info(message) -> None:
	bot.send_message(message.from_user.id, "Вот мои возможности:", interface.get_ui('del'))

	bot.send_message(message.from_user.id, 'ps: Выбери метод о котором хочешь узнать информацию',
					reply_markup = interface.get_ui('help'))

	bot.register_next_step_handler(message, reply_func)


def reply_func(message) -> None:

	try:
		if message.text == 'lowprice':
			bot.send_message(message.from_user.id,
			                 'Метод /lowprice: \n\n >>> Выводит самые дешёвые отели в введённом городе')
			bot.register_next_step_handler(message, reply_func)
		elif message.text == 'highprice':
			bot.send_message(message.from_user.id,
			                 'Метод /highprice: \n\n >>> Выводит самые дорогие отели в введённом городе')
			bot.register_next_step_handler(message, reply_func)
		elif message.text == 'bestdeal':
			bot.send_message(message.from_user.id,
			                 'Метод /bestdeal: \n\n >>> Выводит наилучшие отели (по вашим критериям) в введённом городе')
			bot.register_next_step_handler(message, reply_func)
		elif message.text == 'history':
			bot.send_message(message.from_user.id, 'Метод /history: \n\n >>> Выводит историю запросов')
			bot.register_next_step_handler(message, reply_func)
		elif message.text == "next":
			bot.send_message(message.from_user.id,
			                 'Метод /next:\n\n >>> Нужен для продолжения работы с отелями не выходя в главное меню')
			bot.register_next_step_handler(message, reply_func)
		elif message.text == 'Назад в меню':
			bot.send_message(message.from_user.id, 'Возврат в меню произошёл успешно!',
			                 reply_markup = interface.get_ui('main'))
		else:
			raise ValueError(
				"Введённой команды не существует!\nПроверьте правильность написания и повторите попытку.")
	except ValueError as error:
		bot.send_message(message.from_user.id, error)
		bot.send_message(message.from_user.id, "Выберите дейсвие:", reply_markup = interface.get_ui('main'))
