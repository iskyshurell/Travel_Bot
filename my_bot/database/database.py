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
	request_id = IntegerField(primary_key = True)
	time = DateTimeField()
	func = CharField()
	dist = FloatField()
	m_price = IntegerField()
	n_hotels = IntegerField()
	s_date = DateTimeField()
	f_date = DateTimeField()


class Hotel(BaseModel):
	requester = ForeignKeyField(Request, related_name = 'hotels')
	name = CharField()
	address = CharField()
	dist = CharField()
	price = CharField()


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


def request_update(user_id: int, request_id: int, time: datetime = datetime.now(),
				func: str = 'None', dist: float = 0.0, m_price: int = 0, n_hotels: int = 0,
				s_date: datetime = datetime.now(), f_date: datetime = datetime.now()):

	with db:
		user = User.select().where(User.id == user_id).get()
		Request.create(user = user, time = time, request_id = request_id,
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


def all_info(u_id: int) -> Hotel:
	with db:
		user = user_inf(u_id)
		for i in user.requests:
			for i_h in i.hotels:
				yield i_h


def get_last_req(u_id: int):
	with db:
		user = User.select().where(User.id == u_id).get()
		return user.requests[-1]


if __name__ == '__main__':
	with db:
		User.create_table()
		Request.create_table()
		Hotel.create_table()
		Photo.create_table()

		# create_user('gg', 'wp', 'we', 1234)
		# request_update(1234, 2)
		print(get_last_req(1234))
	# 	print(request_info(000, 1234))
	# 	db_update(000, ('Отель «Ингул»', 'ул. Адмиральская, 34', '3,8 км', '1,570 RUB',
	#             ['https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg',
	#              'https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/45c48d5c_z.jpg']))
	# #
	# db_update(1234, ('INgyl', 'dsgesg2', '1.2 km', '1200 RUB', 'gfgr'))

	# u1 = User.create(name = 'Isky', id = 1234)
	#
	# h1 = Hotel.create(requester = u1, name = 'Отель «Ингул»', address = 'ул. Адмиральская, 34', dist = '3,8 км', price = '2340 RUB')
	#
	# p1 = Photo.create(hotel_ph = h1, photo = 'https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg')
	#
	# p2 = Photo.create(hotel_ph = h1, photo = 'https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/45c48d5c_z.jpg')
	# db_update(1234, ('Отель «Ингул»', 'ул. Адмиральская, 34', '3,8 км', '1,570 RUB',
	#             ['https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg',
	#              'https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/45c48d5c_z.jpg']))
	# info = user_inf(1234)
	# for i_h in info[1]:
	# 	print(i_h.name, i_h.time, i_h.address, i_h.price, i_h.dist)
	# 	for i_ph in i_h.photos:
	# 		print(i_ph.photo)
