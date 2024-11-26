from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        READER = 'reader', _('Reader')
        LIBRARIAN = 'librarian', _('Librarian')

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.READER,
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_reader(self):
        return self.role == self.Role.READER

    @property
    def is_librarian(self):
        return self.role == self.Role.LIBRARIAN

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


class ReaderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.READER)


class Reader(User):
    class Meta:
        proxy = True

    objects = ReaderManager()


class LibrarianManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.LIBRARIAN)


class Librarian(User):
    class Meta:
        proxy = True

    objects = LibrarianManager()


class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.ADMIN)


class Admin(User):
    class Meta:
        proxy = True

    objects = AdminManager()
