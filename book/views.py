from rest_framework import viewsets
from rest_framework.response import Response

from .models import Author, Book
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    BookWithAuthorSerializer,
)
from library.permissions import LibrarianOrReaderReadOnlyPermission
from rest_framework.permissions import IsAuthenticated


class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, LibrarianOrReaderReadOnlyPermission]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    search_fields = ['first_name', 'last_name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.query_params.get('with_author', False):
            return BookWithAuthorSerializer
        elif self.action == 'list':
            return BookSerializer
        return BookWithAuthorSerializer

    def get_queryset(self):
        if self.request.query_params.get('with_author', False):
            return self.queryset.select_related('author')
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data

        return Response(data)
