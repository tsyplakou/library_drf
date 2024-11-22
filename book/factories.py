import factory.fuzzy

from .models import Author, Book


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ('first_name', 'last_name')

    first_name = factory.faker.Faker('first_name')
    last_name = factory.faker.Faker('last_name')


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.faker.Faker('sentence', nb_words=5)
    author = factory.SubFactory(AuthorFactory)
    publication_year = factory.fuzzy.FuzzyInteger(1900, 2024)
