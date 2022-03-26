from loader import bot
import handlers


if __name__ == '__main__':
	try:

		bot.polling()                   
	except BaseException as er:
		print(er)
