import django_filters

from .models import Book


EMPTY_VALUES = ([], (), {}, "", None)


class BookCustomFilter(django_filters.Filter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        if value == '0':
            qs = qs.filter(author__first_name='Tom')
        elif value == '1':
            qs = qs.filter(author__first_name='William')
        else:
            qs = qs.filter(author__first_name='Andrew')

        return qs


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='author__first_name',
    )
    custom = BookCustomFilter()

    class Meta:
        model = Book
        fields = (
            'title',
            'first_name',
            'custom',
        )
