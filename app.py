import streamlit as st
from google import genai
from PIL import Image

# Konfigurasi Tampilan Utama Web Kafe
st.set_page_config(
    page_title="KafeReceipt AI - Auditor Keuangan", 
    page_icon="☕", 
    layout="centered"
)

st.title("☕ KafeReceipt AI Auditor")
st.write("Aplikasi pencatat dan pengelompokan pengeluaran kafe secara instan dari foto struk.")

# Mengambil API Key secara otomatis dari Streamlit Secrets (Aman untuk owner kafe)
# Jika belum diset di server, sediakan input teks darurat
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")

# Area Upload Foto Struk
uploaded_file = st.file_uploader("Upload Foto Struk / Nota Belanja Kafe", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Struk Belanja Kafe", use_container_width=True)
    
    if st.button("Analisis Struk Kafe"):
        if not api_key:
            st.warning("Mohon masukkan API Key terlebih dahulu!")
        else:
            with st.spinner("AI sedang membaca struk dan memilah pos pengeluaran kafe..."):
                try:
                    # Inisialisasi Client Google GenAI
                    client = genai.Client(api_key=api_key)
                    
                    prompt_kafe = (
                        "Tolong analisis foto struk belanja kafe ini. "
                        "Buatkan rincian dalam bentuk tabel yang berisi: Nama Barang, Jumlah, Harga Satuan, Subtotal, "
                        "dan kelompokkan setiap barang ke dalam salah satu Kategori Pengeluaran Kafe berikut: "
                        "1. Bahan Baku Utama (Kopi, Susu, Sirup, Teh, dll) "
                        "2. Operasional Bar & Dapur (Gelas plastik, sedotan, tissue, gas, pembersih) "
                        "3. Utilitas & Lainnya. "
                        "Sertakan juga Total Pengeluaran di bagian akhir."
                    )
                    
                    # Pemanggilan model stabil terbaru untuk multimodal
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=[image, prompt_kafe]
                    )
                    
                    st.success("Analisis Pembukuan Selesai!")
                    st.markdown("### 📊 Laporan Keuangan Kafe:")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
