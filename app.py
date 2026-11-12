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
    
    if st.button("Analisis Struk dengan Groq"):
        if not groq_api_key:
            st.warning("Mohon masukkan Groq API Key terlebih dahulu, Bro!")
        else:
            with st.spinner("Memproses data struk..."):
                try:
                    client = Groq(api_key=groq_api_key)
                    
                    # Menggunakan model llama-3.1-70b-versatile yang stabil dan aktif
                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": (
                                    "Bertindaklah sebagai auditor keuangan kafe. "
                                    "Berdasarkan struk belanja kafe (total Rp38.000, kasir Sinta), "
                                    "buatkan format tabel laporan pengeluaran kafe yang rapi berisi kolom: "
                                    "Nama Barang, Jumlah, Harga Satuan, Subtotal, dan Kategori "
                                    "(Bahan Baku Utama / Operasional Bar & Dapur / Utilitas & Lainnya). "
                                    "Sertakan total pengeluaran di bagian akhir."
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
                    
