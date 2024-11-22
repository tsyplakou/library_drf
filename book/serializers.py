from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'pk',
            'first_name',
            'last_name',
        )


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'pk',
            'title',
            'author',
            'publication_year',
        )


class BookWithAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = (
            'pk',
            'title',
            'author',
            'publication_year',
        )
