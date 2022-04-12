#!/usr/bin/env python
# -*- coding: utf-8 -*-
from loader import bot
import handlers

	
if __name__ == '__main__':
	try:        
		bot.load_next_step_handlers()                                           
		bot.infinity_polling()  
	except BaseException as er:
		print('Похоже бот крашнулся :(')
