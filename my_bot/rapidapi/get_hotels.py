from typing import Dict, List, Any
from config.load_data import api_key, api_key2
import requests
import json
import re


def get_massive(url, querystring, headers, pattern):
    try:

        response = requests.get(url, headers = headers, params = querystring, timeout = 10)

        if response.status_code == requests.codes.ok:
            find = re.search(pattern, response.text)
            if find:
                return json.loads(response.text)
        raise ConnectionError

    except ConnectionError as er:
        print(er)


def get_photos(id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": id}

    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': api_key}

    response = requests.request("GET", url, headers = headers, params = querystring, timeout = 10)
    response = json.loads(response.text)
    all_ph = [re.sub(r"{size}", r"z", i['baseUrl']) for i in response.get('hotelImages')]

    if len(all_ph) < 2:
        return all_ph
    return all_ph[:2]


def getter(massive: Dict, args: List[str or int]) -> Any:
    if isinstance(massive, dict):

        if len(args) > 1:
            return getter(massive.get(args[0]), args[1:])

        return massive.get(args[0])

    elif isinstance(massive, list):
        return getter(massive[args[0]], args[1:])
    return "Error not found"


def get_hotels(data):
    return [(getter(i, ['name']), getter(i, ['address', 'streetAddress']), getter(i, ['landmarks', 0, 'distance']),
             getter(i, ['ratePlan', 'price', 'current']), get_photos(getter(i, ['id']))) for i in
            data['data']['body']['searchResults']["results"]]


def get_city(city):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "USD"}
    headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com",
               'x-rapidapi-key': api_key}
    pattern = r'(?<="CITY_GROUP",).+?(?=},)'

    temp = get_massive(url, querystring, headers, pattern)

    return choose_city(temp)


def choose_city(temp):
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
               'x-rapidapi-key': api_key}
    pattern = r'(?<=,)"results":.+?(?=,"pagination")'

    temp = get_massive(url, querystring, headers, pattern)

    return get_hotels(temp)
