import pandas as pd
import streamlit as st

# Data Arus Kas Terintegrasi
data_asli = {
    "Tanggal": [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-05",
        "2026-01-06",
        "2026-02-01",
        "2026-02-02",
        "2026-02-03",
        "2026-02-04",
        "2026-02-05",
        "2026-04-04",
        "2026-03-03",
        "2026-04-04",
        "2026-03-03",
        "2026-03-04",
        "2026-03-05",
        "2026-04-04",
        "2026-04-05",
        "2026-04-06",
        "2026-04-07",
        "2026-04-08",
        "2026-04-09",
        "2026-04-10",
        "2026-04-11",
        "2026-03-03",
        "2026-03-04",
        "2026-03-05",
        "2026-03-06",
        "2026-06-06",
        "2026-06-07",
        "2026-06-30",
        "2026-06-30",
        "2026-07-01",
        "2026-06-04",
        "2026-06-12",
        "2026-06-12",
        "2026-06-18",
        "2026-06-18",
        "2026-07-01",
        "2026-07-01",
        "2026-07-01",
        "2026-08-01",
        "2026-08-01",
    ],
    "Keterangan": [
        "Saldo per 9 April",
        "Rini",
        "Aldila",
        "Agal",
        "Pulsa",
        "Pulsa",
        "Bu Jo",
        "Bu YR",
        "Rini",
        "Bayar Pak Agus",
        "Pulsa",
        "Bu YR",
        "Almira",
        "Bu Fifith",
        "Bayar Pak Agus",
        "Pulsa",
        "Agal",
        "Tisu",
        "Bayar Pak Agus",
        "Tisu",
        "Ery",
        "Pak Budi",
        "Pulsa IGD",
        "Almira",
        "Pulsa Bangsal",
        "Pulsa",
        "Pulsa",
        "Bayar Pak agus",
        "Tisu",
        "Dr Budi",
        "Bayar Pak agus",
        "pulsa bangsal",
        "rini",
        "fitria",
        "bu ika",
        "pak him",
        "bu vera",
        "amira",
        "yola",
        "aldila",
        "pulsa bangsal",
        "loundry pak agus",
        "loundry pak agus",
        "pulsa bangsal",
    ],
    "Pemasukan": [
        420000,
        50000,
        50000,
        50000,
        0,
        0,
        1000000,
        400000,
        50000,
        0,
        0,
        300000,
        150000,
        150000,
        0,
        0,
        50000,
        0,
        0,
        0,
        50000,
        200000,
        0,
        100000,
        0,
        0,
        0,
        0,
        0,
        100000,
        0,
        0,
        150000,
        150000,
        300000,
        300000,
        300000,
        100000,
        120000,
        50000,
        0,
        0,
        0,
        0,
    ],
    "Pengeluaran": [
        0,
        0,
        0,
        0,
        50000,
        50000,
        0,
        0,
        0,
        200000,
        50000,
        0,
        0,
        0,
        200000,
        50000,
        0,
        20000,
        200000,
        10000,
        0,
        0,
        50000,
        0,
        50000,
        25000,
        25000,
        200000,
        40000,
        0,
        200000,
        50000,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        50000,
        200000,
        200000,
        50000,
    ],
}

df_bersih = pd.DataFrame(data_asli)

st.set_page_config(
    page_title="Aplikasi Arus Kas", page_icon="💰", layout="centered"
)
st.image(
    "https://soerojohospital.go.id/img/rawat-jalan/soerojo_hospital.png",
    width="stretch",
)
st.title("Kas Dokter Umum Soerojo Hospital")

if "data_kas" not in st.session_state:
  st.session_state.data_kas = df_bersih

# Form Input Transaksi Baru di Sidebar
st.sidebar.header("➕ Tambah Transaksi")
with st.sidebar.form("form_tambah"):
  tgl = st.date_input("Tanggal")
  jenis = st.selectbox("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
  ket = st.text_input("Keterangan")
  nominal = st.number_input("Jumlah (Rp)", min_value=0, step=5000)

  submit = st.form_submit_button("Simpan Data")

  if submit:
    masuk = nominal if jenis == "Pemasukan" else 0
    keluar = nominal if jenis == "Pengeluaran" else 0

    baris_baru = pd.DataFrame({
        "Tanggal": [str(tgl)],
        "Keterangan": [ket],
        "Pemasukan": [masuk],
        "Pengeluaran": [keluar],
    })

    st.session_state.data_kas = pd.concat(
        [st.session_state.data_kas, baris_baru], ignore_index=True
    )
    st.sidebar.success("Transaksi berhasil ditambahkan!")

# --- FITUR HAPUS TRANSAKSI TERAKHIR / BERDASARKAN NOMOR BARIS ---
st.sidebar.markdown("---")
st.sidebar.header("❌ Koreksi / Hapus Transaksi")

if len(st.session_state.data_kas) > 0:
  # Pilihan nomor baris data yang ingin dihapus
  indeks_hapus = st.sidebar.number_input(
      "Nomor Baris (Index) yang ingin dihapus",
      min_value=0,
      max_value=len(st.session_state.data_kas) - 1,
      step=1,
  )

  if st.sidebar.button("Hapus Baris Terpilih"):
    st.session_state.data_kas = (
        st.session_state.data_kas.drop(indeks_hapus)
        .reset_index(drop=True)
    )
    st.sidebar.success(f"Baris ke-{indeks_hapus} berhasil dihapus!")
    st.rerun()  # Memuat ulang halaman agar tabel langsung terupdate
# Ringkasan Saldo Utama
df = st.session_state.data_kas
total_masuk = df["Pemasukan"].sum()
total_keluar = df["Pengeluaran"].sum()
saldo_akhir = total_masuk - total_keluar

c1, c2, c3 = st.columns(3)
c1.metric("Total Pemasukan", f"Rp {total_masuk:,.0f}")
c2.metric("Total Pengeluaran", f"Rp {total_keluar:,.0f}")
c3.metric("SALDO AKHIR", f"Rp {saldo_akhir:,.0f}")

st.markdown("---")

st.subheader("📋 Riwayat Arus Kas")
st.dataframe(df, width="stretch")

st.download_button(
    label="📥 Unduh Data ke CSV",
)
