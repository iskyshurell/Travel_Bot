from loader import bot, interface


@bot.message_handler(content_types = 'text')
def start_func(message) -> None:  # Обработчик начала работы с ботом
	try:
		if message.text.lower() in ["привет", "/hello-world", "/start"]:
			bot.send_message(message.from_user.id,
			                 f'И тебе привет!\nТы в главном меню - выбери действие чтобы продолжить.',
			                 reply_markup = interface.get_ui('main'))
		else:
			raise ValueError(
				"Введённой команды не существует!\nПроверьте правильность написания и повторите попытку.")
	except ValueError as error:
		bot.send_message(message.from_user.id, error)
		bot.send_message(message.from_user.id, "Выберите дейсвие:", reply_markup = interface.get_ui('main'))
