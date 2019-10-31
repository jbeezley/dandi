from collections import OrderedDict
from datetime import timedelta
from random import randint, random

from factory import Faker, LazyAttribute, LazyFunction, post_generation
from factory.django import DjangoModelFactory

from faker.providers import BaseProvider, company, date_time

from .models import Dataset, Keyword, Publication

MAX_AGE = int(timedelta(days=90).total_seconds())
MIN_AGE = int(timedelta(days=10).total_seconds())
SPECIES = OrderedDict([('mouse', 0.95), ('rat', 0.05)])


class DjauntyProvider(BaseProvider):
    def doi(self):
        num = self.random_int(min=1000, max=999999999)
        post_size = self.random_int(min=1, max=10)
        post = self.bothify('?' * post_size).lower()
        return f'10.{num}/{post}'

    def keyword(self):
        letters = self.random_int(min=6, max=16)
        return self.lexify('?' * letters).lower()


Faker.add_provider(company)
Faker.add_provider(date_time)
Faker.add_provider(DjauntyProvider)


class Optional(LazyFunction):
    def evaluate(self, instance, step, extra):
        if random() < instance.null_ratio:
            return None
        else:
            return self.function.evaluate(instance, step, extra)


class PublicationFactory(DjangoModelFactory):
    class Meta:
        model = Publication

    doi = Faker('doi')


class KeywordFactory(DjangoModelFactory):
    class Meta:
        model = Keyword

    keyword = Faker('keyword')


class DatasetFactory(DjangoModelFactory):
    class Meta:
        model = Dataset
        exclude = ['age_in_seconds']

    class Params:
        null_ratio = 0.1

    path = Faker('file_path', depth=3)
    size = Faker('random_int', max=1e9)

    genotype = Optional(Faker('word'))
    subject_id = Optional(Faker('word'))

    age_in_seconds = Faker('random_int', min=MIN_AGE, max=MAX_AGE)
    age = Optional(LazyAttribute(lambda o: timedelta(seconds=o.age_in_seconds)))

    number_of_electrodes = Optional(Faker('random_int', min=1, max=128))
    lab = Optional(Faker('company'))
    session_start_time = Optional(Faker('date_between', start_date='-30y', end_date='-1d'))
    experimenter = Optional(Faker('name'))
    session_id = Optional(Faker('pystr'))
    species = Optional(Faker('random_element', elements=SPECIES))
    identifier = Optional(Faker('pystr'))
    session_description = Optional(Faker('text'))
    institution = Optional(Faker('company'))
    number_of_units = Optional(Faker('random_int', min=1, max=150))
    nwb_version = Optional(Faker('numerify', text='#.@#.@#'))

    @post_generation
    def related_publications(self, create, *args, **kwargs):
        if not create:
            return
        for _ in range(randint(0, 5)):
            self.related_publications.add(Publication.objects.order_by('?').first())
        self.save()

    @post_generation
    def keywords(self, create, *args, **kwargs):
        if not create:
            return
        for _ in range(randint(0, 5)):
            self.keywords.add(Keyword.objects.order_by('?').first())
        self.save()
