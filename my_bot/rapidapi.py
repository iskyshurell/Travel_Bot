import requests
import json
import re
from typing import Any, Dict, List


def getter(massive: Dict, args: List[str or int]) -> Any:
    if isinstance(massive, dict):

        if len(args) > 1:
            return getter(massive.get(args[0]), args[1:])

        return massive.get(args[0])

    elif isinstance(massive, list):
        return getter(massive[args[0]], args[1:])
    return "Error not found"


def get_photos(id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": id}

    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': "f68d8d2cf0msh45f08eaee8ee6d7p117ea9jsn7b5b60d5d6f8"}

    response = requests.request("GET", url, headers = headers, params = querystring)
    response = json.loads(response.text)
    all_ph = [re.sub(r"{size}", r"z", i['baseUrl']) for i in response.get('hotelImages')]

    if len(all_ph) < 2:
        return all_ph
    return all_ph[:2]


def get_hotels(data):
    return [(getter(i, ['name']), getter(i, ['address', 'streetAddress']), getter(i, ['landmarks', 0, 'distance']),
             getter(i, ['ratePlan', 'price', 'current']), get_photos(getter(i, ['id']))) for i in
            data['data']['body']['searchResults']["results"]]


def get_massive(url, querystring, headers, pattern):
    try:

        response = requests.get(url, headers=headers, params=querystring, timeout = 10)

        if response.status_code == requests.codes.ok:
            pass
        else:
            raise BaseException

        find = re.search(pattern, response.text)

        if find:
            pass
        else:
            raise BaseException
        text = json.loads(response.text)

        return text
    except Exception as er:
        print(er)


def get_city(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': "f68d8d2cf0msh45f08eaee8ee6d7p117ea9jsn7b5b60d5d6f8"}
    pattern = r'(?<="CITY_GROUP",).+?(?=},)'

    temp = get_massive(url, querystring, headers, pattern)

    pattern = r"\W|[q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m]"
    sec_pattern = r"\s{2,}"
    city = dict()

    for i_city in temp['suggestions'][0]['entities']:
        name = re.sub(pattern, ' ', i_city['caption'])
        name = re.sub(sec_pattern, ' ', name)
        city[name] = i_city["destinationId"]
    return city


def get_hotel(city_id):
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25", "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15", "adults1": "1", "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': "f68d8d2cf0msh45f08eaee8ee6d7p117ea9jsn7b5b60d5d6f8"}  #39b50a7edamsh1bb6fd79c247c85p1d94f7jsn25fe3660cab3
    pattern = r'(?<=,)"results":.+?(?=,"pagination")'

    temp = get_massive(url, querystring, headers, pattern)

    return get_hotels(temp)


def key(x_1, pattern, pattern2 = '', skip = 1):
    if float(skip) == 0:
        return skip
    elif x_1 != 'Error not found':

        res = re.sub(pattern, pattern2, x_1)
        return res
    else:
        return -1


def sort(example, func: str, filt: int = 0, dist: float = 0):
    try:
        if func == 'lowprice':
            temp = [i for i in example if i[3] != 'Error not found']
            temp = sorted(temp, key = lambda x: int(key(x[3], r'[RUB, ]')))
            temp.extend([i for i in filter(lambda x: x[3] == "Error not found", example)])

            return temp
        elif func == 'highprice':

            return sorted(example, key = lambda x: int(key(x[3], r'[RUB, ]')), reverse = True)
        elif func == 'bestdeal':
            obj = filter(lambda x: int(key(x[3], r'[RUB, ]', skip = filt)) <= filt and key(x[3], r'[RUB, ]', skip = filt) != -1 and float(key(key(x[2], r'[,]', '.'), r'[км ]', skip = int(dist))) <= dist, example)
            return [i for i in obj]
        else:
            raise SyntaxError
    except BaseException as er:
        print(er)

        
if __name__ == '__main__':
    example = [('Отель «Ингул»', 'ул. Адмиральская, 34', '3,8 км', '1,570 RUB',
                ['https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg',
                 'https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/45c48d5c_z.jpg']), (
               'Отель «Палас Украина»', 'Центральный пр-т, 57', '3,9 км', '2,921 RUB',
               ['https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg',
                'https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/e524e902_z.jpg']), (
               'Апартаменты с одной спальней в Николаеве с чудесным видом на город и Wi-FI — рядом с пляжем', None,
               '3,2 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/47000000/46020000/46011300/46011263/c53362b3_z.jpg',
                'https://exp.cdn-hotels.com/hotels/47000000/46020000/46011300/46011263/67bd79c8_z.jpg']), (
               'Отель Mark Plaza', 'Центральный пр-т, 188', '3,1 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/49000000/48310000/48305000/48304947/21583f16_z.jpg',
                'https://exp.cdn-hotels.com/hotels/49000000/48310000/48305000/48304947/56abfcc7_z.jpg']), (
               'Гостиница «Турист»', 'ул. Карпенко, 46', '5,3 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/22000000/21610000/21603000/21602937/0fb72324_z.jpg',
                'https://exp.cdn-hotels.com/hotels/22000000/21610000/21603000/21602937/3c5bfd8a_z.jpg']), (
               'Отель и хостел «Сергеев»', 'ул. Гонгадзе, 26/3', '4,7 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/50000000/49100000/49097600/49097551/a18ddaab_z.jpg',
                'https://exp.cdn-hotels.com/hotels/50000000/49100000/49097600/49097551/93e5cb91_z.jpg']), (
               'Отель Nikotel', 'Центральный проспект, 120', '3,0 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/58000000/57760000/57752900/57752803/50bd05f4_z.jpg',
                'https://exp.cdn-hotels.com/hotels/58000000/57760000/57752900/57752803/e97339ff_z.jpg']), (
               'Отель «Континент»', 'ул. Адмирала Макарова, 41', '3,6 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/58000000/57760000/57755400/57755374/13a6602c_z.jpg',
                'https://exp.cdn-hotels.com/hotels/58000000/57760000/57755400/57755374/4aca73b9_z.jpg']), (
               'Хостел MK', 'ул. Генерала Карпенко, 27', '5,1 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/25000000/24050000/24049100/24049063/22f6e8eb_z.jpg',
                'https://exp.cdn-hotels.com/hotels/25000000/24050000/24049100/24049063/fbf844f9_z.jpg']), (
               'Отель «Каравелла»', 'ул. Террасная, 13', '5,4 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/22000000/21630000/21622800/21622781/854e9376_z.jpg',
                'https://exp.cdn-hotels.com/hotels/22000000/21630000/21622800/21622781/82109a8a_z.jpg']), (
               'Гостиница и хостел «Металлург»', 'Богоявленский пр-т, 319а', '9,3 км', 'Error not found',
               ['https://exp.cdn-hotels.com/hotels/13000000/12330000/12321000/12320970/92fd5e86_z.jpg',
                'https://exp.cdn-hotels.com/hotels/13000000/12330000/12321000/12320970/40258323_z.jpg'])]
    print(sort(example, func = 'lowprice'))
    print(sort(example, func = 'highprice'))
    # print(sort(example, 'bestdeal', filt = 40000, dist = 4))
