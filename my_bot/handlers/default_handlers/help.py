from loader import bot, interface


@bot.message_handler(commands = ['help'])
def help_info(message) -> None:

	bot.send_message(
		chat_id = message.from_user.id,
		text = "Вот мои возможности:",
		reply_markup = interface.get_ui('del')
	)

	bot.send_message(
		chat_id = message.from_user.id,
		text = 'ps: Выбери метод о котором хочешь узнать информацию',
		reply_markup = interface.get_ui('help')
	)

	bot.register_next_step_handler(message, reply)


def reply(message) -> None:

	if message.text == 'lowprice':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Метод /lowprice: \n\n >>> Выводит самые дешёвые отели в введённом городе'
		)
		bot.register_next_step_handler(message, reply)

	elif message.text == 'highprice':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Метод /highprice: \n\n >>> Выводит самые дорогие отели в введённом городе'
		)
		bot.register_next_step_handler(message, reply)

	elif message.text == 'bestdeal':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Метод /bestdeal: \n\n >>> Выводит наилучшие отели (по вашим критериям) в введённом городе'
		)
		bot.register_next_step_handler(message, reply)

	elif message.text == 'history':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Метод /history: \n\n >>> Выводит историю запросов'
		)
		bot.register_next_step_handler(message, reply)

	elif message.text == "next":

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Метод /next:\n\n >>> Нужен для продолжения работы с отелями не выходя в главное меню'
		)
		bot.register_next_step_handler(message, reply)

	elif message.text == 'Назад в меню':

		bot.send_message(
			chat_id = message.from_user.id,
			text = 'Возврат в меню произошёл успешно!',
			reply_markup = interface.get_ui('main')
		)

	else:

		bot.send_message(
			chat_id = message.from_user.id,
			text = "Введённой команды не существует!\nПроверьте правильность написания и повторите попытку."
		)
		bot.send_message(
			chat_id = message.from_user.id,
			text = "Выберите дейсвие:",
			reply_markup = interface.get_ui('main')
		)
