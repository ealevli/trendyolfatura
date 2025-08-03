import streamlit as st
import json
from datetime import date

# --- Şifre kontrolü ---
st.set_page_config(page_title="Lisans Paneli", page_icon="🔐")
st.title("🔐 Trendyol Otomasyon Lisans Paneli")

password = st.text_input("Admin Şifresi", type="password")
if password != "admin123":
    st.warning("Devam etmek için geçerli şifre girin.")
    st.stop()

# --- JSON Dosyası ---
LISANS_DOSYA = "lisanslar.json"

# --- JSON'dan lisans verisini oku ---
def lisanslari_yukle():
    try:
        with open(LISANS_DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def lisans_kaydet(data):
    with open(LISANS_DOSYA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Var olan lisansları göster ---
lisanslar = lisanslari_yukle()

if lisanslar:
    st.subheader("📋 Mevcut Lisanslar")
    for kod, detay in lisanslar.items():
        st.markdown(f"**🔑 {kod}** — ⏳ {detay['baslangic']} → {detay['bitis']}")
        if detay["not"]:
            st.markdown(f"📝 {detay['not']}")
        st.markdown("---")
else:
    st.info("Henüz kayıtlı lisans bulunmuyor.")

# --- Yeni lisans ekleme formu ---
st.subheader("➕ Yeni Lisans Ekle")
with st.form("lisans_form"):
    kod = st.text_input("Lisans Kodu").strip().upper()
    baslangic = st.date_input("Başlangıç Tarihi", date.today())
    bitis = st.date_input("Bitiş Tarihi", date.today())
    not_ = st.text_area("Not / Açıklama", height=100)

    submitted = st.form_submit_button("💾 Kaydet")
    if submitted:
        if kod == "":
            st.error("Lisans kodu boş olamaz.")
        else:
            lisanslar[kod] = {
                "baslangic": str(baslangic),
                "bitis": str(bitis),
                "not": not_
            }
            lisans_kaydet(lisanslar)
            st.success(f"✅ {kod} lisansı kaydedildi.")
            st.experimental_rerun()
