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
