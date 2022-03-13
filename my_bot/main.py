import handlers
from loader import *

if __name__ == '__main__':
	try:
		print(bot)
		bot.polling()
	except BaseException as er:
		print(er)
