import streamlit as st
import os

# Sayfa Ayarları
st.set_page_config(page_title="Melis'in KPSS Başarı Günlüğü 🌸", page_icon="👑", layout="wide")

# Verileri Kalıcı Olarak Kaydetme Dosyası
DATA_FILE = "melis_ilerleme.txt"

def verileri_yukle():
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=")
                    data[key] = val == "True"
    return data

def veriyi_kaydet(key, val):
    current_data = verileri_yukle()
    current_data[key] = val
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for k, v in current_data.items():
            f.write(f"{k}={v}\n")

kayitli_veriler = verileri_yukle()

# Renkli ve Tasarımsal Başlık
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌸 Melis'in KPSS Başarı Günlüğü 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #1C83E1;'>Günde 2 Ders | Adım Adım Konu Takibi | Son 3 Ay</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #FF4B4B;'>", unsafe_allow_html=True)

# KPSS Ön Lisans Müfredatı
mat_konulari = ["Temel Kavramlar", "Tek-Çift Sayılar & Basamak Kavramı", "Rasyonel ve Ondalık Sayılar", "Bölme ve Bölünebilme", "Üslü Sayılar", "Köklü Sayılar", "Basit Eşitsizlikler", "Fonksiyonlar", "Sayı ve Yaş Problemleri", "Grafik Problemleri"]
tarih_konulari = ["İslamiyet Öncesi Türk Tarihi", "İlk Türk-İslam Devletleri", "Osmanlı Devleti Kuruluş ve Yükselme", "Osmanlı Devleti Kültür ve Medeniyet", "Osmanlı Devleti Duraklama ve Gerileme", "Osmanlı Devleti Dağılma Dönemi", "XX. Yüzyılda Osmanlı Dönemi", "Kurtuluş Savaşı Hazırlık Dönemi", "Kurtuluş Savaşı Muharebeler Dönemi", "Atatürk İlke ve İnkılapları", "Çağdaş Türk ve Dünya Tarihi"]
turkce_konulari = ["Sözcükte ve Cümlede Anlam", "Paragrafta Anlam", "Ses Bilgisi & Yazım Kuralları", "Noktalama İşaretleri", "Sözcük Türleri (İsim, Sıfat, Zamir, Zarf)", "Cümlenin Ögeleri & Çatı", "Sözel Mantık Soruları"]
vatandasiik_konulari = ["Hukukun Temel Kavramları", "Devletin Temel Ögeleri", "1982 Anayasası ve Temel İlkeler", "Yasama Organı (TBMM)", "Yürütme Organı", "Yargı Organı", "İdare Hukuku"]

# ---- SOL MENÜ (SIDEBAR) ----
st.sidebar.markdown("<h2 style='color: #FF6F61;'>📅 Süreç Durumu</h2>", unsafe_allow_html=True)
if "hafta" not in st.session_state:
    st.session_state.hafta = 1
hafta = st.sidebar.slider("Kaçıncı Haftadasın Melis?", 1, 12, int(st.session_state.hafta))
st.session_state.hafta = hafta

# Genel Müfredat İlerlemesi (Sidebar Açılır Kutuları)
st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color: #9B59B6;'>📊 Genel Müfredat İlerlemesi</h2>", unsafe_allow_html=True)

for d_name, d_list, d_prefix in [("📖 Türkçe", turkce_konulari, "g_tur_"), ("📐 Matematik", mat_konulari, "g_mat_"), ("📜 Tarih", tarih_konulari, "g_tar_")]:
    with st.sidebar.expander(f"{d_name} İlerlemesi"):
        biten = 0
        for k in d_list:
            k_key = f"{d_prefix}{k.replace(' ', '_')}"
            state = st.checkbox(k, value=kayitli_veriler.get(k_key, False), key=k_key)
            if state != kayitli_veriler.get(k_key, False):
                veriyi_kaydet(k_key, state)
                st.rerun()
            if state: biten += 1
        st.markdown(f"**Biten: %{int((biten/len(d_list))*100) if d_list else 0}**")
        st.progress(biten / len(d_list))

# ---- ANA SAYFA DERS PROGRAMI ----
st.markdown("<h3 style='color: #6C5B7B;'>🗓️ Bugün Hangi Gün?</h3>", unsafe_allow_html=True)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi (Genel Tekrar)", "Pazar (Tatil)"]
gun = st.selectbox("", gunler)

index_mat = (hafta - 1) % len(mat_konulari)
index_tar = (hafta - 1) % len(tarih_konulari)
index_tur = (hafta - 1) % len(turkce_konulari)
index_vat = (hafta - 7) % len(vatandasiik_konulari) if hafta > 6 else 0

# Bir Önceki Günün Eksik Seanslarını Kontrol Eden Akıllı Mekanizma
st.markdown("<br>", unsafe_allow_html=True)
eksik_seanslar = []
guncel_gun_index = gunler.index(gun)

if guncel_gun_index > 0: # Eğer bugün Pazartesi değilse, geçmiş günleri kontrol et
    for g_idx in range(guncel_gun_index):
        gecmis_gun = gunler[g_idx]
        if "Tekrar" in gecmis_gun or "Tatil" in gecmis_gun: continue
        
        # O günkü 6 seansın anahtarlarını kontrol et
        for s_no in range(1, 7):
            check_key = f"h_{hafta}_{gecmis_gun}_c{s_no}"
            # Eğer geçmiş seans işaretlenmediyse ve "borç listesine" eklenmediyse borçtur
            if not kayitli_veriler.get(check_key, False):
                # Seans ismini tahmin et
                s_isim = "Konu Çalışması" if s_no in [1, 4] else ("Soru Çözümü" if s_no in [2, 5] else "Tekrar/Analiz")
                eksik_seanslar.append((check_key, f"⏳ {gecmis_gun} gününden kalan: {s_isim}"))

# Eğer geçmişten kalan borç seans varsa en üstte uyarı olarak göster
if eksik_seanslar:
    st.markdown("<div style='background-color: #F8D7DA; padding: 15px; border-radius: 10px; border-left: 6px solid #DC3545;'><h4 style='color: #721C24; margin:0;'>⚠️ Melis, Geçmiş Günlerden Kalan Eksiklerin Var!</h4><p style='color: #721C24; font-size:14px; margin:0;'>Bu seanslar bitmeden tam ilerleme sağlayamazsın, fırsat bulunca hemen eritmelisin:</p></div>", unsafe_allow_html=True)
    for borc_key, borc_metin in eksik_seanslar:
        b_state = st.checkbox(borc_metin, value=False, key=f"borc_{borc_key}")
        if b_state: # Eğer Melis geçmiş borca tik atarsa, asıl seansı tamamlanmış say ve kaydet
            veriyi_kaydet(borc_key, True)
            st.success("Harika! Bir eksik daha kapatıldı.")
            st.rerun()
    st.markdown("<hr style='border: 1px dashed #DC3545;'>", unsafe_allow_html=True)

# GÜNLÜK DERS EKRANLARI
if gun == "Pazar (Tatil)":
    st.balloons()
    st.markdown("<div style='background-color: #D4EDDA; padding: 30px; border-radius: 15px; text-align: center; border: 2px dashed #28A745;'><h2 style='color: #28A745;'>🎉 Harika Bir Dinlenme Günü!</h2></div>", unsafe_allow_html=True)

elif "Genel Tekrar" in gun:
    st.markdown("<div style='background-color: #FFF3CD; padding: 20px; border-radius: 12px; border-left: 6px solid #FFC107;'><h4 style='color: #856404; margin: 0;'>⚠️ Cumartesi Düzeni: Yeni Konu Çalışmak Yok!</h4></div>", unsafe_allow_html=True)
    t_keys = [f"h_{hafta}_t1", f"h_{hafta}_t2", f"h_{hafta}_t3"]
    t1 = st.checkbox("📚 Bu Hafta Çalışılan Konuların Not Tekrarı", value=kayitli_veriler.get(t_keys[0], False), key=t_keys[0])
    t2 = st.checkbox("✏️ Haftalık Soru Çözümü ve Yanlış Analizi", value=kayitli_veriler.get(t_keys[1], False), key=t_keys[1])
    t3 = st.checkbox("⏱️ 1 Adet Paragraf / Problem Rutin Testi", value=kayitli_veriler.get(t_keys[2], False), key=t_keys[2])
    
    for tk in t_keys:
        if st.session_state[tk] != kayitli_veriler.get(tk, False):
            veriyi_kaydet(tk, st.session_state[tk]); st.rerun()

elif gun in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]:
    if gun in ["Pazartesi", "Çarşamba"]:
        ders1_isim, ders1_konu, d1_renk = "📐 Matematik", mat_konulari[index_mat], "#4A90E2"
        ders2_isim, ders2_konu, d2_renk = ("📖 Türkçe", turkce_konulari[index_tur], "#9B59B6") if hafta <= 6 else ("⚖️ Vatandaşlık", vatandasiik_konulari[index_vat], "#E67E22")
    else:
        ders1_isim, ders1_konu, d1_renk = "📜 Tarih", tarih_konulari[index_tar], "#2ECC71"
        ders2_isim, ders2_konu, d2_renk = "📐 Matematik", mat_konulari[(index_mat + 1) % len(mat_konulari)], "#4A90E2"

    kol1, kol2 = st.columns(2)
    c_keys = [f"h_{hafta}_{gun}_c1", f"h_{hafta}_{gun}_c2", f"h_{hafta}_{gun}_c3", f"h_{hafta}_{gun}_c4", f"h_{hafta}_{gun}_c5", f"h_{hafta}_{gun}_c6"]
    
    with kol1:
        st.markdown(f"<div style='background-color: {d1_renk}; padding: 12px; border-radius: 10px; color: white; text-align: center;'><h3>{ders1_isim}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; font-weight: bold; margin-top:10px;'>Hedef Konu: <span style='color: {d1_renk};'>{ders1_konu}</span></p>", unsafe_allow_html=True)
        c1 = st.checkbox("45 dk Konu Çalışması + Not Çıkarma", value=kayitli_veriler.get(c_keys[0], False), key=c_keys[0])
        c2 = st.checkbox("45 dk Soru Çözümü (En az 30 soru)", value=kayitli_veriler.get(c_keys[1], False), key=c_keys[1])
        c3 = st.checkbox("45 dk Yanlış Soruların Çözümünü Öğrenme", value=kayitli_veriler.get(c_keys[2], False), key=c_keys[2])

    with kol2:
        st.markdown(f"<div style='background-color: {d2_renk}; padding: 12px; border-radius: 10px; color: white; text-align: center;'><h3>{ders2_isim}</h3></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px; font-weight: bold; margin-top:10px;'>Hedef Konu: <span style='color: {d2_renk};'>{ders2_konu}</span></p>", unsafe_allow_html=True)
        c4 = st.checkbox("45 dk Konu Videosu / Kaynak Okuması", value=kayitli_veriler.get(c_keys[3], False), key=c_keys[3])
        c5 = st.checkbox("45 dk Soru Çözümü ve Pratik", value=kayitli_veriler.get(c_keys[4], False), key=c_keys[4])
        c6 = st.checkbox("45 dk Günün Son Tekrarı", value=kayitli_veriler.get(c_keys[5], False), key=c_keys[5])

    for ck in c_keys:
        if st.session_state[ck] != kayitli_veriler.get(ck, False):
            veriyi_kaydet(ck, st.session_state[ck]); st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    toplam_skor = sum([c1, c2, c3, c4, c5, c6])
    st.markdown("<h4 style='color: #333;'>📊 Bugünün Tamamlanma Oranı:</h4>", unsafe_allow_html=True)
    st.progress(toplam_skor / 6)
    if toplam_skor == 6 and not eksik_seanslar:
        st.balloons()
        st.success("🏆 MUHTEŞEM! Melis bugün tüm görevlerini tamamladın!")

st.markdown("<hr style='border: 1px solid #FF4B4B;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-style: italic;'>Kız arkadaşın Melis için sevgi ve destekle güncellendi. 👑</p>", unsafe_allow_html=True)
