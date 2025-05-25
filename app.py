import streamlit as st
import pandas as pd
import datetime
import os

# Path ke file Excel
EXCEL_PATH = "Laporan_Keuangan_Usaha.xlsx"

# Fungsi untuk baca sheet Excel
def load_sheet(sheet_name):
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    except:
        df = pd.DataFrame()
    return df

# Fungsi untuk simpan sheet Excel
def save_sheet(sheet_name, df):
    with pd.ExcelWriter(EXCEL_PATH, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

# Sidebar navigasi
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Input Penjualan", "Input Pengeluaran", "Input Pelanggan", "Ringkasan"])

if page == "Input Penjualan":
    st.header("Input Data Penjualan")
    tanggal = st.date_input("Tanggal", datetime.date.today())
    menu = st.text_input("Nama Menu")
    jumlah = st.number_input("Jumlah Terjual", min_value=0)
    harga = st.number_input("Harga Satuan", min_value=0.0)
    catatan = st.text_input("Catatan Khusus")

    if st.button("Simpan Penjualan"):
        total = jumlah * harga
        df = load_sheet("Input Penjualan")
        new_row = {"Tanggal": tanggal, "Nama Menu": menu, "Jumlah Terjual": jumlah,
                   "Harga Satuan": harga, "Total Pendapatan": total, "Catatan Khusus": catatan}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_sheet("Input Penjualan", df)
        st.success("Data penjualan berhasil disimpan!")

elif page == "Input Pengeluaran":
    st.header("Input Data Pengeluaran")
    tanggal = st.date_input("Tanggal", datetime.date.today())
    kategori = st.selectbox("Kategori", ["Bahan Baku", "Gaji", "Listrik/Air/Gas", "Perawatan", "Lainnya"])
    jumlah = st.number_input("Jumlah (Rp)", min_value=0.0)
    keterangan = st.text_input("Keterangan")

    if st.button("Simpan Pengeluaran"):
        df = load_sheet("Input Pengeluaran")
        new_row = {"Tanggal": tanggal, "Kategori Pengeluaran": kategori,
                   "Jumlah": jumlah, "Keterangan": keterangan}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_sheet("Input Pengeluaran", df)
        st.success("Data pengeluaran berhasil disimpan!")

elif page == "Input Pelanggan":
    st.header("Input Jumlah Pelanggan")
    tanggal = st.date_input("Tanggal", datetime.date.today())
    jumlah = st.number_input("Jumlah Pelanggan", min_value=0)

    if st.button("Simpan Data Pelanggan"):
        df = load_sheet("Input Pelanggan")
        new_row = {"Tanggal": tanggal, "Jumlah Pelanggan": jumlah}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_sheet("Input Pelanggan", df)
        st.success("Data pelanggan berhasil disimpan!")

elif page == "Ringkasan":
    st.header("Ringkasan Keuangan dan Pelanggan")

    df_penjualan = load_sheet("Input Penjualan")
    df_pengeluaran = load_sheet("Input Pengeluaran")
    df_pelanggan = load_sheet("Input Pelanggan")

    total_pendapatan = df_penjualan["Total Pendapatan"].sum() if not df_penjualan.empty else 0
    total_pengeluaran = df_pengeluaran["Jumlah"].sum() if not df_pengeluaran.empty else 0
    laba_rugi = total_pendapatan - total_pengeluaran

    total_pelanggan = df_pelanggan["Jumlah Pelanggan"].sum() if not df_pelanggan.empty else 0
    hari_aktif = df_pelanggan["Tanggal"].nunique() if not df_pelanggan.empty else 0
    rata_pelanggan = total_pelanggan / hari_aktif if hari_aktif > 0 else 0
    rata_pemasukan = total_pendapatan / hari_aktif if hari_aktif > 0 else 0

    st.subheader("Pendapatan & Pengeluaran")
    st.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
    st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    st.metric("Laba/Rugi Bersih", f"Rp {laba_rugi:,.0f}")

    st.subheader("Pelanggan")
    st.metric("Jumlah Hari Aktif", hari_aktif)
    st.metric("Total Pelanggan", int(total_pelanggan))
    st.metric("Rata-rata Pelanggan per Hari", f"{rata_pelanggan:.2f}")
    st.metric("Rata-rata Pendapatan per Hari", f"Rp {rata_pemasukan:,.0f}")
