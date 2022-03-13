from loader import *
from handlers import *

if __name__ == '__main__':
	try:
		bot.polling()
	except BaseException as er:
		print(er)
