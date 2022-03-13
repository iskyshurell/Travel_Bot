import re


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
