import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="KPSS Güç Birliği Çalışma Programı", page_icon="📚", layout="wide")

st.title("📚 KPSS Güç Birliği Çalışma Programı")
st.subheader("Günde 7 Seans (45 dk Ders + 15 dk Mola) | Son 3 Ay")
st.markdown("---")

# Ortak hafıza havuzu (Senkronizasyon için)
if "db" not in st.session_state:
    st.session_state.db = {
        "ben_ilerleme": 0,
        "kiz_ilerleme": 0,
        "hafta": 1,
        "gun": "Pazartesi"
    }

# Kullanıcı Seçimi
user = st.sidebar.selectbox("Kullanıcı Seçin:", ["Seçiniz...", "Ben", "Kız Arkadaşım"])

if user == "Seçiniz...":
    st.info("Lütfen sol taraftaki menüden kimin ekranı olduğunu seçin.")
else:
    st.success(f"Hoş geldin! Şu an **{user}** olarak giriş yaptın. Başarılar!")

    # 3 Aylık Süreç Takibi
    st.sidebar.markdown("### 📅 Süreç Durumu")
    st.session_state.db["hafta"] = st.sidebar.slider("Kaçıncı Haftadasınız?", 1, 12, int(st.session_state.db["hafta"]))
    
    # Strateji Bilgilendirmesi
    if st.session_state.db["hafta"] <= 6:
        st.sidebar.warning("⚡ İlk 6 Hafta: Türkçe, Tarih, Matematik odaklı gidiyoruz. Vatandaşlık henüz yok.")
        dersler = ["Matematik", "Tarih", "Türkçe"]
    else:
        st.sidebar.error("🔥 Son 6 Hafta: Vatandaşlık dersi programa eklendi! Tempoyu artırın.")
        dersler = ["Matematik", "Tarih", "Türkçe", "Vatandaşlık"]

    # Gün Seçimi
    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi (Genel Tekrar)", "Pazar (Tatil)"]
    varsayilan_gun_index = gunler.index(st.session_state.db["gun"])
    st.session_state.db["gun"] = st.selectbox("Hangi Günün Programına Bakıyorsunuz?", gunler, index=varsayilan_gun_index)

    st.markdown(f"### 🗓️ {st.session_state.db['gun']} Günü Görevleri")

    # Pazar Günü Tatil Modu
    if st.session_state.db["gun"] == "Pazar (Tatil)":
        st.balloons()
        st.markdown("### 🎉 Bugün Hak Edilmiş Tatil Günü! Dinlenin, zihninizi boşaltın ve haftaya bomba gibi hazırlanın.")
    
    # Cumartesi Genel Tekrar Modu
    elif "Genel Tekrar" in st.session_state.db["gun"]:
        st.markdown("⚠️ **Bugün yeni konu çalışmak yok! Sadece geçmişin tekrarı ve soru çözümü.**")
        kol1, kol2 = st.columns(2)
        
        with kol1:
            st.markdown("#### 🧔 Senin Durumun")
            t1 = st.checkbox("Geçmiş Haftaların Genel Tekrarı (Ben)", key="ben_tekrar")
            t2 = st.checkbox("Haftalık Soru Çözümü & Analizi (Ben)", key="ben_soru")
            
        with kol2:
            st.markdown("#### 👩 Kız Arkadaşının Durumu")
            k_t1 = st.checkbox("Geçmiş Haftaların Genel Tekrarı (Kız Arkadaşım)", key="kiz_tekrar")
            k_t2 = st.checkbox("Haftalık Soru Çözümü & Analizi (Kız Arkadaşım)", key="kiz_soru")

    # Hafta İçi Yoğun Çalışma Programı
    else:
        seans_programi = [
            f"1. Seans (45 dk): {dersler[0]} Konu Çalışması",
            f"2. Seans (45 dk): {dersler[0]} Soru Çözümü",
            f"3. Seans (45 dk): {dersler[1]} Konu Çalışması",
            f"4. Seans (45 dk): {dersler[1]} Soru Çözümü",
            f"5. Seans (45 dk): {dersler[2] if len(dersler)==3 else dersler[3]} Çalışması",
            f"6. Seans (45 dk): Karma Soru Çözümü / Eksik Kapatma",
            f"7. Seans (45 dk): Günün Son Tekrarı ve Paragraf/Problem Çözümü"
        ]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🧔 Senin Seansların")
            ben_skor = 0
            for i, seans in enumerate(seans_programi):
                # Eğer kullanıcı 'Ben' ise tıklayabilir, değilse sadece durumu görür
                disabled_status = False if user == "Ben" else True
                if st.checkbox(seans, key=f"ben_s_{i}", disabled=disabled_status):
                    ben_skor += 1
            st.session_state.db["ben_ilerleme"] = ben_skor
            st.progress(st.session_state.db["ben_ilerleme"] / 7)
            st.write(f"Tamamlanan seans: {st.session_state.db['ben_ilerleme']}/7")

        with col2:
            st.markdown("#### 👩 Kız Arkadaşının Seansları")
            kiz_skor = 0
            for i, seans in enumerate(seans_programi):
                # Eğer kullanıcı 'Kız Arkadaşım' ise tıklayabilir, değilse sadece durumu görür
                disabled_status = False if user == "Kız Arkadaşım" else True
                if st.checkbox(seans, key=f"kiz_s_{i}", disabled=disabled_status):
                    kiz_skor += 1
            st.session_state.db["kiz_ilerleme"] = kiz_skor
            st.progress(st.session_state.db["kiz_ilerleme"] / 7)
            st.write(f"Tamamlanan seans: {st.session_state.db['kiz_ilerleme']}/7")

        # Günün Motivasyon Mesajları
        if st.session_state.db["ben_ilerleme"] == 7 and st.session_state.db["kiz_ilerleme"] == 7:
            st.toast("Tebrikler!", icon="🏆")
            st.success("🏆 İKİNİZ DE GÜNÜ NAKAVT ETTİNİZ! Harika bir çiftsiniz, bu sınav sizden korksun!")
        elif st.session_state.db["ben_ilerleme"] == 7:
            st.info("💪 Harika! Bugünlük görevlerini tamamladın. Şimdi kız arkadaşına destek olma zamanı!")
        elif st.session_state.db["kiz_ilerleme"] == 7:
            st.info("🌸 Kız arkadaşın 7 seansı da bitirdi! Hadi sen de tempoyu artır, ona yetiş!")

st.markdown("---")
st.caption("✨ Birbirinize verdiğiniz sözleri unutmayın. Bu web sitesi aşkla ve azimle ders çalışmanız için tasarlandı.")
