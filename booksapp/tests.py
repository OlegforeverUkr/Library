from django.test import TestCase
from django.urls import reverse

from .models import Book, Author, Genre, UserModel, BorrowRequest
from datetime import date, timedelta
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BookTestCase(TestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(
            name_author='test',
            bio_author='test bio',
            author_age=50
        )
        self.book = Book.objects.create(
            book_title='test_book',
            book_summary='test_summary',
            isbn=17246325742398,
            published_date=date.today(),
        )
        self.genre = Genre.objects.create(
            name_genre='test_genre'
        )
        self.book.book_authors.add(self.author)
        self.book.book_genre.add(self.genre)

    def test_book_author(self):
        book = Book.objects.first()
        author = book.book_authors.all()
        self.assertEqual(author.count(), 1)
        self.assertEqual(author.first(), self.author)

    def test_invalid_author(self):
        author = Author.objects.create(
            name_author='test1',
            bio_author='test bio1'
        )
        self.assertNotEquals(self.book.book_authors.first(), author)

    def test_book_genre(self):
        book = Book.objects.first()
        genre = book.book_genre.all()
        self.assertEqual(genre.count(), 1)
        self.assertEqual(genre.first(), self.genre)

    def test_book_is_available(self):
        book = Book.objects.first()
        self.assertTrue(book.is_available)

    def test_book_title(self):
        book = Book.objects.first()
        self.assertEqual(str(book), 'test_book')


class BorrowRequestTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(
            name_author='test',
            bio_author='test bio',
            author_age=50
        )
        self.genre = Genre.objects.create(name_genre='test_genre')
        self.book = Book.objects.create(
            book_title='test_book',
            book_summary='test_summary',
            isbn='1234567890',
            published_date=date(2023, 1, 1),
        )
        self.book.book_authors.add(self.author)
        self.book.book_genre.add(self.genre)

        self.borrow_request = BorrowRequest.objects.create(
            overdue=False,
            request_date=date.today(),
            due_date=date.today() + timedelta(days=7),
            complete_date=None,
            book=self.book,
            borrower=self.user,
            status=1
        )

    def test_borrow_request_overdue(self):
        self.assertFalse(self.borrow_request.overdue)

    def test_request_request_date(self):
        self.assertEqual(self.borrow_request.request_date, date(2023, 9, 14))

    def test_request_due_date(self):
        self.assertEqual(self.borrow_request.due_date, date(2023, 9, 21))

    def test_request_complete_date(self):
        self.assertIsNone(self.borrow_request.complete_date)

    def test_request_book(self):
        self.assertEqual(self.borrow_request.book, self.book)

    def test_request_borrower(self):
        self.assertEqual(self.borrow_request.borrower, self.user)

    def test_request_status(self):
        self.assertEqual(self.borrow_request.status, 1)

    def test_request_str(self):
        expected_str = f"{self.user} - {self.book}"
        self.assertEqual(str(self.borrow_request), expected_str)


class TestBookViewSet(APITestCase):
    def setUp(self) -> None:
        self.author = Author.objects.create(
            name_author='test',
            bio_author='test bio',
            author_age=50
        )
        self.book = Book.objects.create(
            book_title='test_book',
            book_summary='test_summary',
            isbn=17246325742398,
            published_date=date.today(),
        )
        self.genre = Genre.objects.create(
            name_genre='test_genre'
        )
        self.book.book_authors.add(self.author)
        self.book.book_genre.add(self.genre)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.response = self.client.get(reverse('booksapp:books-list'))

    def test_list_book(self):
        self.assertEqual(self.response.status_code, 200)

    def test_response_len(self):
        self.assertEqual(len(self.response.data), 1)

    def test_response_param(self):
        data = self.response.data[0]
        id_value = data['id']
        book_title = data['book_title']
        book_summary = data['book_summary']
        isbn = data['isbn']
        self.assertEqual(id_value, 16)
        self.assertEqual(book_title, 'test_book')
        self.assertEqual(book_summary, 'test_summary')
        self.assertEqual(int(isbn), 17246325742398)
