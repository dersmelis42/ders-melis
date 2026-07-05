import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Melis'in KPSS Başarı Günlüğü 🌸", page_icon="👑", layout="wide")

# Renkli ve Tasarımsal Başlık
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌸 Melis'in KPSS Başarı Günlüğü 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #1C83E1;'>Günde 2 Ders | Adım Adım Konu Takibi | Son 3 Ay</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #FF4B4B;'>", unsafe_allow_html=True)

# Süreç Durumu ve Hafta Seçimi (Renkli Sidebar)
st.sidebar.markdown("<h2 style='color: #FF6F61;'>📅 Süreç Durumu</h2>", unsafe_allow_html=True)
if "hafta" not in st.session_state:
    st.session_state.hafta = 1

hafta = st.sidebar.slider("Kaçıncı Haftadasın Melis?", 1, 12, int(st.session_state.hafta))
st.session_state.hafta = hafta

# İlk 6 Hafta ve Son 6 Hafta Dinamik Durumu
if hafta <= 6:
    st.sidebar.markdown(
        "<div style='background-color: #E8F4F8; padding: 10px; border-radius: 10px; border-left: 5px solid #1C83E1;'>"
        "<h4 style='color: #1C83E1; margin: 0;'>⚡ İlk 6 Hafta</h4>"
        "<p style='color: #555; font-size: 14px;'>Türkçe, Tarih ve Matematik konularını eritiyoruz!</p>"
        "</div>", 
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        "<div style='background-color: #FDF2E9; padding: 10px; border-radius: 10px; border-left: 5px solid #E67E22;'>"
        "<h4 style='color: #E67E22; margin: 0;'>🔥 Son 6 Hafta</h4>"
        "<p style='color: #555; font-size: 14px;'>Vatandaşlık dersi listeye eklendi, tempoyu koru!</p>"
        "</div>", 
        unsafe_allow_html=True
    )

# Gün Seçimi (Renkli Buton Görünümü İçin)
st.markdown("<h3 style='color: #6C5B7B;'>🗓️ Bugün Hangi Gün?</h3>", unsafe_allow_html=True)
gun = st.selectbox("", ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi (Genel Tekrar)", "Pazar (Tatil)"])

# Kitap Seç KPSS Ön Lisans Müfredatına Göre Konu Havuzu (Haftalara Dağıtılmış)
mat_konulari = [
    "Temel Kavramlar", "Tek-Çift Sayılar & Basamak Kavramı", 
    "Rasyonel ve Ondalık Sayılar", "Bölme ve Bölünebilme", 
    "Üslü Sayılar", "Köklü Sayılar", "Basit Eşitsizlikler", 
    "Fonksiyonlar", "Sayı ve Yaş Problemleri", "Grafik Problemleri"
]

tarih_konulari = [
    "İslamiyet Öncesi Türk Tarihi", "İlk Türk-İslam Devletleri", 
    "Osmanlı Devleti Kuruluş ve Yükselme", "Osmanlı Devleti Kültür ve Medeniyet", 
    "Osmanlı Devleti Duraklama ve Gerileme", "Osmanlı Devleti Dağılma Dönemi", 
    "XX. Yüzyılda Osmanlı (Trablusgarp, Balkan, I. Dünya Savaşı)", "Kurtuluş Savaşı Hazırlık Dönemi", 
    "Kurtuluş Savaşı Muharebeler Dönemi", "Atatürk İlke ve İnkılapları", "Çağdaş Türk ve Dünya Tarihi"
]

turkce_konulari = [
    "Sözcükte ve Cümlede Anlam", "Paragrafta Anlam (Ana Düşünce/Yardımcı Düşünce)",
    "Ses Bilgisi & Yazım Kuralları", "Noktalama İşaretleri", 
    "Sözcük Türleri (İsim, Sıfat, Zamir, Zarf)", "Cümlenin Ögeleri & Çatı", 
    "Sözel Mantık - Tablo ve Sıralama Soruları"
]

vatandasiik_konulari = [
    "Hukukun Temel Kavramları", "Devletin Temel Ögeleri ve Hükümet Sistemleri",
    "1982 Anayasası ve Temel İlkeler", "Yasama Organı (TBMM)", 
    "Yürütme Organı (Cumhurbaşkanlığı)", "Yargı Organı (Mahkemeler)", "İdare Hukuku"
]

# Dinamik Günlük Program Atama (Haftalık değişir, günde 2 ders)
index_mat = (hafta - 1) % len(mat_konulari)
index_tar = (hafta - 1) % len(tarih_konulari)
index_tur = (hafta - 1) % len(turkce_konulari)
index_vat = (hafta - 7) % len(vatandasiik_konulari) if hafta > 6 else 0

# Pazar Tatil Modu
if gun == "Pazar (Tatil)":
    st.balloons()
    st.markdown(
        "<div style='background-color: #D4EDDA; padding: 30px; border-radius: 15px; text-align: center; border: 2px dashed #28A745;'>"
        "<h2 style='color: #28A745;'>🎉 Harika Bir Dinlenme Günü!</h2>"
        "<p style='font-size: 18px; color: #155724;'>Melis, bugün hak edilmiş tatil günün. Zihnini boşalt, kahveni iç ve yeni haftaya enerji depola!</p>"
        "</div>", 
        unsafe_allow_html=True
    )

# Cumartesi Genel Tekrar Modu
elif "Genel Tekrar" in gun:
    st.markdown(
        "<div style='background-color: #FFF3CD; padding: 20px; border-radius: 12px; border-left: 6px solid #FFC107;'>"
        "<h4 style='color: #856404; margin: 0;'>⚠️ Cumartesi Düzeni: Yeni Konu Çalışmak Yok!</h4>"
        "<p style='color: #856404; font-size: 15px; margin: 5px 0 0 0;'>Bu hafta çalıştığın konuları gözden geçir ve bol bol soru çöz.</p>"
        "</div>", 
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    t1 = st.checkbox("📚 Bu Hafta Çalışılan Konuların Not Tekrarı", key="m_tekrar")
    t2 = st.checkbox("✏️ Haftalık Soru Çözümü ve Yapılamayan Soruların Analizi", key="m_soru")
    t3 = st.checkbox("⏱️ 1 Adet Paragraf / Problem Rutin Testi", key="m_rutin")
    
    skor = sum([t1, t2, t3])
    st.progress(skor / 3)
    if skor == 3:
        st.confetti()
        st.success("Haftalık genel tekrar başarıyla tamamlandı! Harikasın Melis! 🌟")

# Hafta İçi Çalışma Günleri
else:
    # Ders Dağılımları (Günde sadece 2 ders olacak şekilde dengelendi)
    if gun in ["Pazartesi", "Çarşamba"]:
        ders1_isim, ders1_konu, d1_renk = "📐 Matematik", mat_konulari[index_mat], "#4A90E2"
        if hafta <= 6:
            ders2_isim, ders2_konu, d2_renk = "📖 Türkçe", turkce_konulari[index_tur], "#9B59B6"
        else:
            ders2_isim, ders2_konu, d2_renk = "⚖️ Vatandaşlık", vatandasiik_konulari[index_vat], "#E67E22"
    else: # Salı, Perşembe, Cuma
        ders1_isim, ders1_konu, d1_renk = "📜 Tarih", tarih_konulari[index_tar], "#2ECC71"
        ders2_isim, ders2_konu, d2_renk = "📐 Matematik", mat_konulari[(index_mat + 1) % len(mat_konulari)], "#4A90E2"

    # Yan Yana Renkli İki Kart Görünümü
    kol1, kol2 = st.columns(2)
    
    with kol1:
        st.markdown(f"<div style='background-color: {d1_renk}; padding: 12px; border-radius: 10px; color: white; text-align: center;'><h3>{ders1_isim}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; font-weight: bold; margin-top:10px;'>Hedef Konu: <span style='color: {d1_renk};'>{ders1_konu}</span></p>", unsafe_allow_html=True)
        
        c1 = st.checkbox("45 dk Konu Çalışması + Not Çıkarma", key="d1_c1")
        c2 = st.checkbox("45 dk Soru Çözümü (En az 30 soru)", key="d1_c2")
        c3 = st.checkbox("45 dk Yanlış Soruların Çözümünü Öğrenme", key="d1_c3")

    with kol2:
        st.markdown(f"<div style='background-color: {d2_renk}; padding: 12px; border-radius: 10px; color: white; text-align: center;'><h3>{ders2_isim}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; font-weight: bold; margin-top:10px;'>Hedef Konu: <span style='color: {d2_renk};'>{ders2_konu}</span></p>", unsafe_allow_html=True)
        
        c4 = st.checkbox("45 dk Konu Videosu / Kaynak Okuması", key="d2_c1")
        c5 = st.checkbox("45 dk Soru Çözümü ve Pratik", key="d2_c2")
        c6 = st.checkbox("45 dk Günün Son Tekrarı", key="d2_c3")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Günlük Skor Hesaplama ve İlerleme Çubuğu
    toplam_skor = sum([c1, c2, c3, c4, c5, c6])
    st.markdown("<h4 style='color: #333;'>📊 Bugünün Tamamlanma Oranı:</h4>", unsafe_allow_html=True)
    st.progress(toplam_skor / 6)
    st.write(f"Tamamlanan Seans: {toplam_skor} / 6")

    # Motivasyon Mesajları
    if toplam_skor == 6:
        st.confetti()
        st.success("🏆 MUHTEŞEM! Melis bugün tüm görevlerini tamamladın ve harika bir iş çıkardın!")
    elif toplam_skor >= 4:
        st.info("✨ Çok iyi gidiyorsun Melis! Azıcık daha gayret, bugünü de dereceyle kapatacaksın!")

st.markdown("<hr style='border: 1px solid #FF4B4B;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-style: italic;'>Kız arkadaşın Melis için sevgi ve destekle güncellendi. Bu sınavı kesinlikle kazanacak! 👑</p>", unsafe_allow_html=True)
