import factory.fuzzy

from .models import User, Reader, Librarian, Admin


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    role = factory.fuzzy.FuzzyChoice(User.Role)
    username = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password', length=10)


class LibrarianFactory(UserFactory):
    class Meta:
        model = Librarian

    role = User.Role.LIBRARIAN


class ReaderFactory(UserFactory):
    class Meta:
        model = Reader

    role = User.Role.READER


class AdminFactory(UserFactory):
    class Meta:
        model = Admin

    role = User.Role.ADMIN
