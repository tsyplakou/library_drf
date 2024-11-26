import random
from library.test import TestCase

from book.factories import AuthorFactory, BookFactory
from user.factories import (
    LibrarianFactory,
    ReaderFactory,
    AdminFactory,
)


class AuthorViewSetTestCase(TestCase):

    def test_only_authenticated_users_can_view_authors(self):
        for user in [
            LibrarianFactory(),
            ReaderFactory(),
            AdminFactory(),
        ]:
            with self.subTest(user=user):
                self.set_user(user)
                resp = self.client.get('/authors/')
                self.assertEqual(resp.status_code, 200)

        self.set_user(None)
        resp = self.client.get('/authors/')
        self.assertEqual(resp.status_code, 403)

    def test_only_librarian_and_admin_can_create_author(self):
        for user, expected_status_code in [
            (LibrarianFactory(), 201),
            (AdminFactory(), 201),
            (ReaderFactory(), 403),
        ]:
            with self.subTest(user=user, expected_status_code=expected_status_code):
                self.set_user(user)
                resp = self.client.post('/authors/', {
                    'first_name': f'John{user.pk}',
                    'last_name': 'Doe',
                })
                self.assertEqual(resp.status_code, expected_status_code)

    def test_list_returns_expected_data(self):
        self.set_user(random.choice([
            LibrarianFactory(),
            AdminFactory(),
            ReaderFactory(),
        ]))

        expected_authors = AuthorFactory.create_batch(size=5)

        resp = self.client.get('/authors/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)
        self.assertEqual(
            sorted([author['pk'] for author in resp.json()]),
            sorted([author.pk for author in expected_authors])
        )

        author_data = resp.json()[0]
        author_for_comparison = next(filter(
            lambda author: author.pk == author_data['pk'],
            expected_authors
        ))
        self.assertEqual(author_data, {
            'pk': author_for_comparison.pk,
            'first_name': author_for_comparison.first_name,
            'last_name': author_for_comparison.last_name,
        })

    def test_author_creation_with_invalid_data(self):
        self.set_user(random.choice([
            LibrarianFactory(),
            AdminFactory(),
        ]))

        resp = self.client.post('/authors/', {
            'first_name': '',
            'last_name': '',
        })

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['first_name'], ['This field may not be blank.'])
        self.assertEqual(resp.json()['last_name'], ['This field may not be blank.'])

        resp = self.client.post('/authors/', {})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['first_name'], ['This field is required.'])
        self.assertEqual(resp.json()['last_name'], ['This field is required.'])


class BookViewSetTestCase(TestCase):

    def test_list_adds_author_details_for_with_author_query_param(self):
        self.set_user(ReaderFactory())

        book = BookFactory()

        resp = self.client.get('/books/', {'with_author': True})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['author'], {
            'pk': book.author.pk,
            'first_name': book.author.first_name,
            'last_name': book.author.last_name,
        })

    def test_list_returns_expected_data(self):
        self.set_user(ReaderFactory())

        expected_books = BookFactory.create_batch(size=5)

        resp = self.client.get('/books/')

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 5)
        self.assertEqual(
            sorted([book['pk'] for book in resp.json()]),
            sorted([book.pk for book in expected_books])
        )

        book_data = resp.json()[0]
        book_for_comparison = next(filter(
            lambda book: book.pk == book_data['pk'],
            expected_books
        ))
        self.assertEqual(book_data, {
            'pk': book_for_comparison.pk,
            'title': book_for_comparison.title,
            'publication_year': book_for_comparison.publication_year,
            'author': book_for_comparison.author.pk,
        })
