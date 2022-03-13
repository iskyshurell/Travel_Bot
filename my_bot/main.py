import handlers
from my_bot.loader import bot

if __name__ == '__main__':
	try:

		bot.polling()
	except BaseException as er:
		print(er)
