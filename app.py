import streamlit as st
import sqlite3
import pandas as pd

# 1. Veritabanından veri çekme fonksiyonu (READ)
def veri_getir(sorgu):
    conn = sqlite3.connect('veteriner_klinigi.db')
    df = pd.read_sql_query(sorgu, conn)
    conn.close()
    return df

# 2. Veritabanına veri ekleme fonksiyonu (CREATE)
def veri_islem(sorgu, parametreler):
    conn = sqlite3.connect('veteriner_klinigi.db')
    cursor = conn.cursor()
    cursor.execute(sorgu, parametreler)
    conn.commit()
    conn.close()

# Sayfa Tasarımı ve Başlık
st.set_page_config(page_title="Veteriner Kliniği", layout="wide")
st.title("Evcil Hayvan Sahiplendirme ve Veteriner Kliniği")

# Sol Menü (Sidebar)
st.sidebar.header("Menü Seçenekleri")
secim = st.sidebar.radio("Gitmek istediğiniz sayfayı seçin:", ["Randevular", "Klinikteki Hayvanlar", "Müşteriler", "Yeni Kayıt Ekle", "Veri Sil"])

# Sayfa 1: Randevular
if secim == "Randevular":
    st.subheader("Yaklaşan Randevular")
    sorgu = """
    SELECT r.Tarih, r.Saat, m.Ad || ' ' || m.Soyad AS Musteri, h.Ad AS Hayvan, v.Ad_Soyad AS Veteriner, r.Durum, r.Sikayet
    FROM Randevu r
    JOIN Musteri m ON r.Musteri_ID = m.Musteri_ID
    JOIN Hayvan h ON r.Hayvan_ID = h.Hayvan_ID
    JOIN Veteriner v ON r.Veteriner_ID = v.Veteriner_ID
    """
    df = veri_getir(sorgu)
    st.dataframe(df, use_container_width=True)

# Sayfa 2: Hayvanlar
elif secim == "Klinikteki Hayvanlar":
    st.subheader("Sistemdeki Hayvanlar")
    sorgu = "SELECT Ad, Tur, Irk, Statu, Kafes_No FROM Hayvan"
    df = veri_getir(sorgu)
    st.dataframe(df, use_container_width=True)

# Sayfa 3: Müşteriler
elif secim == "Müşteriler":
    st.subheader("Kayıtlı Müşteriler")
    sorgu = "SELECT Ad, Soyad, TC_Kimlik, Il, Ilce FROM Musteri"
    df = veri_getir(sorgu)
    st.dataframe(df, use_container_width=True)

# Sayfa 4: Yeni Kayıt Ekle
elif secim == "Yeni Kayıt Ekle":
    st.subheader("Sisteme Yeni Veri Ekle")
    tab1, tab2, tab3 = st.tabs(["Müşteri Ekle", "Hayvan Ekle", "Randevu Ekle"])
    
    with tab1:
        with st.form("yeni_musteri_formu", clear_on_submit=True):
            ad = st.text_input("Ad")
            soyad = st.text_input("Soyad")
            tc_kimlik = st.text_input("TC Kimlik No", max_chars=11)
            il = st.text_input("İl")
            ilce = st.text_input("İlçe")
            
            if st.form_submit_button("Müşteriyi Kaydet"):
                if ad and soyad and tc_kimlik:
                    try:
                        sorgu = "INSERT INTO Musteri (Ad, Soyad, TC_Kimlik, Il, Ilce) VALUES (?, ?, ?, ?, ?)"
                        veri_islem(sorgu, (ad, soyad, tc_kimlik, il, ilce))
                        st.success(f"{ad} {soyad} sisteme eklendi!")
                    except sqlite3.IntegrityError:
                        st.error("Bu TC Kimlik numarasıyla kayıtlı bir müşteri zaten var!")
                else:
                    st.warning("Ad, Soyad ve TC Kimlik zorunludur.")

    with tab2:
        musteriler = veri_getir("SELECT Musteri_ID, Ad || ' ' || Soyad AS Isim FROM Musteri")
        with st.form("yeni_hayvan_formu", clear_on_submit=True):
            h_ad = st.text_input("Hayvanın Adı (Varsa)")
            h_tur = st.selectbox("Türü", ["Köpek", "Kedi", "Kuş", "Diğer"])
            h_irk = st.text_input("Irkı")
            h_statu = st.radio("Statüsü", ["Sahipli", "Sahipsiz"])
            h_kafes = st.text_input("Kafes No (Sadece Sahipsiz ise)")
            
            if not musteriler.empty:
                musteri_dict = dict(zip(musteriler['Isim'], musteriler['Musteri_ID']))
                secilen_musteri = st.selectbox("Sahibi Kim?", list(musteri_dict.keys()))
            else:
                st.warning("Sistemde müşteri yok.")
                secilen_musteri = None
                musteri_dict = {}

            if st.form_submit_button("Hayvanı Kaydet"):
                if h_statu == "Sahipli" and secilen_musteri:
                    sorgu = "INSERT INTO Hayvan (Ad, Tur, Irk, Statu, Musteri_ID) VALUES (?, ?, ?, ?, ?)"
                    veri_islem(sorgu, (h_ad, h_tur, h_irk, h_statu, musteri_dict[secilen_musteri]))
                    st.success("Sahipli hayvan kaydedildi!")
                else:
                    sorgu = "INSERT INTO Hayvan (Ad, Tur, Irk, Statu, Kafes_No) VALUES (?, ?, ?, ?, ?)"
                    veri_islem(sorgu, (h_ad, h_tur, h_irk, h_statu, h_kafes))
                    st.success("Sahipsiz hayvan kliniğe eklendi!")

    with tab3:
        veterinerler = veri_getir("SELECT Veteriner_ID, Ad_Soyad FROM Veteriner")
        hayvanlar = veri_getir("SELECT Hayvan_ID, Ad || ' (' || Tur || ')' AS Isim FROM Hayvan")
        if not musteriler.empty and not hayvanlar.empty and not veterinerler.empty:
            with st.form("yeni_randevu_formu", clear_on_submit=True):
                vet_dict = dict(zip(veterinerler['Ad_Soyad'], veterinerler['Veteriner_ID']))
                hayvan_dict = dict(zip(hayvanlar['Isim'], hayvanlar['Hayvan_ID']))
                mus_dict = dict(zip(musteriler['Isim'], musteriler['Musteri_ID']))

                r_tarih = st.date_input("Randevu Tarihi")
                r_saat = st.time_input("Randevu Saati")
                r_musteri = st.selectbox("Müşteri", list(mus_dict.keys()))
                r_hayvan = st.selectbox("Hayvan", list(hayvan_dict.keys()))
                r_vet = st.selectbox("Veteriner", list(vet_dict.keys()))
                r_sikayet = st.text_area("Şikayet")
                
                if st.form_submit_button("Randevu Oluştur"):
                    sorgu = "INSERT INTO Randevu (Tarih, Saat, Sikayet, Musteri_ID, Hayvan_ID, Veteriner_ID) VALUES (?, ?, ?, ?, ?, ?)"
                    veri_islem(sorgu, (r_tarih, str(r_saat), r_sikayet, mus_dict[r_musteri], hayvan_dict[r_hayvan], vet_dict[r_vet]))
                    st.success("Randevu başarıyla oluşturuldu!")

# Sayfa 5: Veri Sil (DELETE İşlemi)
elif secim == "Veri Sil":
    st.subheader("Sistemden Veri Sil (DELETE)")
    st.warning("Dikkat: Buradan silinen veriler veritabanından kalıcı olarak kaldırılır.")
    
    sil_tab1, sil_tab2, sil_tab3 = st.tabs(["Müşteri Sil", "Hayvan Sil", "Randevu Sil"])
    
    # 1. Müşteri Silme
    with sil_tab1:
        musteriler = veri_getir("SELECT Musteri_ID, Ad || ' ' || Soyad || ' (TC: ' || TC_Kimlik || ')' AS Isim FROM Musteri")
        if not musteriler.empty:
            mus_dict = dict(zip(musteriler['Isim'], musteriler['Musteri_ID']))
            silinecek_mus = st.selectbox("Silinecek Müşteriyi Seçin", list(mus_dict.keys()))
            if st.button("Müşteriyi Kalıcı Olarak Sil"):
                sorgu = "DELETE FROM Musteri WHERE Musteri_ID = ?"
                veri_islem(sorgu, (mus_dict[silinecek_mus],))
                st.success(f"Seçilen müşteri başarıyla silindi!")
        else:
            st.info("Sistemde silinecek müşteri bulunmuyor.")

    # 2. Hayvan Silme
    with sil_tab2:
        hayvanlar = veri_getir("SELECT Hayvan_ID, Ad || ' - ' || Tur || ' (' || Statu || ')' AS Isim FROM Hayvan")
        if not hayvanlar.empty:
            hayvan_dict = dict(zip(hayvanlar['Isim'], hayvanlar['Hayvan_ID']))
            silinecek_hayvan = st.selectbox("Silinecek Hayvanı Seçin", list(hayvan_dict.keys()))
            if st.button("Hayvanı Kalıcı Olarak Sil"):
                sorgu = "DELETE FROM Hayvan WHERE Hayvan_ID = ?"
                veri_islem(sorgu, (hayvan_dict[silinecek_hayvan],))
                st.success(f"Seçilen hayvan başarıyla silindi!")
        else:
            st.info("Sistemde silinecek hayvan bulunmuyor.")

    # 3. Randevu Silme
    with sil_tab3:
        randevular = veri_getir("""
            SELECT r.Randevu_ID, r.Tarih || ' / ' || r.Saat || ' - ' || h.Ad AS Detay 
            FROM Randevu r JOIN Hayvan h ON r.Hayvan_ID = h.Hayvan_ID
        """)
        if not randevular.empty:
            randevu_dict = dict(zip(randevular['Detay'], randevular['Randevu_ID']))
            silinecek_ran = st.selectbox("İptal Edilecek Randevuyu Seçin", list(randevu_dict.keys()))
            if st.button("Randevuyu İptal Et / Sil"):
                sorgu = "DELETE FROM Randevu WHERE Randevu_ID = ?"
                veri_islem(sorgu, (randevu_dict[silinecek_ran],))
                st.success("Randevu sistemden başarıyla silindi!")
        else:
            st.info("Sistemde iptal edilecek randevu bulunmuyor.")