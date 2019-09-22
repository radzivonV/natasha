# coding: utf-8
from __future__ import unicode_literals

from yargy import (
    rule,
    or_, and_
)
from yargy.interpretation import fact, attribute
from yargy.predicates import (
    eq, lte, gte, gram, type, tag,
    length_eq,
    in_, in_caseless, dictionary,
    normalized, caseless,
    is_title
)
from yargy.pipelines import morph_pipeline
from yargy.tokenizer import QUOTES


Address = fact(
    'Address',
    [attribute('parts').repeatable()]
)
Index = fact(
    'Index',
    ['value']
)
Country = fact(
    'Country',
    ['name']
)
Region = fact(
    'Region',
    ['name', 'type']
)
Settlement = fact(
    'Settlement',
    ['name', 'type']
)
Street = fact(
    'Street',
    ['name', 'type']
)
Building = fact(
    'Building',
    ['number', 'type']
)
Room = fact(
    'Room',
    ['number', 'type']
)
Metro = fact(
    'Metro',
    ['type', 'name']
)


DASH = eq('-')
DOT = eq('.')

ADJF = gram('ADJF')
NOUN = gram('NOUN')
#INT = type('INT')
INT = and_(
    gte(1),
    lte(500)
)
TITLE = is_title()

ANUM = rule(
    INT,
    DASH.optional(),
    in_caseless({
        'я', 'й', 'е',
        'ое', 'ая', 'ий', 'ой'
    })
)


#########
#
#  STRANA
#
##########


# TODO
COUNTRY_VALUE = dictionary({
    'россия',
    'украина'
})

ABBR_COUNTRY_VALUE = in_caseless({
    'рф'
})

COUNTRY = or_(
    COUNTRY_VALUE,
    ABBR_COUNTRY_VALUE
).interpretation(
    Country.name
).interpretation(
    Country
)


#############
#
#  FED OKRUGA
#
############


FED_OKRUG_NAME = or_(
    rule(
        dictionary({
            'дальневосточный',
            'приволжский',
            'сибирский',
            'уральский',
            'центральный',
            'южный',
        })
    ),
    rule(
        caseless('северо'),
        DASH.optional(),
        dictionary({
            'западный',
            'кавказский'
        })
    )
).interpretation(
    Region.name
)

FED_OKRUG_WORDS = or_(
    rule(
        normalized('федеральный'),
        normalized('округ')
    ),
    rule(caseless('фо'))
).interpretation(
    Region.type.const('федеральный округ')
)

FED_OKRUG = rule(
    FED_OKRUG_WORDS,
    FED_OKRUG_NAME
).interpretation(
    Region
)


#########
#
#   RESPUBLIKA
#
############


RESPUBLIKA_WORDS = or_(
    rule(caseless('респ'), DOT.optional()),
    rule(normalized('республика'))
).interpretation(
    Region.type.const('республика')
)

RESPUBLIKA_ADJF = or_(
    rule(
        dictionary({
            'удмуртский',
            'чеченский',
            'чувашский',
        })
    ),
    rule(
        caseless('карачаево'),
        DASH.optional(),
        normalized('черкесский')
    ),
    rule(
        caseless('кабардино'),
        DASH.optional(),
        normalized('балкарский')
    )
).interpretation(
    Region.name
)

RESPUBLIKA_NAME = or_(
    rule(
        dictionary({
            'адыгея',
            'алтай',
            'башкортостан',
            'бурятия',
            'дагестан',
            'ингушетия',
            'калмыкия',
            'карелия',
            'коми',
            'крым',
            'мордовия',
            'татарстан',
            'тыва',
            'удмуртия',
            'хакасия',
            'саха',
            'якутия',
        })
    ),
    rule(caseless('марий'), caseless('эл')),
    rule(
        normalized('северный'), normalized('осетия'),
        rule('-', normalized('алания')).optional()
    )
).interpretation(
    Region.name
)

RESPUBLIKA_ABBR = in_caseless({
    'кбр',
    'кчр',
    'рт',  # Татарстан
}).interpretation(
    Region.name  # TODO type
)

RESPUBLIKA = or_(
    rule(RESPUBLIKA_ADJF, RESPUBLIKA_WORDS),
    rule(RESPUBLIKA_WORDS, RESPUBLIKA_NAME),
    rule(RESPUBLIKA_ABBR)
).interpretation(
    Region
)


##########
#
#   KRAI
#
########


KRAI_WORDS = normalized('край').interpretation(
    Region.type.const('край')
)

KRAI_NAME = dictionary({
    'алтайский',
    'забайкальский',
    'камчатский',
    'краснодарский',
    'красноярский',
    'пермский',
    'приморский',
    'ставропольский',
    'хабаровский',
}).interpretation(
    Region.name
)

KRAI = rule(
    KRAI_NAME, KRAI_WORDS
).interpretation(
    Region
)


############
#
#    OBLAST
#
############


OBLAST_WORDS = or_(
    rule(normalized('область')),
    rule(
        caseless('обл'),
        DOT.optional()
    )
).interpretation(
    Region.type.const('область')
)

OBLAST_NAME = dictionary({
    'амурский',
    'архангельский',
    'астраханский',
    'белгородский',
    'брянский',
    'владимирский',
    'волгоградский',
    'вологодский',
    'воронежский',
    'горьковский',
    'ивановский',
    'ивановский',
    'иркутский',
    'калининградский',
    'калужский',
    'камчатский',
    'кемеровский',
    'кировский',
    'костромской',
    'курганский',
    'курский',
    'ленинградский',
    'липецкий',
    'магаданский',
    'московский',
    'мурманский',
    'нижегородский',
    'новгородский',
    'новосибирский',
    'омский',
    'оренбургский',
    'орловский',
    'пензенский',
    'пермский',
    'псковский',
    'ростовский',
    'рязанский',
    'самарский',
    'саратовский',
    'сахалинский',
    'свердловский',
    'смоленский',
    'тамбовский',
    'тверской',
    'томский',
    'тульский',
    'тюменский',
    'ульяновский',
    'челябинский',
    'читинский',
    'ярославский',
}).interpretation(
    Region.name
)

OBLAST = rule(
    OBLAST_NAME,
    OBLAST_WORDS
).interpretation(
    Region
)


##########
#
#    AUTO OKRUG
#
#############


AUTO_OKRUG_NAME = or_(
    rule(
        dictionary({
            'чукотский',
            'эвенкийский',
            'корякский',
            'ненецкий',
            'таймырский',
            'агинский',
            'бурятский',
        })
    ),
    rule(caseless('коми'), '-', normalized('пермяцкий')),
    rule(caseless('долгано'), '-', normalized('ненецкий')),
    rule(caseless('ямало'), '-', normalized('ненецкий')),
).interpretation(
    Region.name
)

AUTO_OKRUG_WORDS = or_(
    rule(
        normalized('автономный'),
        normalized('округ')
    ),
    rule(caseless('ао'))
).interpretation(
    Region.type.const('автономный округ')
)

HANTI = rule(
    caseless('ханты'), '-', normalized('мансийский')
).interpretation(
    Region.name
)

BURAT = rule(
    caseless('усть'), '-', normalized('ордынский'),
    normalized('бурятский')
).interpretation(
    Region.name
)

AUTO_OKRUG = or_(
    rule(AUTO_OKRUG_NAME, AUTO_OKRUG_WORDS),
    or_(
        rule(
            HANTI,
            AUTO_OKRUG_WORDS,
            '-', normalized('югра')
        ),
        rule(
            caseless('хмао'),
        ).interpretation(Region.name),
        rule(
            caseless('хмао'),
            '-', caseless('югра')
        ).interpretation(Region.name),
    ),
    rule(
        BURAT,
        AUTO_OKRUG_WORDS
    )
).interpretation(
    Region
)


##########
#
#  RAION
#
###########


RAION_WORDS = or_(
    rule(caseless('р'), '-', in_caseless({'он', 'н'})),
    rule(normalized('район'))
).interpretation(
    Region.type.const('район')
)

RAION_SIMPLE_NAME = and_(
    ADJF,
    TITLE
)

RAION_MODIFIERS = rule(
    in_caseless({
        'усть',
        'северо',
        'александрово',
        'гаврилово',
    }),
    DASH.optional(),
    TITLE
)

RAION_COMPLEX_NAME = rule(
    RAION_MODIFIERS,
    RAION_SIMPLE_NAME
)

RAION_NAME = or_(
    rule(RAION_SIMPLE_NAME),
    RAION_COMPLEX_NAME
).interpretation(
    Region.name
)

RAION = rule(
    RAION_NAME,
    RAION_WORDS
).interpretation(
    Region
)


###########
#
#   GOROD
#
###########


# Top 200 Russia cities, cover 75% of population

COMPLEX = morph_pipeline([
    'санкт-петербург',
    'нижний новгород',
    'н.новгород',
    'ростов-на-дону',
    'набережные челны',
    'улан-удэ',
    'нижний тагил',
    'комсомольск-на-амуре',
    'йошкар-ола',
    'старый оскол',
    'великий новгород',
    'южно-сахалинск',
    'петропавловск-камчатский',
    'каменск-уральский',
    'орехово-зуево',
    'сергиев посад',
    'новый уренгой',
    'ленинск-кузнецкий',
    'великие луки',
    'каменск-шахтинский',
    'усть-илимск',
    'усолье-сибирский',
    'кирово-чепецк',
])

SIMPLE = dictionary({
    'москва',
    'новосибирск',
    'екатеринбург',
    'казань',
    'самар',
    'омск',
    'челябинск',
    'уфа',
    'волгоград',
    'пермь',
    'красноярск',
    'воронеж',
    'саратов',
    'краснодар',
    'тольятти',
    'барнаул',
    'ижевск',
    'ульяновск',
    'владивосток',
    'ярославль',
    'иркутск',
    'тюмень',
    'махачкала',
    'хабаровск',
    'оренбург',
    'новокузнецк',
    'кемерово',
    'рязань',
    'томск',
    'астрахань',
    'пенза',
    'липецк',
    'тула',
    'киров',
    'чебоксары',
    'калининград',
    'брянск',
    'курск',
    'иваново',
    'магнитогорск',
    'тверь',
    'ставрополь',
    'симферополь',
    'белгород',
    'архангельск',
    # 'владимир',
    'севастополь',
    'сочи',
    'курган',
    'смоленск',
    'калуга',
    'чита',
    'орёл',
    # 'волжский',
    'череповец',
    'владикавказ',
    'мурманск',
    'сургут',
    'вологда',
    'саранск',
    'тамбов',
    'стерлитамак',
    'грозный',
    'якутск',
    'кострома',
    'петрозаводск',
    'таганрог',
    'нижневартовск',
    'братск',
    'новороссийск',
    'дзержинск',
    'шахта',
    'нальчик',
    'орск',
    'сыктывкар',
    'нижнекамск',
    'ангарск',
    'балашиха',
    'благовещенск',
    'прокопьевск',
    'химки',
    'псков',
    'бийск',
    'энгельс',
    'рыбинск',
    'балаково',
    'северодвинск',
    'армавир',
    'подольск',
    # 'королёв',
    'сызрань',
    'норильск',
    'златоуст',
    'мытищи',
    'люберцы',
    'волгодонск',
    'новочеркасск',
    'абакан',
    'находка',
    'уссурийск',
    'березники',
    'салават',
    'электросталь',
    'миасс',
    'первоуральск',
    'рубцовск',
    'альметьевск',
    'ковровый',
    'коломна',
    'керчь',
    'майкоп',
    'пятигорск',
    'одинцово',
    'копейск',
    'хасавюрт',
    'новомосковск',
    'кисловодск',
    'серпухов',
    'новочебоксарск',
    'нефтеюганск',
    'димитровград',
    'нефтекамск',
    'черкесск',
    'дербент',
    'камышин',
    'невинномысск',
    'красногорск',
    'мур',
    'батайск',
    'новошахтинск',
    'ноябрьск',
    'кызыл',
    # 'октябрьский',
    'ачинск',
    'северск',
    'новокуйбышевск',
    'елец',
    'евпатория',
    'арзамас',
    'обнинск',
    'каспийск',
    'элиста',
    'пушкино',
    # 'жуковский',
    'междуреченск',
    'сарапул',
    'ессентуки',
    'воткинск',
    'ногинск',
    'тобольск',
    'ухта',
    'серов',
    'бердск',
    'мичуринск',
    'киселёвск',
    'новотроицк',
    'зеленодольск',
    'соликамск',
    'раменский',
    'домодедово',
    'магадан',
    'глазов',
    'железногорск',
    'канск',
    'назрань',
    'гатчина',
    'саров',
    'новоуральск',
    'воскресенск',
    'долгопрудный',
    'бугульма',
    'кузнецк',
    'губкин',
    'кинешма',
    'ейск',
    'реутов',
    'железногорск',
    'чайковский',
    'азов',
    'бузулук',
    'озёрск',
    'балашов',
    'юрга',
    'кропоткин',
    'клин'
})

GOROD_ABBR = in_caseless({
    'спб',
    'мск',
    'нск'   # Новосибирск
})

GOROD_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(GOROD_ABBR)
).interpretation(
    Settlement.name
)

SIMPLE = and_(
    TITLE,
    or_(
        NOUN,
        ADJF  # Железнодорожный, Юбилейный
    )
)

COMPLEX = or_(
    rule(
        SIMPLE,
        DASH.optional(),
        SIMPLE
    ),
    rule(
        TITLE,
        DASH.optional(),
        caseless('на'),
        DASH.optional(),
        TITLE
    )
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

MAYBE_GOROD_NAME = or_(
    NAME,
    rule(NAME, '-', INT)
).interpretation(
    Settlement.name
)

GOROD_WORDS = or_(
    rule(normalized('город')),
    rule(
        caseless('г'),
        DOT.optional()
    )
).interpretation(
    Settlement.type.const('город')
)

GOROD = or_(
    rule(GOROD_WORDS, MAYBE_GOROD_NAME),
    rule(
        GOROD_WORDS.optional(),
        GOROD_NAME
    )
).interpretation(
    Settlement
)


##########
#
#  SETTLEMENT NAME
#
##########


ADJS = gram('ADJS')
SIMPLE = and_(
    or_(
        NOUN,  # Александровка, Заречье, Горки
        ADJS,  # Кузнецово
        ADJF,  # Никольское, Новая, Марьино
    ),
    TITLE
)

COMPLEX = rule(
    SIMPLE,
    DASH.optional(),
    SIMPLE
)

NAME = or_(
    rule(SIMPLE),
    COMPLEX
)

SETTLEMENT_NAME = or_(
    NAME,
    rule(NAME, '-', INT),
    rule(NAME, ANUM)
)


###########
#
#   SELO
#
#############


SELO_WORDS = or_(
    rule(
        caseless('с'),
        DOT.optional()
    ),
    rule(normalized('село'))
).interpretation(
    Settlement.type.const('село')
)

SELO_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

SELO = rule(
    SELO_WORDS,
    SELO_NAME
).interpretation(
    Settlement
)


###########
#
#   DEREVNYA
#
#############


DEREVNYA_WORDS = or_(
    rule(
        caseless('д'),
        DOT.optional()
    ),
    rule(normalized('деревня'))
).interpretation(
    Settlement.type.const('деревня')
)

DEREVNYA_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

DEREVNYA = rule(
    DEREVNYA_WORDS,
    DEREVNYA_NAME
).interpretation(
    Settlement
)


###########
#
#   POSELOK
#
#############


POSELOK_WORDS = or_(
    rule(
        in_caseless({'п', 'пос'}),
        DOT.optional()
    ),
    rule(normalized('посёлок')),
    rule(
        caseless('р'),
        DOT.optional(),
        caseless('п'),
        DOT.optional()
    ),
    rule(
        normalized('рабочий'),
        normalized('посёлок')
    ),
    rule(
        caseless('пгт'),
        DOT.optional()
    ),
    rule(
        caseless('п'), DOT, caseless('г'), DOT, caseless('т'),
        DOT.optional()
    ),
    rule(
        normalized('посёлок'),
        normalized('городского'),
        normalized('типа'),
    ),
).interpretation(
    Settlement.type.const('посёлок')
)

POSELOK_NAME = SETTLEMENT_NAME.interpretation(
    Settlement.name
)

POSELOK = rule(
    POSELOK_WORDS,
    POSELOK_NAME
).interpretation(
    Settlement
)


##############
#
#   ADDRESS PERSON
#
############


ABBR = and_(
    length_eq(1),
    is_title()
)

PART = and_(
    TITLE,
    or_(
        gram('Name'),
        gram('Surn')
    )
)

MAYBE_FIO = or_(
    rule(TITLE, PART),
    rule(PART, TITLE),
    rule(ABBR, '.', TITLE),
    rule(ABBR, '.', ABBR, '.', TITLE),
    rule(TITLE, ABBR, '.', ABBR, '.')
)

POSITION_WORDS_ = or_(
    rule(
        dictionary({
            'мичман',
            'геолог',
            'подводник',
            'краевед',
            'снайпер',
            'штурман',
            'бригадир',
            'учитель',
            'политрук',
            'военком',
            'ветеран',
            'историк',
            'пулемётчик',
            'авиаконструктор',
            'адмирал',
            'академик',
            'актер',
            'актриса',
            'архитектор',
            'атаман',
            'врач',
            'воевода',
            'генерал',
            'губернатор',
            'хирург',
            'декабрист',
            'разведчик',
            'граф',
            'десантник',
            'конструктор',
            'скульптор',
            'писатель',
            'поэт',
            'капитан',
            'князь',
            'комиссар',
            'композитор',
            'космонавт',
            'купец',
            'лейтенант',
            'лётчик',
            'майор',
            'маршал',
            'матрос',
            'подполковник',
            'полковник',
            'профессор',
            'сержант',
            'старшина',
            'танкист',
            'художник',
            'герой',
            'княгиня',
            'строитель',
            'дружинник',
            'диктор',
            'прапорщик',
            'артиллерист',
            'графиня',
            'большевик',
            'патриарх',
            'сварщик',
            'офицер',
            'рыбак',
            'брат',
        })
    ),
    rule(normalized('генерал'), normalized('армия')),
    rule(normalized('герой'), normalized('россия')),
    rule(
        normalized('герой'),
        normalized('российский'), normalized('федерация')),
    rule(
        normalized('герой'),
        normalized('советский'), normalized('союз')
    ),
)

ABBR_POSITION_WORDS = rule(
    in_caseless({
        'адм',
        'ак',
        'акад',
    }),
    DOT.optional()
)

POSITION_WORDS = or_(
    POSITION_WORDS_,
    ABBR_POSITION_WORDS
)

MAYBE_PERSON = or_(
    MAYBE_FIO,
    rule(POSITION_WORDS, MAYBE_FIO),
    rule(POSITION_WORDS, TITLE)
)


###########
#
#   IMENI
#
##########


IMENI_WORDS = or_(
    rule(
        caseless('им'),
        DOT.optional()
    ),
    rule(caseless('имени'))
)

IMENI = or_(
    rule(
        IMENI_WORDS.optional(),
        MAYBE_PERSON
    ),
    rule(
        IMENI_WORDS,
        TITLE
    )
)

##########
#
#   LET
#
##########


LET_WORDS = or_(
    rule(caseless('лет')),
    rule(
        DASH.optional(),
        caseless('летия')
    )
)

LET_NAME = in_caseless({
    'влксм',
    'ссср',
    'алтая',
    'башкирии',
    'бурятии',
    'дагестана',
    'калмыкии',
    'колхоза',
    'комсомола',
    'космонавтики',
    'москвы',
    'октября',
    'пионерии',
    'победы',
    'приморья',
    'района',
    'совхоза',
    'совхозу',
    'татарстана',
    'тувы',
    'удмуртии',
    'улуса',
    'хакасии',
    'целины',
    'чувашии',
    'якутии',
})

LET = rule(
    INT,
    LET_WORDS,
    LET_NAME
)


##########
#
#    ADDRESS DATE
#
#############


MONTH_WORDS = dictionary({
    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',
})

DAY = and_(
    INT,
    gte(1),
    lte(31)
)

YEAR = and_(
    INT,
    gte(1),
    lte(2100)
)

YEAR_WORDS = normalized('год')

DATE = or_(
    rule(DAY, MONTH_WORDS),
    rule(YEAR, YEAR_WORDS)
)


#########
#
#   MODIFIER
#
############


MODIFIER_WORDS_ = rule(
    dictionary({
        'большой',
        'малый',
        'средний',

        'верхний',
        'центральный',
        'нижний',
        'северный',
        'дальний',

        'первый',
        'второй',

        'старый',
        'новый',

        'красный',
        'лесной',
        'тихий',
    }),
    DASH.optional()
)

ABBR_MODIFIER_WORDS = rule(
    in_caseless({
        'б', 'м', 'н'
    }),
    DOT.optional()
)

SHORT_MODIFIER_WORDS = rule(
    in_caseless({
        'больше',
        'мало',
        'средне',

        'верх',
        'верхне',
        'центрально',
        'нижне',
        'северо',
        'дальне',
        'восточно',
        'западно',

        'перво',
        'второ',

        'старо',
        'ново',

        'красно',
        'тихо',
        'горно',
    }),
    DASH.optional()
)

MODIFIER_WORDS = or_(
    MODIFIER_WORDS_,
    ABBR_MODIFIER_WORDS,
    SHORT_MODIFIER_WORDS,
)


##########
#
#   ADDRESS NAME
#
##########


ROD = gram('gent')

SIMPLE = and_(
    or_(
        ADJF,  # Школьная
        and_(NOUN, ROD)  # Ленина, Победы
    )
)

COMPLEX = or_(
    rule(
        and_(ADJF, TITLE),
        NOUN
    ),
    rule(
        TITLE,
        DASH.optional(),
        TITLE
    ),
)

# TODO
EXCEPTION = dictionary({
    'арбат',
    'варварка'
})

MAYBE_NAME = or_(
    rule(SIMPLE),
    COMPLEX,
    rule(EXCEPTION)
)

NAME = or_(
    MAYBE_NAME,
    LET,
    DATE,
    IMENI
)

NAME = rule(
    MODIFIER_WORDS.optional(),
    NAME
)

ADDRESS_CRF = tag('I').repeatable()

NAME = or_(
    NAME,
    ANUM,
    rule(NAME, ANUM),
    rule(ANUM, NAME),
    rule(INT, DASH.optional(), NAME),
    rule(NAME, DASH, INT),
    ADDRESS_CRF
)

ADDRESS_NAME = NAME


########
#
#    STREET
#
#########


STREET_WORDS = or_(
    rule(normalized('улица')),
    rule(
        caseless('ул'),
        DOT.optional()
    )
).interpretation(
    Street.type.const('улица')
)

STREET_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

STREET = or_(
    rule(STREET_WORDS, STREET_NAME),
    rule(STREET_NAME, STREET_WORDS)
).interpretation(
    Street
)


##########
#
#    PROSPEKT
#
##########


PROSPEKT_WORDS = or_(
    rule(
        in_caseless({'пр', 'просп'}),
        DOT.optional()
    ),
    rule(
        caseless('пр'),
        '-',
        in_caseless({'кт', 'т'}),
        DOT.optional()
    ),
    rule(normalized('проспект'))
).interpretation(
    Street.type.const('проспект')
)

PROSPEKT_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

PROSPEKT = or_(
    rule(PROSPEKT_WORDS, PROSPEKT_NAME),
    rule(PROSPEKT_NAME, PROSPEKT_WORDS)
).interpretation(
    Street
)


############
#
#    PROEZD
#
#############


PROEZD_WORDS = or_(
    rule(caseless('пр'), DOT.optional()),
    rule(
        caseless('пр'),
        '-',
        in_caseless({'зд', 'д'}),
        DOT.optional()
    ),
    rule(normalized('проезд'))
).interpretation(
    Street.type.const('проезд')
)

PROEZD_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

PROEZD = or_(
    rule(PROEZD_WORDS, PROEZD_NAME),
    rule(PROEZD_NAME, PROEZD_WORDS)
).interpretation(
    Street
)


###########
#
#   PEREULOK
#
##############


PEREULOK_WORDS = or_(
    rule(
        caseless('п'),
        DOT
    ),
    rule(
        caseless('пер'),
        DOT.optional()
    ),
    rule(normalized('переулок'))
).interpretation(
    Street.type.const('переулок')
)

PEREULOK_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

PEREULOK = or_(
    rule(PEREULOK_WORDS, PEREULOK_NAME),
    rule(PEREULOK_NAME, PEREULOK_WORDS)
).interpretation(
    Street
)


########
#
#  PLOSHAD
#
##########


PLOSHAD_WORDS = or_(
    rule(
        caseless('пл'),
        DOT.optional()
    ),
    rule(normalized('площадь'))
).interpretation(
    Street.type.const('площадь')
)

PLOSHAD_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

PLOSHAD = or_(
    rule(PLOSHAD_WORDS, PLOSHAD_NAME),
    rule(PLOSHAD_NAME, PLOSHAD_WORDS)
).interpretation(
    Street
)


############
#
#   SHOSSE
#
###########


# TODO
# Покровское 17 км.
# Сергеляхское 13 км
# Сергеляхское 14 км.


SHOSSE_WORDS = or_(
    rule(
        caseless('ш'),
        DOT
    ),
    rule(normalized('шоссе'))
).interpretation(
    Street.type.const('шоссе')
)

SHOSSE_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

SEP = in_('.,')

lit = in_caseless({
    'й', 'ом', 'ой', 'м'
})

kms_int = or_(
    rule(INT, '-', lit),
    rule(INT, lit),
    rule(INT))

kms_words = or_(
    rule(normalized('километр')),
    rule(caseless('км'), 
         SEP.optional()))

KMS = rule(
    kms_int,
    kms_words
)


SHOSSE = or_(
    rule(KMS.optional(), SHOSSE_WORDS, SHOSSE_NAME),
    rule(SHOSSE_WORDS, SHOSSE_NAME, KMS.optional()),
    rule(KMS.optional(), SHOSSE_NAME, SHOSSE_WORDS),
    rule(SHOSSE_NAME, SHOSSE_WORDS, KMS.optional())
).interpretation(
    Street
)

########
#
#  NABEREG
#
##########


NABEREG_WORDS = or_(
    rule(
        caseless('наб'),
        DOT.optional()
    ),
    rule(normalized('набережная'))
).interpretation(
    Street.type.const('набережная')
)

NABEREG_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

NABEREG = or_(
    rule(NABEREG_WORDS, NABEREG_NAME),
    rule(NABEREG_NAME, NABEREG_WORDS)
).interpretation(
    Street
)


########
#
#  BULVAR
#
##########


BULVAR_WORDS = or_(
    rule(
        caseless('б'),
        '-',
        caseless('р')
    ),
    rule(
        caseless('б'),
        DOT
    ),
    rule(
        caseless('бул'),
        DOT.optional()
    ),
    rule(normalized('бульвар'))
).interpretation(
    Street.type.const('бульвар')
)

BULVAR_NAME = ADDRESS_NAME.interpretation(
    Street.name
)

BULVAR = or_(
    rule(BULVAR_WORDS, BULVAR_NAME),
    rule(BULVAR_NAME, BULVAR_WORDS)
).interpretation(
    Street
)

###
## METRO

DOT = eq('.')
METRO_WORDS = or_(
    rule(normalized('метро')),
    rule(
        caseless('м'),
        DOT.optional()
    )
).interpretation(
    Metro.type.const('метро')
)

METRO_NAMES = morph_pipeline(
   ['Девяткино',
 'Гражданский проспект',
 'Академическая',
 'Политехническая',
 'Площадь Мужества',
 'Лесная',
 'Выборгская',
 'Площадь Ленина',
 'Чернышевская',
 'Площадь Восстания',
 'Владимирская',
 'Пушкинская',
 'Балтийская',
 'Нарвская',
 'Кировский завод',
 'Автово',
 'Ленинский проспект',
 'Проспект Ветеранов',
 'Парнас',
 'Проспект Просвещения',
 'Озерки',
 'Удельная',
 'Пионерская',
 'Чёрная речка',
 'Петроградская',
 'Горьковская',
 'Невский проспект',
 'Сенная площадь',
 'Фрунзенская',
 'Московские ворота',
 'Электросила',
 'Парк Победы',
 'Московская',
 'Звёздная',
 'Купчино',
 'Беговая',
 'Новокрестовская',
 'Приморская',
 'Василеостровская',
 'Гостиный двор',
 'Маяковская',
 'Площадь Александра Невского',
 'Елизаровская',
 'Ломоносовская',
 'Пролетарская',
 'Обухово',
 'Рыбацкое',
 'Спасская',
 'Достоевская',
 'Лиговский проспект',
 'Площадь Александра Невского',
 'Новочеркасская',
 'Ладожская',
 'Проспект Большевиков',
 'Улица Дыбенко',
 'Комендантский проспект',
 'Старая Деревня',
 'Крестовский остров',
 'Чкаловская',
 'Спортивная',
 'Адмиралтейская',
 'Садовая',
 'Звенигородская',
 'Обводный канал',
 'Волковская',
 'Бухарестская',
 'Международная',
 'Бульвар Рокоссовского',
 'Черкизовская',
 'Преображенская площадь',
 'Сокольники',
 'Красносельская',
 'Комсомольская',
 'Красные Ворота',
 'Чистые пруды',
 'Лубянка',
 'Охотный Ряд',
 'Библиотека имени Ленина',
 'Кропоткинская',
 'Парк культуры',
 'Фрунзенская',
 'Спортивная',
 'Воробьёвы горы',
 'Университет',
 'Проспект Вернадского',
 'Юго-Западная',
 'Тропарёво',
 'Румянцево',
 'Саларьево',
 'Ховрино',
 'Беломорская',
 'Речной вокзал',
 'Водный стадион',
 'Войковская',
 'Сокол',
 'Аэропорт',
 'Динамо',
 'Белорусская',
 'Маяковская',
 'Тверская',
 'Театральная',
 'Новокузнецкая',
 'Павелецкая',
 'Автозаводская',
 'Технопарк',
 'Коломенская',
 'Каширская',
 'Кантемировская',
 'Царицыно',
 'Орехово',
 'Домодедовская',
 'Красногвардейская',
 'Алма-Атинская',
 'Пятницкое шоссе',
 'Митино',
 'Волоколамская',
 'Мякинино',
 'Строгино',
 'Крылатское',
 'Молодёжная',
 'Кунцевская',
 'Славянский бульвар',
 'Парк Победы',
 'Киевская',
 'Смоленская',
 'Арбатская',
 'Площадь Революции',
 'Курская',
 'Бауманская',
 'Электрозаводская',
 'Семёновская',
 'Партизанская',
 'Измайловская',
 'Первомайская',
 'Щёлковская',
 'Кунцевская',
 'Пионерская',
 'Филёвский парк',
 'Багратионовская',
 'Фили',
 'Кутузовская',
 'Студенческая',
 'Международная',
 'Выставочная',
 'Киевская',
 'Смоленская',
 'Арбатская',
 'Александровский сад',
 'Парк культуры',
 'Октябрьская',
 'Добрынинская',
 'Павелецкая',
 'Таганская',
 'Курская',
 'Комсомольская',
 'Проспект Мира',
 'Новослободская',
 'Белорусская',
 'Краснопресненская',
 'Киевская',
 'Медведково',
 'Бабушкинская',
 'Свиблово',
 'Ботанический сад',
 'ВДНХ',
 'Алексеевская',
 'Рижская',
 'Проспект Мира',
 'Сухаревская',
 'Тургеневская',
 'Китай-город',
 'Третьяковская',
 'Октябрьская',
 'Шаболовская',
 'Ленинский проспект',
 'Академическая',
 'Профсоюзная',
 'Новые Черёмушки',
 'Калужская',
 'Беляево',
 'Коньково',
 'Тёплый Стан',
 'Ясенево',
 'Новоясеневская',
 'Планерная',
 'Сходненская',
 'Тушинская',
 'Спартак',
 'Щукинская',
 'Октябрьское Поле',
 'Полежаевская',
 'Беговая',
 'Улица 1905 года',
 'Баррикадная',
 'Пушкинская',
 'Кузнецкий Мост',
 'Китай-город',
 'Таганская',
 'Пролетарская',
 'Волгоградский проспект',
 'Текстильщики',
 'Кузьминки',
 'Рязанский проспект',
 'Выхино',
 'Лермонтовский проспект',
 'Жулебино',
 'Котельники',
 'Рассказовка',
 'Новопеределкино',
 'Боровское шоссе',
 'Солнцево',
 'Говорово',
 'Озёрная',
 'Мичуринский проспект',
 'Раменки',
 'Ломоносовский проспект',
 'Минская',
 'Парк Победы',
 'Деловой центр',
 'Третьяковская',
 'Марксистская',
 'Площадь Ильича',
 'Авиамоторная',
 'Шоссе Энтузиастов',
 'Перово',
 'Новогиреево',
 'Новокосино',
 'Алтуфьево',
 'Бибирево',
 'Отрадное',
 'Владыкино',
 'Петровско-Разумовская',
 'Дмитровская',
 '23 Августа',
 'Абая',
 'Авиамоторная',
 'Авиастроительная',
 'Автово',
 'Автозаводская',
 'Адмиралтейская',
 'Академгородок',
 'Академика Барабашова',
 'Академика Павлова',
 'Академическая',
 'Академия наук',
 'Алабинская',
 'Алатау',
 'Александровский сад',
 'Алексеевская',
 'Алма-Атинская',
 'Алмалы',
 'Алтуфьево',
 'Аметьево',
 'Андроновка',
 'Аннино',
 'Арбатская',
 'Арсенальная',
 'Архитектора Бекетова',
 'Аэропорт',
 'Бабушкинская',
 'Багратионовская',
 'Бажовская',
 'Байконур',
 'Балтийская',
 'Баррикадная',
 'Бауманская',
 'Беговая',
 'Безымянка',
 'Белокаменная',
 'Белорусская',
 'Беляево',
 'Березовая роща',
 'Берестейская',
 'Бибирево',
 'Библиотека им. Ленина',
 'Битцевский Парк',
 'Борисово',
 'Борисовский тракт',
 'Бориспольская',
 'Боровицкая',
 'Ботаническая',
 'Ботанический сад',
 'Братиславская',
 'Бульвар Адмирала Ушакова',
 'Бульвар Дмитрия Донского',
 'Бульвар Рокоссовского',
 'Бунинская аллея',
 'Буревестник',
 'Бурнаковская',
 'Бутырская',
 'Бухарестская',
 'ВДНХ',
 'Варшавская',
 'Василеостровская',
 'Васильковская',
 'Верхние Котлы',
 'Владимирская',
 'Владыкино',
 'Водный стадион',
 'Войковская',
 'Вокзальная',
 'Волгоградский проспект',
 'Волжская',
 'Волковская',
 'Волоколамская',
 'Воробьевы горы',
 'Восток',
 'Выборгская',
 'Выдубичи',
 'Вырлица',
 'Выставочная',
 'Выставочный центр',
 'Выхино',
 'Гагаринская',
 'Геологическая',
 'Героев Днепра',
 'Героев труда',
 'Гидропарк',
 'Голосеевская',
 'Горки',
 'Горьковская',
 'Госпром',
 'Гостиный двор',
 'Гражданский проспект',
 'Грушевка',
 'Дарница',
 'Двигатель Революции',
 'Дворец "Украина"',
 'Дворец спорта',
 'Девяткино',
 'Деловой центр',
 'Демеевская',
 'Динамо',
 'Дмитровская',
 'Днепр',
 'Добрынинская',
 'Домодедовская',
 'Дорогожичи',
 'Достоевская',
 'Драмтеатр имени Ауэзова',
 'Дружбы народов',
 'Дубровка',
 'Елизаровская',
 'Жибек Жолы',
 'Житомирская',
 'Жулебино',
 'ЗИЛ',
 'Завод имени Малышева',
 'Заводская',
 'Заельцовская',
 'Заречная',
 'Звенигородская',
 'Звёздная',
 'Золотая нива',
 'Золотые ворота',
 'Зорге',
 'Зябликово',
 'Измайлово',
 'Измайловская',
 'Имени А. С. Масельского',
 'Институт Культуры',
 'Ипподром',
 'Исторический музей',
 'Калужская',
 'Каменная Горка',
 'Канавинская',
 'Кантемировская',
 'Каховская',
 'Каширская',
 'Киевская',
 'Кировская',
 'Кировский завод',
 'Китай-город',
 'Кловская',
 'Кожуховская',
 'Козья слобода',
 'Коломенская',
 'Комендантский проспект',
 'Коммунаровская',
 'Комсомольская',
 'Контрактовая площадь',
 'Коньково',
 'Коптево',
 'Котельники',
 'Красногвардейская',
 'Краснопресненская',
 'Красносельская',
 'Красные ворота',
 'Красный проспект',
 'Красный хутор',
 'Кремлевская',
 'Крестовский остров',
 'Крестьянская застава',
 'Крещатик',
 'Кропоткинская',
 'Крылатское',
 'Крымская',
 'Кузнецкий мост',
 'Кузьминки',
 'Кунцевская',
 'Кунцевщина',
 'Купаловская',
 'Купчино',
 'Курская',
 'Кутузовская',
 'Ладожская',
 'Левобережная',
 'Ленинская',
 'Ленинский проспект',
 'Лермонтовский проспект',
 'Лесная',
 'Лесопарковая',
 'Лиговский проспект',
 'Лихоборы',
 'Локомотив',
 'Ломоносовская',
 'Ломоносовский проспект',
 'Лубянка',
 'Лужники',
 'Лукьяновская',
 'Лыбедская',
 'Люблино',
 'Майдан Независимости',
 'Малиновка',
 'Марксистская',
 'Маршала Жукова',
 'Маршала Покрышкина',
 'Марьина Роща',
 'Марьино',
 'Машиностроителей',
 'Маяковская',
 'Медведково',
 'Международная',
 'Менделеевская',
 'Металлургов',
 'Метростроителей',
 'Метростроителей имени Ващенко',
 'Минская',
 'Митино',
 'Михалово',
 'Могилевская',
 'Молодежная',
 #'Москва',
 'Московская',
 'Московская 2',
 'Московские ворота',
 'Московский проспект',
 'Мякинино',
 'Нагатинская',
 'Нагорная',
 'Нарвская',
 'Научная',
 'Нахимовский проспект',
 'Невский проспект',
 'Немига',
 'Нивки',
 'Нижегородская',
 'Новогиреево',
 'Новокосино',
 'Новокузнецкая',
 'Новослободская',
 'Новохохловская',
 'Новочеркасская',
 'Новоясеневская',
 'Новые Черемушки',
 'Обводный Канал',
 'Оболонь',
 'Обухово',
 'Озерки',
 'Окружная',
 'Октябрьская',
 'Октябрьское поле',
 'Олимпийская',
 'Орехово',
 'Осокорки',
 'Отрадное',
 'Охотный ряд',
 'Павелецкая',
 'Панфиловская',
 'Парк Культуры',
 'Парк Победы',
 'Парк Челюскинцев',
 'Парк культуры',
 'Парнас',
 'Партизанская',
 'Первомайская',
 'Перово',
 'Петровка',
 'Петровско-Разумовская',
 'Петровщина',
 'Петроградская',
 'Печатники',
 'Печерская',
 'Пионерская',
 'Планерная',
 'Площадь 1905 года',
 'Площадь Александра Невского 1',
 'Площадь Александра Невского 2',
 'Площадь Восстания',
 'Площадь Гагарина',
 'Площадь Гарина-Михайловского',
 'Площадь Ильича',
 'Площадь Ленина',
 'Площадь Льва Толстого',
 'Площадь Мужества',
 'Площадь Победы',
 'Площадь Революции',
 'Площадь Тукая',
 'Площадь Якуба Коласа',
 'Победа',
 'Позняки',
 'Полежаевская',
 'Политехническая',
 'Политехнический институт',
 'Полянка',
 'Почтовая площадь',
 'Пражская',
 'Преображенская площадь',
 'Приморская',
 'Пролетарская',
 'Проспект Большевиков',
 'Проспект Вернадского',
 'Проспект Ветеранов',
 'Проспект Гагарина',
 'Проспект Космонавтов',
 'Проспект Мира',
 'Проспект Победы',
 'Проспект Просвещения',
 'Проспект свободы',
 'Профсоюзная',
 'Пушкинская',
 'Пятницкое шоссе',
 'Райымбек батыра',
 'Раменки',
 'Речной вокзал',
 'Рижская',
 'Римская',
 'Российская',
 'Ростокино',
 'Румянцево',
 'Рыбацкое',
 'Рязанский проспект',
 'Савеловская',
 'Садовая',
 'Сайран',
 'Саларьево',
 'Свиблово',
 'Святошин',
 'Севастопольская',
 'Северный вокзал',
 'Семеновская',
 'Сенная площадь',
 'Серпуховская',
 'Сибирская',
 'Славутич',
 'Славянский бульвар',
 'Смоленская',
 'Советская',
 'Советской армии',
 'Сокол',
 'Соколиная Гора',
 'Сокольники',
 'Спартак',
 'Спасская',
 'Спортивная',
 'Сретенский бульвар',
 'Старая Деревня',
 'Стрешнево',
 'Строгино',
 'Студенческая',
 'Суконная слобода',
 'Сухаревская',
 'Сходненская',
 'Сырец',
 'Таганская',
 'Тараса Шевченко',
 'Тверская',
 'Театральная',
 'Текстильщики',
 'Телецентр',
 'Теплый Стан',
 'Теремки',
 'Технологический институт',
 'Технологический институт 2',
 'Технопарк',
 'Тимирязевская',
 'Тракторный завод',
 'Третьяковская',
 'Тропарево',
 'Трубная',
 'Тульская',
 'Тургеневская',
 'Тушинская',
 'Угрешская',
 'Удельная',
 'Улица 1905 года',
 'Улица Академика Королёва',
 'Улица Академика Янгеля',
 'Улица Горчакова',
 'Улица Дыбенко',
 'Улица Милашенкова',
 'Улица Сергея Эйзенштейна',
 'Улица Скобелевская',
 'Улица Старокачаловская',
 'Университет',
 'Уралмаш',
 'Уральская',
 'Уручье',
 'Филевский парк',
 'Фили',
 'Фонвизинская',
 'Фрунзенская',
 'Харьковская',
 'Холодная гора',
 'Хорошево',
 'Царицыно',
 'Цветной бульвар',
 'Центральный рынок',
 'Черкизовская',
 'Черниговская',
 'Чернышевская',
 'Чертановская',
 'Чеховская',
 'Чистые пруды',
 'Чкаловская',
 'Чёрная речка',
 'Шаболовская',
 'Шелепиха',
 'Шипиловская',
 'Шоссе Энтузиастов',
 'Шоссе энтузиастов',
 'Шулявская',
 'Щелковская',
 'Щукинская',
 'Электрозаводская',
 'Электросила',
 'Юго-Западная',
 'Южная',
 'Южный вокзал',
 'Юнгородок',
 'Ясенево',
 'Яшьлек (Юность)',
 'площадь Карла Маркса']
).interpretation(
    Metro.name
)

METRO = rule(
    METRO_WORDS.optional(),
    METRO_NAMES
).interpretation(
    Metro
)


### 
## NEARBY

v_raione_words = or_(
    rule(caseless('р'), '-', in_caseless({'он', 'н', 'не'})),
    rule(normalized('район')),
    rule(caseless('около'))
)

nearby_words = or_(
    rule(caseless('около')),
    v_raione_words
)
park = normalized('парк')
tc = or_(
    morph_pipeline([
    'тц',
    'торговый центр',
    'трц']),
    rule(normalized('торгово'), DASH.optional(), 
         normalized('развлекательный'), normalized('центр')
        )
)
bc = morph_pipeline([
    'бц',
    'бизнес центр',
    'бизнес-центр',
    'деловой центр'])

OTHER_OBJECTS = or_(
    #rule(nearby_words, SIMPLE),
    rule(park, SIMPLE),
    rule(tc, SIMPLE),
    rule(bc, SIMPLE)
)
    

##############
#
#   ADDRESS VALUE
#
#############


LETTER = in_caseless(set('абвгдежзиклмнопрстуфхшщэюя'))

QUOTE = in_(QUOTES)

LETTER = or_(
    rule(LETTER),
    rule(QUOTE, LETTER, QUOTE)
)

VALUE = rule(
    INT,
    LETTER.optional()
)

SEP = in_(r'/\-')

VALUE = or_(
    rule(VALUE),
    rule(VALUE, SEP, VALUE),
    rule(VALUE, SEP, LETTER)
)

ADDRESS_VALUE = rule(
    eq('№').optional(),
    VALUE
)


############
#
#    DOM
#
#############


DOM_WORDS = or_(
    rule(normalized('дом')),
    rule(
        caseless('д'),
        DOT
    )
).interpretation(
    Building.type.const('дом')
)

DOM_VALUE = ADDRESS_VALUE.interpretation(
    Building.number
)

DOM = rule(
    DOM_WORDS.optional(),
    DOM_VALUE
).interpretation(
    Building
)


###########
#
#  KORPUS
#
##########


KORPUS_WORDS = or_(
    rule(
        in_caseless({'корп', 'кор'}),
        DOT.optional()
    ),
    rule(normalized('корпус'))
).interpretation(
    Building.type.const('корпус')
)

KORPUS_VALUE = ADDRESS_VALUE.interpretation(
    Building.number
)

KORPUS = or_(
    rule(
        KORPUS_WORDS,
        KORPUS_VALUE
    ),
    rule(
        KORPUS_VALUE,
        KORPUS_WORDS
    )
).interpretation(
    Building
)


###########
#
#  STROENIE
#
##########


STROENIE_WORDS = or_(
    rule(
        caseless('стр'),
        DOT.optional()
    ),
    rule(normalized('строение'))
).interpretation(
    Building.type.const('строение')
)

STROENIE_VALUE = ADDRESS_VALUE.interpretation(
    Building.number
)

STROENIE = rule(
    STROENIE_WORDS,
    ADDRESS_VALUE
).interpretation(
    Building
)


###########
#
#   OFIS
#
#############


OFIS_WORDS = or_(
    rule(
        caseless('оф'),
        DOT.optional()
    ),
    rule(normalized('офис'))
).interpretation(
    Room.type.const('офис')
)

OFIS_VALUE = ADDRESS_VALUE.interpretation(
    Room.number
)

OFIS = rule(
    OFIS_WORDS,
    OFIS_VALUE
).interpretation(
    Room
)


###########
#
#   KVARTIRA
#
#############


KVARTIRA_WORDS = or_(
    rule(
        caseless('кв'),
        DOT.optional()
    ),
    rule(normalized('квартира'))
).interpretation(
    Room.type.const('квартира')
)

KVARTIRA_VALUE = ADDRESS_VALUE.interpretation(
    Room.number
)

KVARTIRA = rule(
    KVARTIRA_WORDS,
    KVARTIRA_VALUE
).interpretation(
    Room
)


###########
#
#   INDEX
#
#############


INDEX = and_(
    INT,
    gte(100000),
    lte(999999)
).interpretation(
    Index.value
).interpretation(
    Index
)


#############
#
#   FULL ADDRESS
#
############


OBLAST_LEVEL = or_(
    RESPUBLIKA,
    KRAI,
    OBLAST,
    AUTO_OKRUG
)
GOROD_LEVEL = or_(
    GOROD,
    DEREVNYA,
    SELO,
    POSELOK
)
STREET_LEVEL = or_(
    STREET,
    PROSPEKT,
    PROEZD,
    PEREULOK,
    PLOSHAD,
    SHOSSE,
    NABEREG,
    BULVAR,
    #NEARBY
)
OFIS_LEVEL = or_(
    OFIS,
    KVARTIRA
)

PRE_STREET_LEVEL = or_(
    INDEX,
    COUNTRY,
    OBLAST_LEVEL,
    RAION,
    GOROD_LEVEL
)

POST_STREET_LEVEL = or_(
    KORPUS,
    STROENIE,
    OFIS_LEVEL
)

SEP = in_('.,;')

ADDRESS = rule(
    rule(
        PRE_STREET_LEVEL.interpretation(
            Address.parts
        ),
        SEP.optional()
    ).optional().repeatable(),

    STREET_LEVEL.interpretation(
        Address.parts
    ).optional(),
    SEP.optional(),
    DOM.optional().interpretation(
        Address.parts
    ),

    rule(
        SEP.optional(),
        POST_STREET_LEVEL.interpretation(
            Address.parts
        )
    ).optional().repeatable(),
).interpretation(
    Address
)

STREET_LEVEL_CUSTOM = rule(
        STREET_LEVEL.interpretation(
        Address.parts
        ),
        SEP.optional(),
        DOM.optional().interpretation(
                Address.parts
                ))
