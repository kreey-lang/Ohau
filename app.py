import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman
st.set_page_config(
    page_title="Ohau AI - POS & Pembukuan UMKM", 
    page_icon="⚡", 
    layout="wide"
)

# Inisialisasi Session State untuk database memori sementara
if "profil" not in st.session_state:
    st.session_state.profil = {"nama": "Kafe Ohau", "pemilik": "Owner", "kategori": "Kafe / Resto"}

if "produk" not in st.session_state:
    st.session_state.produk = pd.DataFrame([
        {"ID": 1, "Nama": "Kopi Susu Gula Aren", "Kategori": "Minuman", "Harga Jual": 18000, "Modal": 10000, "Stok": 50},
        {"ID": 2, "Nama": "Nasi Goreng Spesial", "Kategori": "Makanan", "Harga Jual": 25000, "Modal": 14000, "Stok": 30},
        {"ID": 3, "Nama": "Es Teh Manis", "Kategori": "Minuman", "Harga Jual": 5000, "Modal": 2000, "Stok": 100}
    ])

if "transaksi" not in st.session_state:
    st.session_state.transaksi = []

if "pengeluaran" not in st.session_state:
    st.session_state.pengeluaran = []

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

# Sidebar Navigasi Utama
st.sidebar.title("⚡ Ohau AI POS")
st.sidebar.write(f"Toko: **{st.session_state.profil['nama']}**")

menu = st.sidebar.radio(
    "Pilih Menu:", 
    ["🛒 Kasir (POS)", "📦 Kelola Produk & Stok", "💸 Catat Pengeluaran", "📊 Laporan & Grafik", "⚙️ Setup Profil Toko"]
)

# ==========================================
# 1. MENU KASIR (POS)
# ==========================================
if menu == "🛒 Kasir (POS)":
    st.title("🛒 Kasir & Transaksi Penjualan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Daftar Menu Tersedia")
        df_prod = st.session_state.produk
        
        if df_prod.empty:
            st.warning("Belum ada produk. Tambahkan produk di menu Kelola Produk.")
        else:
            for index, row in df_prod.iterrows():
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.write(f"**{row['Nama']}**")
                c2.write(f"Rp {row['Harga Jual']:,}")
                c3.write(f"Stok: {row['Stok']}")
                
                qty_input = c4.number_input("Qty", min_value=1, max_value=int(row['Stok']) if row['Stok'] > 0 else 1, value=1, key=f"qty_{row['ID']}")
                
                if c4.button("Tambah", key=f"add_{row['ID']}"):
                    if row['Stok'] <= 0:
                        st.error("Stok habis, Bro!")
                    else:
                        item_ada = False
                        for item in st.session_state.keranjang:
                            if item['ID'] == row['ID']:
                                item['Qty'] += qty_input
                                item['Subtotal'] = item['Qty'] * item['Harga Jual']
                                item_ada = True
                                break
                        if not item_ada:
                            st.session_state.keranjang.append({
                                "ID": row['ID'],
                                "Nama": row['Nama'],
                                "Harga Jual": row['Harga Jual'],
                                "Modal": row['Modal'],
                                "Qty": qty_input,
                                "Subtotal": qty_input * row['Harga Jual']
                            })
                        st.success(f"{row['Nama']} ditambahkan ke keranjang!")
                        st.rerun()

    with col2:
        st.subheader("🛍️ Keranjang Belanja")
        if not st.session_state.keranjang:
            st.info("Keranjang masih kosong.")
        else:
            total_belanja = 0
            for i, item in enumerate(st.session_state.keranjang):
                st.write(f"**{item['Nama']}** (x{item['Qty']})")
                st.write(f"Rp {item['Subtotal']:,}")
                total_belanja += item['Subtotal']
                if st.button("Hapus", key=f"del_cart_{i}"):
                    st.session_state.keranjang.pop(i)
                    st.rerun()
            
            st.markdown("---")
            st.markdown(f"### Total Tagihan: Rp {total_belanja:,}")
            
            metode_bayar = st.selectbox("Metode Pembayaran:", ["Tunai (Cash)", "QRIS", "Transfer Bank"])
            
            if st.button("Selesaikan Pembayaran & Cetak Struk", type="primary"):
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                transaksi_baru = {
                    "Waktu": waktu_sekarang,
                    "Item": st.session_state.keranjang.copy(),
                    "Total Omzet": total_belanja,
                    "Total Modal": sum([it['Modal'] * it['Qty'] for it in st.session_state.keranjang]),
                    "Metode": metode_bayar
                }
                st.session_state.transaksi.append(transaksi_baru)
                
                for item in st.session_state.keranjang:
                    st.session_state.produk.loc[st.session_state.produk['ID'] == item['ID'], 'Stok'] -= item['Qty']
                
                st.session_state.keranjang = []
                st.success("Transaksi Berhasil Dicatat ke Pembukuan! 🎉")
                st.balloons()

# ==========================================
# 2. KELOLA PRODUK & STOK
# ==========================================
elif menu == "📦 Kelola Produk & Stok":
    st.title("📦 Manajemen Produk, Stok & Harga")
    
    with st.form("form_produk"):
        st.subheader("Tambah Menu / Produk Baru")
        nama_p = st.text_input("Nama Produk (Contoh: Es Kopi Susu)")
        kat_p = st.selectbox("Kategori", ["Minuman", "Makanan", "Snack", "Lainnya"])
        harga_jual = st.number_input("Harga Jual ke Pelanggan (Rp)", min_value=0, value=10000, step=1000)
        modal_p = st.number_input("Modal / HPP per Porsi (Rp)", min_value=0, value=5000, step=500)
        stok_awal = st.number_input("Stok Awal", min_value=0, value=50)
        
        submitted = st.form_submit_button("Simpan Produk Baru")
        if submitted and nama_p:
            new_id = len(st.session_state.produk) + 1
            new_row = {"ID": new_id, "Nama": nama_p, "Kategori": kat_p, "Harga Jual": harga_jual, "Modal": modal_p, "Stok": stok_awal}
            st.session_state.produk = pd.concat([st.session_state.produk, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Produk '{nama_p}' berhasil ditambahkan!")
            st.rerun()

    st.subheader("Daftar Produk & Stok Saat Ini")
    st.dataframe(st.session_state.produk, use_container_width=True)
    
    st.subheader("⚠️ Peringatan Stok Menipis")
    stok_tipis = st.session_state.produk[st.session_state.produk['Stok'] <= 5]
    if not stok_tipis.empty:
        st.error("Produk berikut hampir habis, segera restock!")
        st.dataframe(stok_tipis, use_container_width=True)
    else:
        st.success("Aman! Semua stok produk masih mencukupi.")

# ==========================================
# 3. CATAT PENGELUARAN
# ==========================================
elif menu == "💸 Catat Pengeluaran":
    st.title("💸 Pencatatan Pengeluaran Operasional")
    st.write("Catat biaya operasional harian seperti belanja gas, bahan baku, listrik, dll.")
    
    with st.form("form_pengeluaran"):
        ket_exp = st.text_input("Keterangan Pengeluaran (Contoh: Beli Gas 3kg & Tepung)")
        kat_exp = st.selectbox("Kategori Pengeluaran", ["Bahan Baku Utama", "Operasional Bar & Dapur", "Utilitas & Lainnya"])
        jumlah_exp = st.number_input("Total Biaya (Rp)", min_value=0, value=50000, step=5000)
        
        btn_exp = st.form_submit_button("Simpan Pengeluaran")
        if btn_exp and ket_exp:
            waktu_exp = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.session_state.pengeluaran.append({
                "Waktu": waktu_exp,
                "Keterangan": ket_exp,
                "Kategori": kat_exp,
                "Jumlah": jumlah_exp
            })
            st.success("Pengeluaran berhasil dicatat!")
            st.rerun()
            
    st.subheader("Riwayat Pengeluaran")
    if st.session_state.pengeluaran:
        st.dataframe(pd.DataFrame(st.session_state.pengeluaran), use_container_width=True)
    else:
        st.info("Belum ada pengeluaran tercatat.")

# ==========================================
# 4. LAPORAN & GRAFIK KEUANGAN
# ==========================================
elif menu == "📊 Laporan & Grafik":
    st.title("📊 Dashboard Laporan & Grafik Keuangan")
    
    total_omzet = sum([t['Total Omzet'] for t in st.session_state.transaksi])
    total_modal_terjual = sum([t['Total Modal'] for t in st.session_state.transaksi])
    total_pengeluaran_op = sum([p['Jumlah'] for p in st.session_state.pengeluaran])
    
    laba_kotor = total_omzet - total_modal_terjual
    laba_bersih = laba_kotor - total_pengeluaran_op
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Omzet", f"Rp {total_omzet:,}")
    col2.metric("📦 HPP / Modal Terjual", f"Rp {total_modal_terjual:,}")
    col3.metric("💸 Total Pengeluaran", f"Rp {total_pengeluaran_op:,}")
    col4.metric("📈 Laba Bersih", f"Rp {laba_bersih:,}")
    
    st.markdown("---")
    
    st.subheader("📋 Ringkasan Riwayat Transaksi Kasir")
    if st.session_state.transaksi:
        df_trx_summary = pd.DataFrame([{
            "Waktu": t["Waktu"],
            "Omzet": t["Total Omzet"],
            "Metode Bayar": t["Metode"]
        } for t in st.session_state.transaksi])
        st.dataframe(df_trx_summary, use_container_width=True)
    else:
        st.info("Belum ada transaksi penjualan tercatat hari ini.")
        
    st.subheader("💡 Smart Insights (Analisis Ohau AI)")
    if total_omzet > 0:
        st.success(f"Mantap, Bro! Usaha **{st.session_state.profil['nama']}** hari ini mencatat omzet sehat sebesar Rp {total_omzet:,}. Pertahankan stok menu favorit agar pelanggan tidak kecewa!")
    else:
        st.info("Belum cukup data transaksi untuk dianalisis. Yuk mulai jualan dan catat transaksi di menu Kasir!")

# ==========================================
# 5. SETUP PROFIL TOKO
# ==========================================
elif menu == "⚙️ Setup Profil Toko":
    st.title("⚙️ Pengaturan Profil Bisnis & Toko")
    
    with st.form("form_profil"):
        nama_toko = st.text_input("Nama Bisnis / Toko", value=st.session_state.profil["nama"])
        nama_owner = st.text_input("Nama Pemilik", value=st.session_state.profil["pemilik"])
        kat_toko = st.text_input("Kategori Usaha", value=st.session_state.profil["kategori"])
        
        save_prof = st.form_submit_button("Simpan Profil")
        if save_prof:
            st.session_state.profil = {"nama": nama_toko, "pemilik": nama_owner, "kategori": kat_toko}
            st.success("Profil toko berhasil diperbarui!")
            st.rerun()
                                
