#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loader import bot
import handlers

	
if __name__ == '__main__':
	try:        

		bot.polling()                   
	except BaseException as er:
		print('Похоже бот крашнулся :(')
