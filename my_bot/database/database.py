from datetime import datetime
from peewee import *
from typing import List

db = SqliteDatabase('BDB')  # 'Bot Data Base'


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	username = CharField()
	first_name = CharField()
	surname = CharField()
	id = IntegerField()


class Hotel(BaseModel):
	requester = ForeignKeyField(User, related_name = 'hotels')
	time = DateTimeField()
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


def db_update(user_id: int, massive: List) -> None:
	with db:

		try:
			user = User.select().where(User.id == user_id).get()
			hotel = Hotel.create(requester = user, time = datetime.now(), name = f'{massive[0]}', address = f'{massive[1]}', dist = f'{massive[2]}', price = f'{massive[3]}')
			for i_ph in massive[4]:
				Photo.create(hotel_ph = hotel, photo = i_ph)
		except DoesNotExist:
			print("No User")


def create_user(name: str, fname: str, sname: str, u_id: int) -> None:
	with db:
		User.create(username = name, first_name = fname, surname = sname, id = u_id)


if __name__ == '__main__':
	with db:
		User.create_table()
		Hotel.create_table()
		Photo.create_table()
		create_user('isky', 'GG', 'GGh', 1234)
		print(User.select().where(User.id == 1234).get().surname)
	#
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
