from typing import Dict, List, Tuple, Iterable, Union
from config.load_data import api_key, api_key2
import requests
import json
import re


def get_massive(url: str, querystring: Dict, headers: Dict, pattern: str = '') -> Dict:
    try:

        response = requests.get(url, headers = headers, params = querystring, timeout = 10)
        print(headers['x-rapidapi-key'])

        if response.status_code == requests.codes.ok:
            print(response.text)
            find = re.search(pattern, response.text)
            print(f'{find} - find')
            if find:
                return json.loads(response.text)

        raise ConnectionError

    except ConnectionError as er:
        if headers['x-rapidapi-key'] != api_key2:
            headers['x-rapidapi-key'] = api_key2
            get_massive(url, querystring, headers, pattern)
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
    temp = get_massive(url= "https://hotels4.p.rapidapi.com/locations/v2/search",
                       querystring = {"query": city, "locale": "ru_RU", "currency": "USD"},
                       headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
                                  'x-rapidapi-key': api_key},
                       pattern = r'(?<="CITY_GROUP",).+?(?=},)')
    return choose_city(temp)


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


if __name__ == '__main__':
    print(get_city('Николаев'))
