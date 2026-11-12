import streamlit as st
from groq import Groq
from PIL import Image

st.set_page_config(
    page_title="Ohau AI - Asisten Keuangan UMKM", 
    page_icon="☕", 
    layout="centered"
)

st.title("☕ Ohau AI (Smart Café & UMKM Auditor)")
st.write("Aplikasi pembukuan harian kilat berbasis foto struk untuk pemilik usaha.")

groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

groq_api_key = st.text_input("Masukkan Groq API Key:", value=groq_api_key if groq_api_key else "", type="password")

# Pilihan Menu Mode Operasional Ohau AI
mode_analisis = st.selectbox(
    "Pilih Jenis Dokumen yang Ingin Diproses:",
    (
        "1. Struk Pengeluaran (Belanja Modal / Bahan Baku / Operasional)",
        "2. Rekap Penjualan / Omzet (Tutup Toko / Kasir)"
    )
)

uploaded_file = st.file_uploader("Upload Foto Struk / Nota Terkait", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Dokumen yang Di-upload", use_container_width=True)
    
    if st.button("Proses dengan Ohau AI"):
        if not groq_api_key:
            st.warning("Mohon masukkan Groq API Key terlebih dahulu, Bro!")
        else:
            with st.spinner("Ohau AI sedang merekap data keuangan..."):
                try:
                    client = Groq(api_key=groq_api_key)
                    
                    if "Struk Pengeluaran" in mode_analisis:
                        prompt_content = (
                            "Anda adalah auditor keuangan UMKM/Kafe bernama Ohau AI. "
                            "Buatkan format tabel laporan pengeluaran harian berdasarkan dokumen belanja operasional kafe. "
                            "Sertakan kolom: No, Nama Barang/Keperluan, Jumlah, Harga Satuan, Subtotal, "
                            "dan Kategori Pengeluaran (Pilih: 1. Bahan Baku Utama, 2. Operasional Bar & Dapur, atau 3. Utilitas & Lainnya). "
                            "Berikan estimasi rincian yang masuk akal dan total pengeluaran di akhir."
                        )
                    else:
                        prompt_content = (
                            "Anda adalah auditor keuangan UMKM/Kafe bernama Ohau AI. "
                            "Buatkan ringkasan laporan rekap penjualan / omzet harian berdasarkan catatan atau struk tutup toko ini. "
                            "Sertakan informasi: Total Pendapatan Kotor (Omzet), Estimasi Total Pengeluaran Hari Ini, "
                            "serta Perhitungan Laba Bersih (Net Profit) harian dalam bentuk format yang rapi dan profesional."
                        )
                    
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=[
                            {
                                "role": "system",
                                "content": "Anda adalah Ohau AI, asisten pembukuan keuangan profesional yang cerdas, cepat, dan akurat untuk pemilik usaha kafe dan UMKM."
                            },
                            {
                                "role": "user",
                                "content": prompt_content
                            }
                        ]
                    )
                    
                    result_text = completion.choices[0].message.content
                    
                    st.success("Analisis Ohau AI Selesai!")
                    st.markdown("### 📊 Laporan Keuangan Ohau AI:")
                    st.markdown(result_text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis Ohau AI: {e}")
                    
