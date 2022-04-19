import re
from typing import Union, Iterable


def key(x_1: Union[int, str], pattern: str, pattern2: str = '', skip: int = 1) -> Union[int, str]:

    if float(skip) == 0:
        return skip

    elif x_1 != 'Error not found':
        res = re.sub(pattern, pattern2, x_1)
        return res

    else:
        return -1


def sort_lp(example: Iterable) -> Iterable:

    temp = [i for i in example if i[3] != 'Error not found']

    temp = sorted(temp, key = lambda x: int(key(x[3], r'[RUB, ]')))
    temp.extend([i for i in filter(lambda x: x[3] == "Error not found", example)])

    return temp


def sort_hp(example: Iterable) -> Iterable:

    return sorted(example, key = lambda x: int(key(x[3], r'[RUB, ]')), reverse = True)


def sort_bd(example: Iterable, filt: int, dist: Union[int, float]) -> Iterable:

    obj = filter(
        lambda x:
            int(key(x[3], r'[RUB, ]', skip = filt)) <= filt
            and key(x[3], r'[RUB, ]', skip = filt) != -1
            and float(key(key(x[2], r'[,]', '.'), r'[км ]', skip = int(dist))) <= dist, example
    )
    return [i for i in obj]


def sort(example: Iterable, func: str, filt: int = 0, dist: Union[int, float] = 0) -> Iterable:

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
