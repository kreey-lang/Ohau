import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman (Lebar agar layout Moka POS kiri-kanan pas)
st.set_page_config(
    page_title="Ohau AI POS - Professional", 
    page_icon="⚡", 
    layout="wide"
)

# Custom CSS Ala Moka POS (Grid Kiri, Keranjang Kanan, Dark Mode Elegan)
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header POS */
    .pos-top-bar {
        background: #161b22;
        padding: 12px 20px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Grid Kartu Menu */
    .moka-product-box {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    .moka-product-box:hover {
        border-color: #238636;
    }
    .prod-name {
        font-size: 15px;
        font-weight: bold;
        color: #f0f6fc;
        margin-bottom: 6px;
    }
    .prod-price {
        font-size: 14px;
        color: #3fb950;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .prod-stock {
        font-size: 11px;
        color: #8b949e;
    }
    
    /* Panel Keranjang Kanan */
    .cart-container {
        background: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    
    /* Tombol */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Inisialisasi Database Sementara (Session State)
if "profil" not in st.session_state:
    st.session_state.profil = {"nama": "Kafe Ohau Official", "pemilik": "Owner", "kategori": "Kafe & Resto"}

if "produk" not in st.session_state:
    st.session_state.produk = pd.DataFrame([
        {"ID": 1, "Nama": "Kopi Susu Gula Aren", "Kategori": "Minuman", "Harga Jual": 18000, "Modal": 10000, "Stok": 50},
        {"ID": 2, "Nama": "Nasi Goreng Spesial", "Kategori": "Makanan", "Harga Jual": 25000, "Modal": 14000, "Stok": 30},
        {"ID": 3, "Nama": "Es Teh Manis", "Kategori": "Minuman", "Harga Jual": 5000, "Modal": 2000, "Stok": 100},
        {"ID": 4, "Nama": "Roti Bakar Coklat", "Kategori": "Snack", "Harga Jual": 15000, "Modal": 8000, "Stok": 25}
    ])

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

if "pengeluaran" not in st.session_state:
    st.session_state.pengeluaran = []

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# Sidebar Navigasi Menu
st.sidebar.title("⚡ Ohau AI POS")
st.sidebar.markdown(f"📍 **{st.session_state.profil['nama']}**")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigasi Utama:", 
    ["🛒 Kasir Utama (POS Moka)", "📦 Kelola Produk & Stok", "💸 Catat Pengeluaran", "📊 Laporan & Grafik", "⚙️ Setup Profil Toko"]
)

# ==========================================
# 1. MENU KASIR UTAMA (LAYOUT ALA MOKA POS)
# ==========================================
if menu == "🛒 Kasir Utama (POS Moka)":
    # Top Bar ala Moka Register
    st.markdown(f"""
        <div class="pos-top-bar">
            <div>
                <h3 style="margin:0; color: #f0f6fc;">⚡ Ohau Register POS</h3>
                <p style="margin:0; font-size:12px; color:#8b949e;">Kasir: <b>{st.session_state.profil['pemilik']}</b> | Outlet: <b>{st.session_state.profil['nama']}</b></p>
            </div>
            <div>
                <span style="background: #238636; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">● Register Online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Bagi Layout Menjadi 2 Kolom Besar (Kiri Katalog Grid, Kanan Keranjang Checkout)
    col_katalog, col_keranjang = st.columns([1.6, 1])
    
    with col_katalog:
        st.subheader("📋 Katalog Menu Produk")
        
        # Filter Kategori ala Moka
        kategori_list = ["Semua"] + list(st.session_state.produk["Kategori"].unique())
        selected_kat = st.selectbox("Filter Kategori:", kategori_list, label_visibility="collapsed")
        
        df_prod = st.session_state.produk
        if selected_kat != "Semua":
            df_prod = df_prod[df_prod["Kategori"] == selected_kat]
        
        if df_prod.empty:
            st.warning("Tidak ada produk dalam kategori ini.")
        else:
            # Grid Produk (2 kolom produk per baris)
            cols = st.columns(2)
            for index, row in df_prod.iterrows():
                col_target = cols[index % 2]
                with col_target:
                    st.markdown(f"""
                        <div class="moka-product-box">
                            <div class="prod-name">{row['Nama']}</div>
                            <div class="prod-price">Rp {row['Harga Jual']:,}</div>
                            <div class="prod-stock">Stok: {row['Stok']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"＋ Tambah", key=f"moka_grid_{row['ID']}", use_container_width=True):
                        if row['Stok'] <= 0:
                            st.error("Stok habis!")
                        else:
                            item_ada = False
                            for item in st.session_state.keranjang:
                                if item['ID'] == row['ID']:
                                    item['Qty'] += 1
                                    item['Subtotal'] = item['Qty'] * item['Harga Jual']
                                    item_ada = True
                                    break
                            if not item_ada:
                                st.session_state.keranjang.append({
                                    "ID": row['ID'],
                                    "Nama": row['Nama'],
                                    "Harga Jual": row['Harga Jual'],
                                    "Modal": row['Modal'],
                                    "Qty": 1,
                                    "Subtotal": row['Harga Jual']
                                })
                            st.rerun()

    with col_keranjang:
        st.subheader("🛍️ Current Order (Keranjang)")
        
        if not st.session_state.keranjang:
            st.info("Keranjang masih kosong. Silakan pilih menu di sebelah kiri.")
        else:
            total_belanja = 0
            for i, item in enumerate(st.session_state.keranjang):
                st.markdown(f"""
                    <div style="background: #161b22; padding: 10px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 8px;">
                        <div style="font-weight: bold; color: #f0f6fc; font-size: 14px;">{item['Nama']}</div>
                        <div style="font-size: 12px; color: #8b949e;">{item['Qty']}x @Rp {item['Harga Jual']:,} = <b style="color: #3fb950;">Rp {item['Subtotal']:,}</b></div>
                    </div>
                """, unsafe_allow_html=True)
                total_belanja += item['Subtotal']
                
                # Kontrol Qty di Keranjang
                c_min, c_plus, c_del = st.columns(3)
                if c_min.button("➖", key=f"mk_min_{i}"):
                    if item['Qty'] > 1:
                        item['Qty'] -= 1
                        item['Subtotal'] = item['Qty'] * item['Harga Jual']
                    else:
                        st.session_state.keranjang.pop(i)
                    st.rerun()
                if c_plus.button("➕", key=f"mk_plus_{i}"):
                    item['Qty'] += 1
                    item['Subtotal'] = item['Qty'] * item['Harga Jual']
                    st.rerun()
                if c_del.button("❌", key=f"mk_del_{i}"):
                    st.session_state.keranjang.pop(i)
                    st.rerun()
            
            st.markdown("---")
            st.markdown(f"### Total Tagihan: Rp {total_belanja:,}")
            
            metode_bayar = st.selectbox("Metode Pembayaran:", ["Tunai (Cash)", "QRIS", "Transfer Bank"])
            
            if st.button("💳 Bayar Sekarang", type="primary", use_container_width=True):
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                transaksi_baru = {
                    "Waktu": waktu_sekarang,
                    "Item": st.session_state.keranjang.copy(),
                    "Total Omzet": total_belanja,
                    "Total Modal": sum([it['Modal'] * it['Qty'] for it in st.session_state.keranjang]),
                    "Metode": metode_bayar
                }
                st.session_state.transaksi.append(transaksi_baru)
                
                # Kurangi stok produk
                for item in st.session_state.keranjang:
                    st.session_state.produk.loc[st.session_state.produk['ID'] == item['ID'], 'Stok'] -= item['Qty']
                
                st.session_state.keranjang = []
                st.success("Pembayaran Berhasil! Struk tercatat di sistem.")
                st.balloons()

# ==========================================
# 2. KELOLA PRODUK & STOK
# ==========================================
elif menu == "📦 Kelola Produk & Stok":
    st.title("📦 Manajemen Inventaris & Menu")
    
    with st.expander("➕ Tambah Menu Produk Baru"):
        with st.form("form_produk"):
            nama_p = st.text_input("Nama Produk")
            kat_p = st.selectbox("Kategori", ["Makanan", "Minuman", "Snack", "Lainnya"])
            harga_jual = st.number_input("Harga Jual (Rp)", min_value=0, value=15000, step=1000)
            modal_p = st.number_input("Modal / HPP (Rp)", min_value=0, value=8000, step=500)
            stok_awal = st.number_input("Stok Awal", min_value=0, value=50)
            
            if st.form_submit_button("Simpan Produk", use_container_width=True) and nama_p:
                new_id = len(st.session_state.produk) + 1
                new_row = {"ID": new_id, "Nama": nama_p, "Kategori": kat_p, "Harga Jual": harga_jual, "Modal": modal_p, "Stok": stok_awal}
                st.session_state.produk = pd.concat([st.session_state.produk, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Produk '{nama_p}' berhasil ditambahkan!")
                st.rerun()

    st.subheader("Daftar Stok Produk Saat Ini")
    st.dataframe(st.session_state.produk, use_container_width=True)

# ==========================================
# 3. CATAT PENGELUARAN
# ==========================================
elif menu == "💸 Catat Pengeluaran":
    st.title("💸 Catat Pengeluaran Operasional")
    with st.form("form_pengeluaran"):
        ket_exp = st.text_input("Keterangan (Contoh: Belanja Bahan Baku / Gas)")
        kat_exp = st.selectbox("Kategori", ["Bahan Baku Utama", "Operasional", "Utilitas"])
        jumlah_exp = st.number_input("Total Biaya (Rp)", min_value=0, value=50000, step=5000)
        
        if st.form_submit_button("Simpan Pengeluaran", use_container_width=True) and ket_exp:
            st.session_state.pengeluaran.append({"Waktu": datetime.now().strftime("%Y-%m-%d %H:%M"), "Keterangan": ket_exp, "Kategori": kat_exp, "Jumlah": jumlah_exp})
            st.success("Pengeluaran berhasil dicatat!")
            st.rerun()
            
    st.subheader("Riwayat Pengeluaran")
    if st.session_state.pengeluaran:
        st.dataframe(pd.DataFrame(st.session_state.pengeluaran), use_container_width=True)

# ==========================================
# 4. LAPORAN & GRAFIK KEUANGAN
# ==========================================
elif menu == "📊 Laporan & Grafik":
    st.title("📊 Dashboard Laporan Keuangan")
    
    total_omzet = sum([t['Total Omzet'] for t in st.session_state.transaksi])
    total_modal_terjual = sum([t['Total Modal'] for t in st.session_state.transaksi])
    total_pengeluaran_op = sum([p['Jumlah'] for p in st.session_state.pengeluaran])
    laba_bersih = (total_omzet - total_modal_terjual) - total_pengeluaran_op
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Total Omzet", f"Rp {total_omzet:,}")
    c2.metric("💸 Total Pengeluaran", f"Rp {total_pengeluaran_op:,}")
    c3.metric("📈 Laba Bersih", f"Rp {laba_bersih:,}")
    
    st.subheader("Riwayat Transaksi Penjualan")
    if st.session_state.transaksi:
        st.dataframe(pd.DataFrame([{"Waktu": t["Waktu"], "Omzet": t["Total Omzet"], "Metode": t["Metode"]} for t in st.session_state.transaksi]), use_container_width=True)

# ==========================================
# 5. SETUP PROFIL TOKO
# ==========================================
elif menu == "⚙️ Setup Profil Toko":
    st.title("⚙️ Pengaturan Profil Bisnis")
    with st.form("form_profil"):
        nama_toko = st.text_input("Nama Toko / Usaha", value=st.session_state.profil["nama"])
        nama_owner = st.text_input("Nama Pemilik / Kasir", value=st.session_state.profil["pemilik"])
        
        if st.form_submit_button("Simpan Profil", use_container_width=True):
            st.session_state.profil["nama"] = nama_toko
            st.session_state.profil["pemilik"] = nama_owner
            st.success("Profil berhasil diperbarui!")
            st.rerun()
