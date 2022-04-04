from typing import Dict, List, Tuple, Iterable, Union
# from config.load_data import api_key, api_key2
import requests
import json
import re

api_key = 'f68d8d2cf0msh45f08eaee8ee6d7p117ea9jsn7b5b60d5d6f8'
api_key2 = '39b50a7edamsh1bb6fd79c247c85p1d94f7jsn25fe3660cab3'

def get_massive(url: str, querystring: Dict, headers: Dict, pattern: str = ''):
    try:
        response = requests.get(url, headers = headers, params = querystring)
        if response.status_code == requests.codes.ok and re.search(pattern, response.text):
            return json.loads(response.text)
            
        raise ConnectionError
    except ConnectionError as er:
        if headers['x-rapidapi-key'] != api_key2:
            headers['x-rapidapi-key'] = api_key2
            return get_massive(url, querystring, headers, pattern)
        else:
            print('Не удалось выполнить запрос')


def get_photos(id: str) -> List:
    response = get_massive(url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos",
                           querystring = {"id": id},
                           headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com", 'x-rapidapi-key': api_key})

    all_ph = [re.sub(r"{size}", r"z", i['baseUrl']) for i in response.get('hotelImages')]

    if len(all_ph) < 2:
        return all_ph
    return all_ph[:2]


def getter(massive: Dict, args: List[str or int]) -> Union[str, Iterable]:
    if isinstance(massive, dict):

        if len(args) > 1:
            return getter(massive.get(args[0]), args[1:])

        return massive.get(args[0])

    elif isinstance(massive, list):
        return getter(massive[args[0]], args[1:])
    return "Error not found"


def get_hotels(data: Union[List, Tuple, Dict]) -> List:
    return [(getter(i, ['name']), getter(i, ['address', 'streetAddress']), getter(i, ['landmarks', 0, 'distance']),
             getter(i, ['ratePlan', 'price', 'current']), get_photos(getter(i, ['id']))) for i in
            data['data']['body']['searchResults']["results"]]


def get_city(city: str) -> Dict:
    result = get_massive(url= "https://hotels4.p.rapidapi.com/locations/v2/search",
                         querystring = {"query": city, "locale": "ru_RU", "currency": "USD"},
                         headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                  'x-rapidapi-key': api_key},
                         pattern = r'(?<="CITY_GROUP",).+?(?=},)')
    return choose_city(result)


def choose_city(temp: Dict) -> Dict:
    pattern = r"\W|[q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m]"
    sec_pattern = r"\s{2,}"
    city = dict()

    for i_city in temp['suggestions'][0]['entities']:
        name = re.sub(pattern, ' ', i_city['caption'])
        name = re.sub(sec_pattern, ' ', name)
        city[name] = i_city["destinationId"]
    return city


def get_hotel(city_id: str) -> List:
    temp = get_massive(url = "https://hotels4.p.rapidapi.com/properties/list",
                       querystring = {"destinationId": city_id, "pageNumber": "1", "pageSize": "25",
                                      "checkIn": "2020-01-08", "checkOut": "2020-01-15", "adults1": "1",
                                      "sortOrder": "PRICE", "locale": "ru_RU", "currency": "RUB"},
                       headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com", 'x-rapidapi-key': api_key},
                       pattern = r'(?<=,)"results":.+?(?=,"pagination")')

    return get_hotels(temp)


if __name__ == '__main__':   #1376905
    # print(get_hotel('1376905'))
    asd = [('Отель «Ингул»', 'ул. Адмиральская, 34', '3,8 км', '1,853 RUB', ['https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/b97327bd_z.jpg', 'https://exp.cdn-hotels.com/hotels/27000000/26730000/26724300/26724285/45c48d5c_z.jpg']), ('Отель «Палас Украина»', 'Центральный пр-т, 57', '3,9 км', '3,104 RUB', ['https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/481e0d06_z.jpg', 'https://exp.cdn-hotels.com/hotels/28000000/27320000/27317800/27317796/e524e902_z.jpg']), ('Отель Mark Plaza', 'Центральный пр-т, 188', '3,1 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/49000000/48310000/48305000/48304947/21583f16_z.jpg', 'https://exp.cdn-hotels.com/hotels/49000000/48310000/48305000/48304947/56abfcc7_z.jpg']), ('Гостиница «Турист»', 'ул. Карпенко, 46', '5,3 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/22000000/21610000/21603000/21602937/0fb72324_z.jpg', 'https://exp.cdn-hotels.com/hotels/22000000/21610000/21603000/21602937/3c5bfd8a_z.jpg']), ('Отель и хостел «Сергеев»', 'ул. Гонгадзе, 26/3', '4,7 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/50000000/49100000/49097600/49097551/a18ddaab_z.jpg', 'https://exp.cdn-hotels.com/hotels/50000000/49100000/49097600/49097551/93e5cb91_z.jpg']), ('Отель Nikotel', 'Центральный проспект, 120', '3,0 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/58000000/57760000/57752900/57752803/50bd05f4_z.jpg', 'https://exp.cdn-hotels.com/hotels/58000000/57760000/57752900/57752803/e97339ff_z.jpg']), ('Отель «Континент»', 'ул. Адмирала Макарова, 41', '3,6 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/58000000/57760000/57755400/57755374/13a6602c_z.jpg', 'https://exp.cdn-hotels.com/hotels/58000000/57760000/57755400/57755374/4aca73b9_z.jpg']), ('Хостел MK', 'ул. Генерала Карпенко, 27', '5,1 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/25000000/24050000/24049100/24049063/22f6e8eb_z.jpg', 'https://exp.cdn-hotels.com/hotels/25000000/24050000/24049100/24049063/fbf844f9_z.jpg']), ('Отель «Каравелла»', 'ул. Террасная, 13', '5,4 км', 'Error not found', ['https://exp.cdn-hotels.com/hotels/22000000/21630000/21622800/21622781/854e9376_z.jpg', 'https://exp.cdn-hotels.com/hotels/22000000/21630000/21622800/21622781/82109a8a_z.jpg'])]
