from datetime import datetime
from peewee import *

db = SqliteDatabase('BDB')  # 'Bot Data Base'


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	name = CharField()
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


def user_inf(u_id):
	with db:
		result = User.select().where(User.id == u_id).get()
		return result.name, result.hotels


def db_update(user_id, massive):
	with db:
		try:
			user = User.select().where(User.id == user_id).get()
			hotel = Hotel.create(requester = user, time = datetime.now(), name = massive[0], address = massive[1], dist = massive[2], price = massive[3])
			for i_ph in massive[4]:
				Photo.create(hotel_ph = hotel, photo = i_ph)
		except DoesNotExist:
			print("No User")


def create_user(name, u_id):
	with db:
		User.create(name = name, id = u_id)


if __name__ == '__main__':
	pass
	# with db:
	# 	User.create_table()
	# 	Hotel.create_table()
	# 	Photo.create_table()
	# create_user('isky', 1234)
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
