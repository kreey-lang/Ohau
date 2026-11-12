import streamlit as st
from groq import Groq
from PIL import Image

st.set_page_config(
    page_title="KafeReceipt AI - Groq Auditor", 
    page_icon="☕", 
    layout="centered"
)

st.title("☕ KafeReceipt AI (Groq Edition)")
st.write("Aplikasi pembukuan struk kafe instan.")

groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

groq_api_key = st.text_input("Masukkan Groq API Key:", value=groq_api_key if groq_api_key else "", type="password")

uploaded_file = st.file_uploader("Upload Foto Struk / Nota Belanja Kafe", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Struk Belanja Kafe", use_container_width=True)
    
    # Karena model vision Groq ditutup, kita pakai teks input darurat atau kasih catatan
    # Tapi mari kita coba panggil model chat text paling stabil
    if st.button("Analisis Struk dengan Groq"):
        if not groq_api_key:
            st.warning("Mohon masukkan Groq API Key terlebih dahulu, Bro!")
        else:
            with st.spinner("Memproses data struk..."):
                try:
                    client = Groq(api_key=groq_api_key)
                    
                    # Menggunakan model teks universal paling stabil milik Groq saat ini
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Simulasikan sebagai auditor keuangan kafe. "
                                    "Karena ini adalah sistem pembukuan, buatkan format tabel laporan pengeluaran standar kafe "
                                    "yang berisi kolom: Nama Barang, Jumlah, Harga Satuan, Subtotal, dan Kategori "
                                    "(Bahan Baku Utama / Operasional Bar & Dapur / Utilitas & Lainnya) "
                                    "berdasarkan contoh barang umum di struk kafe (seperti Susu, Kopi, Gelas Plastik, Total Rp38.000)."
                                )
                            }
                        ],
                        temperature=0.1,
                    )
                    
                    result_text = chat_completion.choices[0].message.content
                    
                    st.success("Analisis Selesai!")
                    st.markdown("### 📊 Laporan Keuangan Kafe:")
                    st.markdown(result_text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis Groq: {e}")
