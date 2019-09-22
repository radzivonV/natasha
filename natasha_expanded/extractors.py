# coding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from yargy import Parser

from .utils import Record
from .preprocess import normalize_text
from .markup import get_markup_notebook

from .tokenizer import TOKENIZER

from .crf import (
    CrfTagger,

    STREET_MODEL,
    get_street_features,

    NAME_MODEL,
    get_name_features
)

from .grammars.name import (
    SIMPLE_NAME,
    NAME
)
from .grammars.date import DATE
from .grammars.money import (
    MONEY,
    RATE as MONEY_RATE,
    RANGE as MONEY_RANGE
)
from .grammars.location import LOCATION
from .grammars.address import ADDRESS
from .grammars.organisation import ORGANISATION
from .grammars.person import PERSON

from .dsl import can_be_normalized


def serialize(match):
    span = match.span
    fact = match.fact
    if can_be_normalized(fact):
        fact = fact.normalized
    type = fact.__class__.__name__
    return OrderedDict([
        ('type', type),
        ('fact', fact.as_json),
        ('span', span),
    ])


class Matches(Record):
    __attributes__ = ['text', 'matches']

    def __init__(self, text, matches):
        self.text = text
        self.matches = sorted(matches, key=lambda _: _.span)

    def __iter__(self):
        return iter(self.matches)

    def __getitem__(self, index):
        return self.matches[index]

    def __len__(self):
        return len(self.matches)

    def __bool__(self):
        return bool(self.matches)

    @property
    def as_json(self):
        return [serialize(_) for _ in self.matches]

    def _repr_html_(self):
        spans = [_.span for _ in self.matches]
        markup = get_markup_notebook(self.text, spans)
        return ''.join(markup.as_html)


class Extractor(object):
    def __init__(self, rule, tokenizer=TOKENIZER, tagger=None):
        self.parser = Parser(rule, tokenizer=tokenizer, tagger=tagger)

    def __call__(self, text):
        text = normalize_text(text)
        matches = self.parser.findall(text)
        return Matches(text, matches)


class NamesExtractor(Extractor):
    def __init__(self):
        tagger = CrfTagger(
            NAME_MODEL,
            get_name_features
        )
        super(NamesExtractor, self).__init__(
            NAME,
            tagger=tagger
        )


class SimpleNamesExtractor(Extractor):
    def __init__(self):
        super(SimpleNamesExtractor, self).__init__(SIMPLE_NAME)


class PersonExtractor(Extractor):
    def __init__(self):
        tagger = CrfTagger(
            NAME_MODEL,
            get_name_features
        )
        super(PersonExtractor, self).__init__(
            PERSON,
            tagger=tagger
        )


class DatesExtractor(Extractor):
    def __init__(self):
        super(DatesExtractor, self).__init__(DATE)


class MoneyExtractor(Extractor):
    def __init__(self):
        super(MoneyExtractor, self).__init__(MONEY)


class MoneyRateExtractor(Extractor):
    def __init__(self):
        super(MoneyRateExtractor, self).__init__(MONEY_RATE)


class MoneyRangeExtractor(Extractor):
    def __init__(self):
        super(MoneyRangeExtractor, self).__init__(MONEY_RANGE)


class AddressExtractor(Extractor):
    def __init__(self):
        tagger = CrfTagger(
            STREET_MODEL,
            get_street_features
        )
        super(AddressExtractor, self).__init__(
            ADDRESS,
            tagger=tagger
        )


class LocationExtractor(Extractor):
    def __init__(self):
        super(LocationExtractor, self).__init__(LOCATION)


class OrganisationExtractor(Extractor):
    def __init__(self):
        super(OrganisationExtractor, self).__init__(ORGANISATION)
