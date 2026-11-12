import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="KafeReceipt AI - Auditor Keuangan", page_icon="☕", layout="centered")

st.title("☕ KafeReceipt AI Auditor")
st.write("Aplikasi cerdas pencatat dan pengelompokan pengeluaran kafe secara instan dari foto struk.")

# API Key sudah ditanam langsung di sini
API_KEY = "AQ.Ab8RN6I1_mDyOjgaDaA1LOOzoTJF0SJCW8jGJX0lpVrDTuvLJQ"

uploaded_file = st.file_uploader("Upload Foto Struk / Nota Belanja Kafe", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Struk Belanja Kafe", use_container_width=True)
    
    if st.button("Analisis Struk Kafe"):
        with st.spinner("AI sedang membaca struk dan memilah pos pengeluaran kafe..."):
            try:
                client = genai.Client(api_key=API_KEY)
                
                prompt_kafe = (
                    "Tolong analisis foto struk belanja kafe ini. "
                    "Buatkan rincian dalam bentuk tabel yang berisi: Nama Barang, Jumlah, Harga Satuan, Subtotal, "
                    "dan kelompokkan setiap barang ke dalam salah satu Kategori Pengeluaran Kafe berikut: "
                    "1. Bahan Baku Utama (Kopi, Susu, Sirup, Teh, dll) "
                    "2. Operasional Bar & Dapur (Gelas plastik, sedotan, tissue, gas, pembersih) "
                    "3. Utilitas & Lainnya. "
                    "Sertakan juga Total Pengeluaran di bagian akhir."
                )
                
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[image, prompt_kafe]
                )
                
                st.success("Analisis Pembukuan Selesai!")
                st.markdown("### 📊 Laporan Keuangan Kafe:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
                
