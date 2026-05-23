import sqlite3

def veritabani_olustur():
    # Veritabanına bağlan (dosya yoksa otomatik oluşturur)
    conn = sqlite3.connect('veteriner_klinigi.db')
    cursor = conn.cursor()

    # 1. Müşteri Tablosu (Birleşik Nitelik olan Adres; İl, İlçe, Mahalle olarak ayrıldı)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Musteri (
            Musteri_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ad TEXT NOT NULL,
            Soyad TEXT NOT NULL,
            TC_Kimlik TEXT UNIQUE NOT NULL,
            Il TEXT,
            Ilce TEXT,
            Mahalle TEXT
        )
    ''')

    # 2. Müşteri Telefon Tablosu (Çok Değerli Nitelik / Multi-valued Attribute)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Musteri_Telefon (
            Musteri_ID INTEGER,
            Telefon_No TEXT,
            PRIMARY KEY (Musteri_ID, Telefon_No),
            FOREIGN KEY (Musteri_ID) REFERENCES Musteri(Musteri_ID) ON DELETE CASCADE
        )
    ''')

    # 3. Hayvan Tablosu (Subclass/Alt Sınıf mantığı 'Statu' sütunu ile tek tabloda birleştirildi)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Hayvan (
            Hayvan_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ad TEXT,
            Tur TEXT NOT NULL,
            Irk TEXT,
            Dogum_Tarihi DATE,
            Statu TEXT CHECK(Statu IN ('Sahipli', 'Sahipsiz')) NOT NULL,
            Sahiplenme_Tarihi DATE,
            Bulunma_Tarihi DATE,
            Kafes_No TEXT,
            Musteri_ID INTEGER,
            FOREIGN KEY (Musteri_ID) REFERENCES Musteri(Musteri_ID) ON DELETE SET NULL
        )
    ''')

    # 4. Veteriner Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Veteriner (
            Veteriner_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Ad_Soyad TEXT NOT NULL,
            Uzmanlik TEXT
        )
    ''')

    # 5. Randevu Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Randevu (
            Randevu_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Tarih DATE NOT NULL,
            Saat TEXT NOT NULL,
            Durum TEXT DEFAULT 'Bekliyor',
            Sikayet TEXT,
            Musteri_ID INTEGER NOT NULL,
            Hayvan_ID INTEGER NOT NULL,
            Veteriner_ID INTEGER NOT NULL,
            FOREIGN KEY (Musteri_ID) REFERENCES Musteri(Musteri_ID),
            FOREIGN KEY (Hayvan_ID) REFERENCES Hayvan(Hayvan_ID),
            FOREIGN KEY (Veteriner_ID) REFERENCES Veteriner(Veteriner_ID)
        )
    ''')

    # 6. Tıbbi Kayıt Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tibbi_Kayit (
            Kayit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Teshis TEXT,
            Kayit_Tarihi DATE NOT NULL,
            Hayvan_ID INTEGER NOT NULL,
            FOREIGN KEY (Hayvan_ID) REFERENCES Hayvan(Hayvan_ID)
        )
    ''')

    # 7. Tedavi Kataloğu Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tedavi_Katalogu (
            Tedavi_Kodu TEXT PRIMARY KEY,
            Tedavi_Adi TEXT NOT NULL,
            Ucret REAL NOT NULL
        )
    ''')

    # 8. Tıbbi Kayıt - Tedavi İlişki Tablosu (M:N / Çoka Çok İlişki)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Kayit_Tedavi_Detay (
            Kayit_ID INTEGER,
            Tedavi_Kodu TEXT,
            PRIMARY KEY (Kayit_ID, Tedavi_Kodu),
            FOREIGN KEY (Kayit_ID) REFERENCES Tibbi_Kayit(Kayit_ID) ON DELETE CASCADE,
            FOREIGN KEY (Tedavi_Kodu) REFERENCES Tedavi_Katalogu(Tedavi_Kodu)
        )
    ''')

    conn.commit()
    conn.close()
    print("Veritabanı ve tüm tablolar başarıyla oluşturuldu!")

if __name__ == '__main__':
    veritabani_olustur()