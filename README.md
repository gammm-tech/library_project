# 📚 Python Terminal ve API Kütüphane Uygulaması

## Proje Açıklaması
Bu proje, **Python** ile yazılmış bir kütüphane yönetim uygulamasıdır.  
- Terminal üzerinden kitap ekleme, silme, listeleme ve arama.  
- ISBN numarası ile Open Library API’den kitap bilgilerini çekme.  
- FastAPI ile kütüphane verilerini bir web API üzerinden erişilebilir hale getirme.  

---

## Kurulum

1. Depoyu klonlayın:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Gerekli bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

---

## Kullanım (Usage)

### Terminal Uygulaması (Aşama 1 & 2)
```bash
python main.py
```
**Menü seçenekleri:**
1. Kitap Ekle (ISBN ile)  
2. Kitap Sil  
3. Kitapları Listele  
4. Kitap Ara  
5. Çıkış  

- Kitap eklerken sadece ISBN numarasını girmeniz yeterlidir, başlık ve yazar bilgisi Open Library API’den çekilir.

---

### API Sunucusu (Aşama 3)
API sunucusunu başlatmak için:
```bash
uvicorn api:app --reload
```

- Tarayıcıda `http://127.0.0.1:8000/docs` adresine giderek interaktif API dokümantasyonunu görebilirsiniz.  

**API Endpointleri:**

| Endpoint | Method | Açıklama | Body Örneği |
|----------|--------|----------|-------------|
| `/books` | GET | Tüm kitapları listeler | - |
| `/books` | POST | ISBN ile kitap ekler | `{"isbn": "9780140449136"}` |
| `/books/{isbn}` | DELETE | Belirtilen ISBN’li kitabı siler | - |

---

## Test Senaryoları (Pytest)

Projede hem unit testler hem de API testleri bulunmaktadır.

### Unit Testler (`test_library.py`)
- `Book.__str__` metodunun doğru çalıştığını test eder.  
- `Library.add_book()` metodu ile gerçek ve geçersiz ISBN testleri.  
- Kitap ekleme, silme, listeleme ve bulma metodları test edilir.  

### API Testleri (`test_api.py`)
- FastAPI endpointleri test edilir:  
  - GET `/books` → kitap listesi  
  - POST `/books` → ISBN ile kitap ekleme  
  - DELETE `/books/{isbn}` → ISBN ile kitap silme  

### Testleri Çalıştırmak
Terminalden proje klasöründe:
```bash
pytest
```

- Tüm testler çalıştırılır ve sonuçları terminalde görüntülenir.  
- Gerçek ISBN testi internet bağlantısı gerektirir.  

---

## Notlar
- Kütüphane verileri `library.json` dosyasında saklanır, uygulama kapatılsa bile veriler kaybolmaz.  
- `requirements.txt` dosyasında tüm bağımlılıklar listelenmiştir (`httpx`, `fastapi`, `uvicorn`, `pytest`).  
