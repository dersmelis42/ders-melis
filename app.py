import streamlit as st
import os

# Sayfa Ayarları
st.set_page_config(page_title="Melis'in KPSS Başarı Günlüğü 🌸", page_icon="👑", layout="wide")

# Verileri Kalıcı Olarak Kaydetme Dosyası (Yenilenince Silinmeyi Önler)
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

# Hafızayı dosyadan yükle
kayitli_veriler = verileri_yukle()

# Renkli ve Tasarımsal Başlık
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌸 Melis'in KPSS Başarı Günlüğü 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #1C83E1;'>Günde 2 Ders | Adım Adım Konu Takibi | Son 3 Ay</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #FF4B4B;'>", unsafe_allow_html=True)

# Müfredat Konu Havuzu
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
    "XX. Yüzyılda Osmanlı Dönemi", "Kurtuluş Savaşı Hazırlık Dönemi", 
    "Kurtuluş Savaşı Muharebeler Dönemi", "Atatürk İlke ve İnkılapları", "Çağdaş Türk ve Dünya Tarihi"
]

turkce_konulari = [
    "Sözcükte ve Cümlede Anlam", "Paragrafta Anlam",
    "Ses Bilgisi & Yazım Kuralları", "Noktalama İşaretleri", 
    "Sözcük Türleri (İsim, Sıfat, Zamir, Zarf)", "Cümlenin Ögeleri & Çatı", 
    "Sözel Mantık Soruları"
]

vatandasiik_konulari = [
    "Hukukun Temel Kavramları", "Devletin Temel Ögeleri",
    "1982 Anayasası ve Temel İlkeler", "Yasama Organı (TBMM)", 
    "Yürütme Organı", "Yargı Organı", "İdare Hukuku"
]

# ---- SOL MENÜ (SIDEBAR) VE GENEL İLERLEME DURUMU ----
st.sidebar.markdown("<h2 style='color: #FF6F61;'>📅 Süreç Durumu</h2>", unsafe_allow_html=True)
if "hafta" not in st.session_state:
    st.session_state.hafta = 1

hafta = st.sidebar.slider("Kaçıncı Haftadasın Melis?", 1, 12, int(st.session_state.hafta))
st.session_state.hafta = hafta

st.sidebar.markdown("---")
st.sidebar.markdown("<h2 style='color: #9B59B6;'>📊 Genel Müfredat İlerlemesi</h2>", unsafe_allow_html=True)

# Ders bazlı genel ilerleme takibi expandaer'ları
with st.sidebar.expander("📖 Türkçe İlerlemesi"):
    turkce_biten = 0
    for k in turkce_konulari:
        k_key = f"g_tur_{k.replace(' ', '_')}"
        default_val = kayitli_veriler.get(k_key, False)
        state = st.checkbox(k, value=default_val, key=k_key)
        if state != default_val:
            veriyi_kaydet(k_key, state)
            st.rerun()
        if state:
            turkce_biten += 1
    turkce_yuzde = int((turkce_biten / len(turkce_konulari)) * 100) if turkce_konulari else 0
    st.markdown(f"**Türkçe Biten: %{turkce_yuzde}**")
    st.progress(turkce_biten / len(turkce_konulari))

with st.sidebar.expander("📐 Matematik İlerlemesi"):
    mat_biten = 0
    for k in mat_konulari:
        k_key = f"g_mat_{k.replace(' ', '_')}"
        default_val = kayitli_veriler.get(k_key, False)
        state = st.checkbox(k, value=default_val, key=k_key)
        if state != default_val:
            veriyi_kaydet(k_key, state)
            st.rerun()
        if state:
            mat_biten += 1
    mat_yuzde = int((mat_biten / len(mat_konulari)) * 100) if mat_konulari else 0
    st.markdown(f"**Matematik Biten: %{mat_yuzde}**")
    st.progress(mat_biten / len(mat_konulari))

with st.sidebar.expander("📜 Tarih İlerlemesi"):
    tarih_biten = 0
    for k in tarih_konulari:
        k_key = f"g_tar_{k.replace(' ', '_')}"
        default_val = kayitli_veriler.get(k_key, False)
        state = st.checkbox(k, value=default_val, key=k_key)
        if state != default_val:
            veriyi_kaydet(k_key, state)
            st.rerun()
        if state:
            tarih_biten += 1
    tarih_yuzde = int((tarih_biten / len(tarih_konulari)) * 100) if tarih_konulari else 0
    st.markdown(f"**Tarih Biten: %{tarih_yuzde}**")
    st.progress(tarih_biten / len(tarih_konulari))

if hafta > 6:
    with st.sidebar.expander("⚖️ Vatandaşlık İlerlemesi"):
        vat_biten = 0
        for k in vatandasiik_konulari:
            k_key = f"g_vat_{k.replace(' ', '_')}"
            default_val = kayitli_veriler.get(k_key, False)
            state = st.checkbox(k, value=default_val, key=k_key)
            if state != default_val:
                veriyi_kaydet(k_key, state)
                st.rerun()
            if state:
                vat_biten += 1
        vat_yuzde = int((vat_biten / len(vatandasiik_konulari)) * 100) if vatandasiik_konulari else 0
        st.markdown(f"**Vatandaşlık Biten: %{vat_yuzde}**")
        st.progress(vat_biten / len(vatandasiik_konulari))

st.sidebar.markdown("---")

# ---- ANA SAYFA DERS PROGRAMI EKRANI ----
st.markdown("<h3 style='color: #6C5B7B;'>🗓️ Bugün Hangi Gün?</h3>", unsafe_allow_html=True)
gun = st.selectbox("", ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi (Genel Tekrar)", "Pazar (Tatil)"])

index_mat = (hafta - 1) % len(mat_konulari)
index_tar = (hafta - 1) % len(tarih_konulari)
index_tur = (hafta - 1) % len(turkce_konulari)
index_vat = (hafta - 7) % len(vatandasiik_konulari) if hafta > 6 else 0

# Pazar Tatil Modu
if gun == "Pazar (Tatil)":
    st.balloons()
    st.markdown("<div style='background-color: #D4EDDA; padding: 30px; border-radius: 15px; text-align: center; border: 2px dashed #28A745;'><h2 style='color: #28A745;'>🎉 Harika Bir Dinlenme Günü!</h2></div>", unsafe_allow_html=True)

# Cumartesi Genel Tekrar Modu
elif "Genel Tekrar" in gun:
    st.markdown("<div style='background-color: #FFF3CD; padding: 20px; border-radius: 12px; border-left: 6px solid #FFC107;'><h4 style='color: #856404; margin: 0;'>⚠️ Cumartesi Düzeni: Yeni Konu Çalışmak Yok!</h4></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    t_keys = [f"h_{hafta}_t1", f"h_{hafta}_t2", f"h_{hafta}_t3"]
    t1 = st.checkbox("📚 Bu Hafta Çalışılan Konuların Not Tekrarı", value=kayitli_veriler.get(t_keys[0], False), key=t_keys[0])
    t2 = st.checkbox("✏️ Haftalık Soru Çözümü ve Yanlış Analizi", value=kayitli_veriler.get(t_keys[1], False), key=t_keys[1])
    t3 = st.checkbox("⏱️ 1 Adet Paragraf / Problem Rutin Testi", value=kayitli_veriler.get(t_keys[2], False), key=t_keys[2])
    
    for tk in t_keys:
        if st.session_state[tk] != kayitli_veriler.get(tk, False):
            veriyi_kaydet(tk, st.session_state[tk])
            st.rerun()

    skor = sum([t1, t2, t3])
    st.progress(skor / 3)
    if skor == 3:
        st.balloons()
        st.success("Haftalık genel tekrar başarıyla tamamlandı! Harikasın Melis! 🌟")

# Hafta İçi Çalışma Günleri
else:
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
            veriyi_kaydet(ck, st.session_state[ck])
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    toplam_skor = sum([c1, c2, c3, c4, c5, c6])
    st.markdown("<h4 style='color: #333;'>📊 Bugünün Tamamlanma Oranı:</h4>", unsafe_allow_html=True)
    st.progress(toplam_skor / 6)
    st.write(f"Tamamlanan Seans: {toplam_skor} / 6")

    if toplam_skor == 6:
        st.balloons()
        st.success("🏆 MUHTEŞEM! Melis bugün tüm görevlerini tamamladın!")

st.markdown("<hr style='border: 1px solid #FF4B4B;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-style: italic;'>Kız arkadaşın Melis için sevgi ve destekle güncellendi. 👑</p>", unsafe_allow_html=True)
