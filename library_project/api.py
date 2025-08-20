from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from main import Library, Book


app = FastAPI()

# Test için basit endpoint
@app.get("/")
def read_root():
    return {"message": "Kütüphane API'sine hoş geldiniz!"}


app = FastAPI(title="Library API", version="1.0")

# Library nesnesi (JSON dosyasına bağlı)
library = Library("library.json")


# --- Pydantic Modelleri ---
class BookModel(BaseModel):
    title: str
    author: str
    ISBN: str

class ISBNRequest(BaseModel):
    isbn: str


# --- Endpoint'ler ---

@app.get("/books", response_model=List[BookModel])
def get_books():
    """Kütüphanedeki tüm kitapları döndürür"""
    return [BookModel(**vars(book)) for book in library.books]


@app.post("/books", response_model=BookModel)
def add_book(request: ISBNRequest):
    """ISBN alır, Open Library API'den kitap bilgisi çeker ve kütüphaneye ekler"""
    book = library.add_book(request.isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya eklenemedi.")
    return BookModel(**vars(book))


@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    """ISBN numarasına göre kitabı siler"""
    book = library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")
    library.remove_book(isbn)
    return {"message": f"{isbn} numaralı kitap silindi."}
