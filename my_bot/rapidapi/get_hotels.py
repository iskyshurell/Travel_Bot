from typing import Dict, List, Any
import requests
import json
import re


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

    response = requests.request("GET", url, headers = headers, params = querystring, timeout = 10)
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

        response = requests.get(url, headers = headers, params = querystring, timeout = 10)

        if not response.status_code == requests.codes.ok:
            raise ConnectionError

        find = re.search(pattern, response.text)

        if not find:
            raise ConnectionError

        text = json.loads(response.text)

        return text
    except ConnectionError as er:
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
               'x-rapidapi-key': "f68d8d2cf0msh45f08eaee8ee6d7p117ea9jsn7b5b60d5d6f8"}  # '39b50a7edamsh1bb6fd79c247c85p1d94f7jsn25fe3660cab3'
    pattern = r'(?<=,)"results":.+?(?=,"pagination")'

    temp = get_massive(url, querystring, headers, pattern)

    return get_hotels(temp)
