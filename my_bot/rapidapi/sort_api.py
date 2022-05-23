import re
from typing import Union, Iterable


def key(x_1: Union[int, str], pattern: str, pattern2: str = '', skip: int = 1) -> Union[int, str]:
    """
    Функция key():

    принимает 4 аргумента:
    -- x_1 = str() or int()
    -- pattern = str(), патерн для замены в строке
    -- pattern2 = str(), патерн которым заменять другой
    -- skip = int(), по умолчанию 1, нужен для sort_db() и пропуска сортировки

    Вовзращает отредактированное число
    """

    if float(skip) == 0:
        return skip

    elif x_1 != 'Error not found':
        res = re.sub(pattern, pattern2, x_1)
        return res

    else:
        return -1


def sort_lp(example: Iterable) -> Iterable:
    """
    Функция sort_lp():

    принимает 1 аргумент:
    -- example = iterable(), массив который нужно отсортировать

    Возвращает отсортированный по возрастанию цены массив.
    """
    temp = [i for i in example if i[3] != 'Error not found']   # такая структура нужна чтобы

    temp = sorted(temp, key = lambda x: int(key(x[3], r'[RUB, ]')))   # пользователю не возвращать
    temp.extend([i for i in example if i[3] == 'Error not found'])     # отели без цены как дешёвые

    return temp


def sort_hp(example: Iterable) -> Iterable:
    """
    Функция sort_hp():

    принимает 1 аргумент:
    -- example = iterable(), массив который нужно отсортировать

    Возвращает отсортированный по убыванию цены массив.
    """

    return sorted(example, key = lambda x: int(key(x[3], r'[RUB, ]')), reverse = True)


def sort_bd(example: Iterable, filt: int, dist: Union[int, float]) -> Iterable:
    """
    Функция sort_bd():

    принимает 3 аргумента:
    -- example = iterable(), массив который нужно отсортировать
    -- filt = int()
    -- dist() = int() or float()

    Возвращает список который подходит требованиям параметров filt и dist.
    """

    obj = filter(
        lambda x:
            int(key(x[3], r'[RUB, ]', skip = filt)) <= filt
            and key(x[3], r'[RUB, ]', skip = filt) != -1
            and float(key(key(x[2], r'[,]', '.'), r'[км ]', skip = int(dist))) <= dist, example
    )
    return [i for i in obj]


def sort(example: Iterable, func: str, filt: int = 0, dist: Union[int, float] = 0) -> Iterable:
    """
    Функция sort:

    принимает 4 аргумента:
    -- example = iterable(), массив который нужно отсортировать
    -- func = str(), название функции сортировки
    -- filt = int(), опциональный параметр для sort_bd()
    -- dist() = int() or float(), опциональный параметр для sort_bd()

    Возвращает отсортированный массив если все условия соблюдены.
    """
    
    try:
        if func == 'lowprice':

            return sort_lp(example)
        elif func == 'highprice':

            return sort_hp(example)
        elif func == 'bestdeal':

            return sort_bd(example, filt, dist)
        else:

            raise SyntaxError
    except SyntaxError as er:
        print(er)


if __name__ == '__main__':
    pass
