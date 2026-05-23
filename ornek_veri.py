import sqlite3

def ornek_verileri_yukle():
    conn = sqlite3.connect('veteriner_klinigi.db')
    cursor = conn.cursor()

    # 1. MÜŞTERİLER (5 Farklı Kayıt)
    musteriler = [
        (1, 'Ahmet', 'Yılmaz', '12345678901', 'Ankara', 'Çankaya', 'Bahçelievler'),
        (2, 'Ayşe', 'Demir', '98765432109', 'Ankara', 'Keçiören', 'Etlik'),
        (3, 'Mehmet', 'Kaya', '56473829102', 'Ankara', 'Yenimahalle', 'Batıkent'),
        (4, 'Zeynep', 'Çelik', '34567891234', 'Ankara', 'Gölbaşı', 'İncek'),
        (5, 'Can', 'Öztürk', '78912345600', 'Ankara', 'Altındağ', 'Aydınlıkevler')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Musteri VALUES (?, ?, ?, ?, ?, ?, ?)", musteriler)

    # 2. MÜŞTERİ TELEFONLARI (Çok Değerli Nitelik Gösterimi İçin)
    # Ahmet Bey'in sistemde iki adet kayıtlı telefonu bulunuyor
    telefonlar = [
        (1, '0532 111 22 33'),
        (1, '0312 444 55 66'), 
        (2, '0543 222 33 44'),
        (3, '0555 333 44 55'),
        (4, '0505 444 55 66'),
        (5, '0533 555 66 77')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Musteri_Telefon VALUES (?, ?)", telefonlar)

    # 3. VETERİNER HEKİMLER (Farklı Uzmanlık Alanları)
    veterinerler = [
        (1, 'Dr. Murat Aydın', 'Cerrahi'),
        (2, 'Dr. Elif Yurt', 'Dahiliye'),
        (3, 'Dr. Seda Korkmaz', 'Aşılama ve Koruyucu Hekimlik'),
        (4, 'Dr. Burak Deniz', 'Ortopedi')
    ]
    cursor.executemany("INSERT OR IGNORE INTO Veteriner VALUES (?, ?, ?)", veterinerler)
    
    # 4. HAYVANLAR (Sahipli ve Sahipsiz Dağılımı)
    # Sütunlar: Hayvan_ID, Ad, Tur, Irk, Dogum_Tarihi, Statu, Sahiplenme_Tarihi, Bulunma_Tarihi, Kafes_No, Musteri_ID
    hayvanlar = [
        (1, 'Karabaş', 'Köpek', 'Kangal', '2022-01-15', 'Sahipli', None, None, None, 1),
        (2, 'Minnoş', 'Kedi', 'Tekir', '2024-05-10', 'Sahipsiz', None, '2026-01-10', 'K-01', None),
        (3, 'Pamuk', 'Kedi', 'Ankara Kedisi', '2023-08-20', 'Sahipli', None, None, None, 2),
        (4, 'Gofret', 'Köpek', 'Golden', '2021-11-02', 'Sahipli', None, None, None, 3),
        (5, 'Maviş', 'Kuş', 'Muhabbet Kuşu', '2025-02-14', 'Sahipli', None, None, None, 4),
        (6, 'Duman', 'Kedi', 'British Shorthair', '2025-06-01', 'Sahipsiz', None, '2026-03-20', 'K-05', None)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Hayvan VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", hayvanlar)

    # 5. TEDAVİ KATALOĞU
    tedaviler = [
        ('T01', 'Kuduz Aşısı', 450.0),
        ('T02', 'Karma Aşı', 500.0),
        ('T03', 'Kısırlaştırma Operasyonu', 2500.0),
        ('T04', 'Genel Kan Tahlili', 850.0),
        ('T05', 'Dijital Röntgen Çekimi', 700.0)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Tedavi_Katalogu VALUES (?, ?, ?)", tedaviler)

    # 6. RANDEVULAR
    randevular = [
        (1, '2026-05-25', '14:30', 'Bekliyor', 'Genel Muayene ve Rutin Kontrol', 1, 1, 1),
        (2, '2026-05-26', '10:00', 'Bekliyor', 'Yıllık Aşı Tekrarları', 2, 3, 3),
        (3, '2026-05-26', '11:15', 'Bekliyor', 'Arka Bacakta Aksama Şikayeti', 3, 4, 4),
        (4, '2026-05-27', '15:45', 'Bekliyor', 'Halsizlik ve Kusma', 4, 5, 2)
    ]
    cursor.executemany("INSERT OR IGNORE INTO Randevu VALUES (?, ?, ?, ?, ?, ?, ?, ?)", randevular)

    # 7. GEÇMİŞ TIBBİ KAYITLAR (Klinik Geçmişi Göstermek İçin)
    tibbi_kayitlar = [
        (1, 'Gastroenterit (Mide Üşütmesi)', '2026-04-10', 4), 
        (2, 'Sokakta Yaralı Bulunma - Sol Pati Travması', '2026-01-12', 2) 
    ]
    cursor.executemany("INSERT OR IGNORE INTO Tibbi_Kayit VALUES (?, ?, ?, ?)", tibbi_kayitlar)

    # 8. TIBBİ KAYIT - TEDAVİ DETAYLARI (M:N İlişkisi Gösterimi)
    detaylar = [
        (1, 'T04'), # Gofret'e kan tahlili yapılmış
        (1, 'T01'), # Gofret'e kuduz aşısı yapılmış
        (2, 'T05')  # Minnoş'a röntgen çekilmiş
    ]
    cursor.executemany("INSERT OR IGNORE INTO Kayit_Tedavi_Detay VALUES (?, ?)", detaylar)

    conn.commit()
    conn.close()
    print("Genişletilmiş zengin örnek veri seti başarıyla yüklendi! ")

if __name__ == '__main__':
    ornek_verileri_yukle()