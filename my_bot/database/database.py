import re
from datetime import datetime
from peewee import *
from typing import Tuple

db = SqliteDatabase('BDB')  # 'Bot Data Base'


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	username = CharField()
	first_name = CharField()
	surname = CharField()
	id = IntegerField(primary_key = True)


class Request(BaseModel):
	user = ForeignKeyField(User, related_name = 'requests')
	request_id = AutoField(primary_key = True)
	city = IntegerField()
	time = DateTimeField()
	func = CharField()
	dist = FloatField(null = True)
	m_price = IntegerField(null = True)
	n_hotels = IntegerField()
	s_date = DateTimeField(null = True)
	f_date = DateTimeField(null = True)

	def __str__(self):
		return f'{self.s_date}  {self.f_date}'


class Hotel(BaseModel):
	requester = ForeignKeyField(Request, related_name = 'hotels')
	name = CharField()
	address = CharField()
	dist = CharField()
	price = CharField()
	full_price = CharField()


class Photo(BaseModel):
	hotel_ph = ForeignKeyField(Hotel, related_name = 'photos')
	photo = CharField()


def user_inf(u_id: int) -> User:
	with db:
		result = User.select().where(User.id == u_id).get()
		return result


def request_info(request_id: int, u_id: int) -> Request:
	with db:
		request = Request.select().where(request_id == Request.request_id and u_id == Request.user).get()
		return request


def request_update(user_id: int, time: datetime = datetime.now(), city: int = 0,
					func: str = 'None', dist: float = None, m_price: int = None, n_hotels: int = 0,
					s_date: datetime = None, f_date: datetime = None):

	with db:
		user = User.select().where(User.id == user_id).get()
		Request.create(user = user, time = time, city = city,
						func = func, dist = dist, m_price = m_price, n_hotels = n_hotels,
						s_date = s_date, f_date = f_date)


def db_update(req_id: int, massive: Tuple) -> None:
	with db:

		try:
			request = Request.select().where(Request.request_id == req_id).get()
			hotel = Hotel.create(requester = request, time = datetime.now(), name = f'{massive[0]}', address = f'{massive[1]}', dist = f'{massive[2]}', price = f'{massive[3]}')
			for i_ph in massive[4]:
				Photo.create(hotel_ph = hotel, photo = i_ph)
		except DoesNotExist:
			print("No User")


def create_user(name: str, fname: str, sname: str, u_id: int) -> None:
	with db:
		User.create(username = name, first_name = fname, surname = sname, id = u_id)


def get_last_req(u_id: int):
	with db:
		user = User.select().where(User.id == u_id).get()
		return user.requests[-1]


def dates_difference(f_d: str, s_d: str):
	f_d, s_d = re.search(r'\S+', f_d).group(), re.search(r'\S+', s_d).group()
	f_d, s_d = datetime.strptime(f_d, '%Y-%m-%d'), datetime.strptime(s_d, '%Y-%m-%d')
	return max(f_d - s_d, s_d - f_d)


if __name__ == '__main__':
	with db:
		User.create_table()
		Request.create_table()
		Hotel.create_table()
		Photo.create_table()
		for i in User.select(): 
			for i_r in i.requests:

				obj = i_r.__str__().split('  ')


				if obj[0] != 'None':
					obj = [i.split(' ')[0] for i in obj]
					f_date = datetime.strptime(obj[-1], '%Y-%m-%d')
					s_date = datetime.strptime(obj[-2], '%Y-%m-%d')
					days = f_date - s_date
					print(type(days))