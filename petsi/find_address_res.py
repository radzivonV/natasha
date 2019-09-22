from yargy import (
    Parser, or_
)

from yargy import interpretation
from yargy.interpretation import fact, attribute

import sys
sys.path.append('/home/bun/natasha')

from natasha_expanded.grammars import address

import requests
from functools import lru_cache

YNDX_GEO_KEY = '29d541ba-6887-4e71-be53-b00d7e178147'

@lru_cache(maxsize=2**11)
def get_coordinates(geocode):
    r = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={YNDX_GEO_KEY}&geocode={geocode}&format=json&results=1')
    featureMember = r.json()['response']['GeoObjectCollection']['featureMember']
    if featureMember:
        r = featureMember[0]['GeoObject']['Point']['pos']
        long, lat = [float(i) for i in r.split(' ')]
        return long, lat
    else:
        return None, None

Address = fact(
    'Address',
    [attribute('parts').repeatable()]
)

FIND_ADDRESS = or_(
    address.METRO.interpretation(
        Address.parts
    ),
    address.STREET_LEVEL_CUSTOM.interpretation(
        Address.parts
    ),
    address.GOROD_LEVEL.interpretation(
        Address.parts
    ),
    address.RAION.interpretation(
        Address.parts
    ),
    address.OTHER_OBJECTS.interpretation(
        Address.parts
    )
).interpretation(Address)
    
def find_address(text):
        pars = Parser(FIND_ADDRESS)
        matc = pars.findall(text)
        facts = [_.span for _ in matc]
        return get_coordinates(' '.join([text[f[0]:f[1]] for f in facts]))
    
text = """5.12.17 №32214 кобель, Взрослый Черный с белым,хвост пушистый,
не купированный, больше темного окраса,или просто грязный. 
в районе Можайское шоссе, бегает собака(мальчик),грязный,похож 
на русского спаниеля. Заметили его дней 5-6 тому назад,близко не подходит,
кажется с коричневым ошейником,упитанный.может кто ищет 
Найден(а) в районе Москва ул.Толбухина, ул Говорово 89163894451 
Ирина mussirina@mail.ru"""

print(find_address(text))