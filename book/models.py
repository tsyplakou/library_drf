from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=80)
    publication_year = models.PositiveSmallIntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books',
        help_text='Author of the book.',
    )

    def __str__(self):
        return f'{self.title} ({self.publication_year})'
