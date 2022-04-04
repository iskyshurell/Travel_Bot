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
    obj = filter(lambda x: int(key(x[3], r'[RUB, ]', skip = filt)) <= filt and key(x[3], r'[RUB, ]', skip = filt) != -1 and float(key(key(x[2], r'[,]', '.'), r'[км ]', skip = int(dist))) <= dist, example)
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
    except BaseException as er:
        print(er)


if __name__ == '__main__':
    obj = [('Heart of Gold Hostel Berlin', 'Johannisstr. 11', '3,1 км', '2,975 RUB', ['https://exp.cdn-hotels.com/hotels/5000000/4540000/4539000/4538932/00922183_z.jpg', 'https://exp.cdn-hotels.com/hotels/5000000/4540000/4539000/4538932/1858b11a_z.jpg']), ('CLUB Lodges Berlin Mitte - Hostel', 'Caroline-Michaelis-Straße 8', '3,2 км', '3,868 RUB', ['https://exp.cdn-hotels.com/hotels/13000000/12760000/12750600/12750584/2351c338_z.jpg', 'https://exp.cdn-hotels.com/hotels/13000000/12760000/12750600/12750584/d3b07b3d_z.jpg']), ('Metropol Hostel Berlin', 'Mehringdamm 32', '3,4 км', '4,141 RUB', ['https://exp.cdn-hotels.com/hotels/4000000/3920000/3911700/3911650/e1e55fb9_z.jpg', 'https://exp.cdn-hotels.com/hotels/4000000/3920000/3911700/3911650/82422a6c_z.jpg']), ('Sunflower Hostel Berlin', 'Helsingforser Str. 17', '6,5 км', '4,247 RUB', ['https://exp.cdn-hotels.com/hotels/10000000/9020000/9016900/9016892/cd7b2a78_z.jpg', 'https://exp.cdn-hotels.com/hotels/10000000/9020000/9016900/9016892/6b0ecad5_z.jpg']), ('Motel Plus Berlin', 'Silbersteinstraße 30-34', '7,9 км', '4,717 RUB', ['https://exp.cdn-hotels.com/hotels/7000000/6570000/6562900/6562856/07e42403_z.jpg', 'https://exp.cdn-hotels.com/hotels/7000000/6570000/6562900/6562856/b845f80e_z.jpg']), ('Pension Schwalbenweg', 'Schwalbenweg 7', '18 км', '4,719 RUB', ['https://exp.cdn-hotels.com/hotels/11000000/10260000/10250700/10250651/8ff0fd80_z.jpg', 'https://exp.cdn-hotels.com/hotels/11000000/10260000/10250700/10250651/3dd01a65_z.jpg']), ('Generator Berlin Prenzlauer Berg', 'Storkower Strasse 160', '7,4 км', '4,856 RUB', ['https://exp.cdn-hotels.com/hotels/2000000/1120000/1110100/1110031/77b15c8f_z.jpg', 'https://exp.cdn-hotels.com/hotels/2000000/1120000/1110100/1110031/16139da6_z.jpg']), ('Hotel Bellevue am Kurfürstendamm', 'Emser Strasse 19-20', '2,8 км', '4,856 RUB', ['https://exp.cdn-hotels.com/hotels/2000000/1190000/1187300/1187218/80fdddeb_z.jpg', 'https://exp.cdn-hotels.com/hotels/2000000/1190000/1187300/1187218/9e787c1d_z.jpg']), ('Icke Apartments', 'Danckelmannstr. 35', '4,0 км', '4,953 RUB', ['https://exp.cdn-hotels.com/hotels/5000000/4620000/4619000/4618995/687bdfad_z.jpg', 'https://exp.cdn-hotels.com/hotels/5000000/4620000/4619000/4618995/eb008b0a_z.jpg']), ('Hotel Atlantic Berlin', 'Zadekstraße 1a', '11 км', '4,955 RUB', ['https://exp.cdn-hotels.com/hotels/10000000/9310000/9307900/9307808/0ffc64b6_z.jpg', 'https://exp.cdn-hotels.com/hotels/10000000/9310000/9307900/9307808/5a26e467_z.jpg']), ('City Hotel Berlin East', 'Landsberger Allee 203', '8,9 км', '4,965 RUB', ['https://exp.cdn-hotels.com/hotels/3000000/2040000/2038500/2038473/7c877b2c_z.jpg', 'https://exp.cdn-hotels.com/hotels/3000000/2040000/2038500/2038473/721118ee_z.jpg']), ('Leonardo Boutique Hotel Berlin City South', 'Rudower Str. 80-82', '11 км', '4,998 RUB', ['https://exp.cdn-hotels.com/hotels/1000000/80000/70500/70426/200bf22a_z.jpg', 'https://exp.cdn-hotels.com/hotels/1000000/80000/70500/70426/6adf2885_z.jpg']), ('Boutique Hotel Sena', 'Weinmeisterhornweg 42', '12 км', '5,001 RUB', ['https://exp.cdn-hotels.com/hotels/58000000/57780000/57775400/57775361/fc37ba08_z.jpg', 'https://exp.cdn-hotels.com/hotels/58000000/57780000/57775400/57775361/7db374d7_z.jpg']), ('Novum Hotel Aldea Berlin Centrum', 'Bülowstraße 20-22', '1,9 км', '5,053 RUB', ['https://exp.cdn-hotels.com/hotels/1000000/880000/876400/876313/3f51f29d_z.jpg', 'https://exp.cdn-hotels.com/hotels/1000000/880000/876400/876313/b1fd7e85_z.jpg']), ('Easy Lodges', 'Columbiadamm 160', '5,8 км', '5,054 RUB', ['https://exp.cdn-hotels.com/hotels/20000000/19800000/19793500/19793438/1d7847d6_z.jpg', 'https://exp.cdn-hotels.com/hotels/20000000/19800000/19793500/19793438/e7383ea9_z.jpg']), ('Hotel Prens Berlin', 'Kottbusser Damm 102', '5,2 км', '5,110 RUB', ['https://exp.cdn-hotels.com/hotels/5000000/4810000/4805000/4804913/a847df23_z.jpg', 'https://exp.cdn-hotels.com/hotels/5000000/4810000/4805000/4804913/552d126d_z.jpg']), ('Hotel Amadeus Central', 'Hohenzollerndamm 57', '4,7 км', '5,153 RUB', ['https://exp.cdn-hotels.com/hotels/8000000/7520000/7510500/7510476/25cb8ecb_z.jpg', 'https://exp.cdn-hotels.com/hotels/8000000/7520000/7510500/7510476/a19cbe94_z.jpg']), ('Pension Messe am Funkturm', 'Wundtstrasse 72', '4,5 км', '5,153 RUB', ['https://exp.cdn-hotels.com/hotels/2000000/1800000/1798800/1798779/375ad9d8_z.jpg', 'https://exp.cdn-hotels.com/hotels/2000000/1800000/1798800/1798779/2cfaf285_z.jpg']), ('Hotel Pankow', 'Pasewalker Str. 14-15', '9,5 км', '5,190 RUB', ['https://exp.cdn-hotels.com/hotels/2000000/1670000/1665300/1665207/b4d1582a_z.jpg', 'https://exp.cdn-hotels.com/hotels/2000000/1670000/1665300/1665207/30e7c9bc_z.jpg']), ('Hotel Karlshorst', 'Treskowallee 89', '12 км', '5,231 RUB', ['https://exp.cdn-hotels.com/hotels/12000000/11340000/11331600/11331583/62d0a26b_z.jpg', 'https://exp.cdn-hotels.com/hotels/12000000/11340000/11331600/11331583/0d8a4142_z.jpg']), ('Novum Hotel Kronprinz Berlin', 'Kronprinzendamm 1', '4,7 км', '5,257 RUB', ['https://exp.cdn-hotels.com/hotels/1000000/450000/441400/441302/717e5232_z.jpg', 'https://exp.cdn-hotels.com/hotels/1000000/450000/441400/441302/d9572fb8_z.jpg']), ('a&o Berlin Kolumbus', 'Genslerstraße 18', '11 км', '5,341 RUB', ['https://exp.cdn-hotels.com/hotels/1000000/800000/796500/796459/7994f524_z.jpg', 'https://exp.cdn-hotels.com/hotels/1000000/800000/796500/796459/483539c6_z.jpg']), ('Amaya Motel', 'Silbersteinstraße 5-7', '8,0 км', '5,411 RUB', ['https://exp.cdn-hotels.com/hotels/39000000/38400000/38393400/38393361/460ce109_z.jpg', 'https://exp.cdn-hotels.com/hotels/39000000/38400000/38393400/38393361/ca3e94dd_z.jpg']), ('Novum Hotel Gates Berlin Charlottenburg', 'Knesebeckstr. 8-9', '1,9 км', '5,420 RUB', ['https://exp.cdn-hotels.com/hotels/1000000/50000/42300/42249/a3b0e815_z.jpg', 'https://exp.cdn-hotels.com/hotels/1000000/50000/42300/42249/192ce328_z.jpg']), ('Hotel Am Stuttgarter Eck', 'Kaiser-Friedrich-Str. 54a', '3,4 км', '5,470 RUB', ['https://exp.cdn-hotels.com/hotels/3000000/2390000/2384600/2384558/495159ba_z.jpg', 'https://exp.cdn-hotels.com/hotels/3000000/2390000/2384600/2384558/99485742_z.jpg'])]
    print(sort_lp(obj))