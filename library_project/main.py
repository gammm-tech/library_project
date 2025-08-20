from dataclasses import dataclass,asdict
import json
import os
import httpx
import json
import os
from dataclasses import asdict
from typing import Optional

@dataclass
class Book:
    title:str
    author:str
    ISBN:str
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.ISBN})"

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_books()

    def add_book(self, isbn: str) -> Optional[Book]:
        """
        ISBN ile Open Library API'den kitap bilgisi çekip kütüphaneye ekler.
        """
        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            response = httpx.get(url, timeout=10.0)

            if response.status_code == 404:
                print("Kitap bulunamadı.")
                return None

            response.raise_for_status()
            data = response.json()

            title = data.get("title", "Bilinmeyen Başlık")

            # Yazar bilgilerini ayrı API’den çekelim (authors alanında id var)
            authors = []
            if "authors" in data:
                for author in data["authors"]:
                    author_key = author.get("key")
                    if author_key:
                        author_url = f"https://openlibrary.org{author_key}.json"
                        try:
                            author_resp = httpx.get(author_url, timeout=10.0)
                            if author_resp.status_code == 200:
                                author_data = author_resp.json()
                                authors.append(author_data.get("name", "Bilinmeyen Yazar"))
                        except Exception:
                            continue

            if not authors:
                authors = ["Bilinmeyen Yazar"]

            book = Book(title, ", ".join(authors), isbn)
            self.books.append(book)
            self.save_books()
            print(f"Kitap eklendi: {book}")
            return book

        except httpx.RequestError:
            print("Bağlantı hatası: İnternet bağlantınızı kontrol edin.")
            return None
        except Exception as e:
            print("Bir hata oluştu:", e)
            return None

    def remove_book(self, isbn: str):
        self.books = [book for book in self.books if book.ISBN != isbn]
        self.save_books()

    def list_books(self):
        if not self.books:
            print("Kütüphanede kitap yok.")
        for book in self.books:
            print(book)

    def find_book(self, isbn: str):
        for book in self.books:
            if book.ISBN == isbn:
                return book
        return None

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book(**book_dict) for book_dict in data]

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([asdict(book) for book in self.books], file, indent=4, ensure_ascii=False)





def main():
    library = Library("library.json")

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın (1-5): ")

        try:
            if choice == "1":
                isbn = input("ISBN: ").strip()
                if not isbn:
                    print("ISBN boş olamaz.")
                    continue
                result = library.add_book(isbn)
                if result is None:
                    print("Kitap eklenemedi.")

            elif choice == "2":
                isbn = input("Silmek istediğiniz kitabın ISBN numarası: ").strip()
                if not isbn:
                    print("ISBN boş olamaz.")
                    continue
                library.remove_book(isbn)
                print("Kitap silindi (eğer bulunduysa).")

            elif choice == "3":
                print("\n--- Kütüphanedeki Kitaplar ---")
                library.list_books()

            elif choice == "4":
                isbn = input("Aramak istediğiniz kitabın ISBN numarası: ").strip()
                if not isbn:
                    print("ISBN boş olamaz.")
                    continue
                book = library.find_book(isbn)
                if book:
                    print("Bulunan kitap:", book)
                else:
                    print("Kitap bulunamadı.")

            elif choice == "5":
                print("Çıkış yapılıyor...")
                break

            else:
                print("Geçersiz seçim! Lütfen 1-5 arasında bir sayı girin.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()

        





