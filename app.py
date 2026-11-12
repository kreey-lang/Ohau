import streamlit as st
from groq import Groq
from PIL import Image
import base64
import io

st.set_page_config(
    page_title="KafeReceipt AI - Groq Auditor", 
    page_icon="⚡", 
    layout="centered"
)

st.title("⚡ KafeReceipt AI (Groq Edition)")
st.write("Aplikasi pembukuan struk kafe super cepat menggunakan Groq AI.")

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
            with st.spinner("Groq AI sedang memproses struk kilat..."):
                try:
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    image_url = f"data:image/jpeg;base64,{img_str}"
                    
                    client = Groq(api_key=groq_api_key)
                    
                    prompt_kafe = (
                        "Tolong analisis foto struk belanja kafe ini. "
                        "Buatkan rincian dalam bentuk tabel yang berisi: Nama Barang, Jumlah, Harga Satuan, Subtotal, "
                        "dan kelompokkan setiap barang ke dalam salah satu Kategori Pengeluaran Kafe berikut: "
                        "1. Bahan Baku Utama (Kopi, Susu, Sirup, Teh, dll) "
                        "2. Operasional Bar & Dapur (Gelas plastik, sedotan, tissue, gas, pembersih) "
                        "3. Utilitas & Lainnya. "
                        "Sertakan juga Total Pengeluaran di bagian akhir."
                    )
                    
                    # Menggunakan model llama-3.2-11b-vision-preview yang stabil
                    chat_completion = client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt_kafe},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": image_url}
                                    },
                                ],
                            }
                        ],
                        temperature=0.1,
                    )
                    
                    result_text = chat_completion.choices[0].message.content
                    
                    st.success("Analisis Selesai Super Cepat!")
                    st.markdown("### 📊 Laporan Keuangan Kafe:")
                    st.markdown(result_text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan teknis Groq: {e}")
                    
