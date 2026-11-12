import streamlit as st
from google import genai
from PIL import Image
import os

st.set_page_config(
    page_title="KafeReceipt AI - Auditor Keuangan", 
    page_icon="☕", 
    layout="centered"
)

st.title("☕ KafeReceipt AI Auditor")
st.write("Aplikasi pencatat dan pengelompokan pengeluaran kafe secara instan dari foto struk.")

api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

api_key = st.text_input("Masukkan Google Gemini API Key / Token:", value=api_key if api_key else "", type="password")

uploaded_file = st.file_uploader("Upload Foto Struk / Nota Belanja Kafe", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Struk Belanja Kafe", use_container_width=True)
    
    if st.button("Analisis Struk Kafe"):
        if not api_key:
            st.warning("Mohon masukkan API Key atau token terlebih dahulu, Bro!")
        else:
            with st.spinner("AI sedang membaca struk dan memilah pos pengeluaran kafe..."):
                try:
                    os.environ["GEMINI_API_KEY"] = api_key
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
                    
                    # Daftar model cadangan otomatis untuk menghindari error 503 / 404
                    response = None
                    models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-2.0-flash']
                    
                    last_error = None
                    for m in models_to_try:
                        try:
                            response = client.models.generate_content(
                                model=m,
                                contents=[image, prompt_kafe]
                            )
                            if response and response.text:
                                break
                        except Exception as err:
                            last_error = err
                            continue
                    
                    if response and response.text:
                        st.success("Analisis Pembukuan Selesai!")
                        st.markdown("### 📊 Laporan Keuangan Kafe:")
                        st.markdown(response.text)
                    else:
                        st.error(f"Server AI sedang padat, silakan coba klik sekali lagi. (Detail: {last_error})")
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis: {e}")
                    
