# 🐾 Evcil Hayvan Sahiplendirme ve Veteriner Kliniği Yönetim Sistemi

Bu proje, modern bir veteriner kliniğinin operasyonel iş süreçlerini (hasta takibi, randevu yönetimi, sahipsiz hayvanların kayıt altına alınması ve sahiplendirilmesi) otomatize eden **ilişkisel bir veritabanı yönetim sistemidir (VTYS)**. 

Proje, kavramsal ER diyagramı aşamasından başlanarak ilişkisel normalizasyon kurallarına (1NF, 2NF, 3NF) göre fiziksel veritabanı şemasına dökülmüş ve **Python tabanlı modern bir web arayüzü** ile entegre edilmiştir.

## 🚀 Proje Özellikleri

* **Dinamik Veri Yönetimi (CRUD):** Arayüz üzerinden Müşteri, Hayvan ve Randevu kayıtları eklenebilir, listelenebilir ve güvenli bir şekilde silinebilir.
* **İlişkisel Veri Bütünlüğü:** Foreign Key (Yabancı Anahtar) ihlallerini önlemek amacıyla, randevu veya hayvan eklerken sistem mevcut veritabanını tarar ve kullanıcıya sadece kayıtlı kişileri/hekimleri **Açılır Liste (Dropdown)** olarak sunar.
* **Kalıtım (Subclass) Hiyerarşisi:** Sistemdeki hayvanlar veri tabanı seviyesinde "Sahipli" ve "Sahipsiz" olarak ayrık (disjoint) bir yapıda yönetilir.
* **Gelişmiş SQL Sorguları:** Çoklu tablolar (Müşteri, Hayvan, Veteriner, Randevu) `INNER JOIN` işlemleriyle birleştirilerek anlamlı veri setleri halinde arayüze yansıtılır.

## 🛠️ Kullanılan Teknolojiler

* **Veritabanı Motoru:** SQLite (Hafif, hızlı ve sunucusuz mimari)
* **Backend & Veri İşleme:** Python, Pandas
* **Frontend (Arayüz):** Streamlit (Responsive web arayüzü)
* **Kavramsal Tasarım:** Chen Notasyonu ile ER Modelleme

## 📂 Dosya Yapısı

* `db_kurulum.py`: İlişkisel veritabanı tablolarını ve kısıtlamalarını (Constraints) oluşturan SQL DDL betiği.
* `ornek_veri.py`: Sistemi test etmek için örnek hekim, müşteri ve randevu verilerini sisteme enjekte eden betik.
* `app.py`: Streamlit web sunucusunu başlatan ve arayüzü çalıştıran ana uygulama dosyası.
* `veteriner_klinigi.db`: Sistemin SQLite veritabanı dosyası.

## 💻 Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda (localhost) çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

**1. Gerekli Kütüphaneleri Yükleyin**
Proje Python ve Streamlit gerektirir. Terminalinizde şu komutu çalıştırın:
```bash
pip install streamlit pandas
