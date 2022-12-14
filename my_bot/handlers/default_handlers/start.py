from loader import bot, interface


@bot.message_handler(content_types = 'text')
def start(message) -> None:  # Обработчик начала работы с ботом

	if message.text.lower() in ["привет", "/hello-world", "/start"]:

		bot.send_message(
			chat_id = message.from_user.id,
			text = f'И тебе привет!\nТы в главном меню - выбери действие чтобы продолжить.',
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
