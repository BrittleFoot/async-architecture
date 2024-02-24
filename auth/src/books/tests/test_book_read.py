import pytest
from books.models import Author, Book

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def author(mixer) -> Author:
    return mixer.blend(Author)


@pytest.fixture
def book(mixer, author) -> Book:
    return mixer.blend(Book, author=author)


def test_book_read(api, book, author):
    result = api.get("/api/v1/books/")

    assert result[0]["id"] == book.id
    assert result[0]["name"] == book.name
    assert result[0]["author"]["id"] == author.id
    assert result[0]["author"]["name"] == author.name
