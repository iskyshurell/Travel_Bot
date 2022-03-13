import handlers
from loader import bot

if __name__ == '__main__':
	try:

		bot.polling()
	except BaseException as er:
		print(er)
