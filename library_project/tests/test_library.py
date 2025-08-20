import pytest
from main import Book, Library
from unittest.mock import patch

TEST_FILE = "test_library.json"

# Fixture ile test kütüphanesi oluşturup temizliyoruz
@pytest.fixture
def library():
    lib = Library(TEST_FILE)
    lib.books = []
    lib.save_books()
    yield lib
    import os
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

# Book.__str__ metodunu test
def test_str_method():
    book = Book("Test Başlık", "Test Yazar", "1234567890")
    assert str(book) == "Test Başlık by Test Yazar (ISBN: 1234567890)"

# Gerçek API çağrısı ile kitap ekleme ve bulma
def test_add_and_find_book_real_api(library):
    isbn = "9780140449136"  # Örnek ISBN (İlyada)
    book = library.add_book(isbn)
    assert book is not None
    found = library.find_book(isbn)
    assert found is not None
    assert found.ISBN == isbn

# Geçersiz ISBN ile hata yönetimi testi (mock)
def test_add_book_invalid_isbn(library):
    with patch("httpx.get") as mock_get:
        mock_get.return_value.status_code = 404
        book = library.add_book("0000000000000")
        assert book is None

# Kitap silme testi
def test_remove_book(library):
    isbn = "9780140449136"
    library.add_book(isbn)
    library.remove_book(isbn)
    assert library.find_book(isbn) is None

# Boş kütüphane listleme testi
def test_list_books_empty(capsys, library):
    library.books = []
    library.list_books()
    captured = capsys.readouterr()
    assert "Kütüphanede kitap yok." in captured.out
