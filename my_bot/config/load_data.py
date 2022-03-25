from dotenv import load_dotenv, find_dotenv
from os import getenv

if not find_dotenv('token.env'):
	exit('Переменные окружения не загружены т.к отсутствует файл .env')

else:
	load_dotenv('token.env')

token = getenv('token')
api_key = getenv('rapidapi_key')
api_key2 = getenv('rapidapi_key2')

