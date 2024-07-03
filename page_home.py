import streamlit as st  # Import Streamlit untuk membuat aplikasi web interaktif
import pandas as pd  # Import Pandas untuk mengelola data dalam bentuk DataFrame
import sqlite3  # Import SQLite3 untuk berinteraksi dengan database SQLite
import plotly.express as px  # Import Plotly Express untuk membuat visualisasi data

# Fungsi untuk mendapatkan koneksi ke database
def get_db_connection():
    conn = sqlite3.connect('data/data_mahasiswa.db')  # Membuka koneksi ke database SQLite
    return conn  # Mengembalikan objek koneksi

# Fungsi untuk mengambil data kelulusan dari database
def get_graduation_data():
    conn = get_db_connection()  # Mendapatkan koneksi ke database
    query = 'SELECT kelulusan FROM mahasiswa'  # Query SQL untuk mengambil kolom 'kelulusan' dari tabel 'mahasiswa'
    df = pd.read_sql_query(query, conn)  # Menjalankan query dan menyimpan hasilnya dalam DataFrame
    conn.close()  # Menutup koneksi ke database
    return df  # Mengembalikan DataFrame yang berisi data kelulusan

# Fungsi untuk membuat grafik pie chart dari data kelulusan
def plot_graduation_chart(df):
    graduation_counts = df['kelulusan'].value_counts(normalize=True) * 100  # Menghitung persentase tiap status kelulusan
    labels = graduation_counts.index  # Mendapatkan label dari hasil perhitungan
    values = graduation_counts.values  # Mendapatkan nilai dari hasil perhitungan

    # Membuat pie chart menggunakan Plotly Express
    fig = px.pie(
        names=labels,  # Menetapkan label pada pie chart
        values=values,  # Menetapkan nilai pada pie chart
        title='Persentase Prediksi Kelulusan dan Dropout',  # Judul pie chart
        labels={'labels': 'Status', 'values': 'Persentase'}  # Label untuk chart
    )
    return fig  # Mengembalikan objek figure dari pie chart

# Fungsi untuk menampilkan halaman utama
def page_home():
    # Menambahkan CSS untuk mempercantik tampilan
    st.markdown(
        """
        <style>
            .header-text {
                font-size: 36px;
                color: #333333;
                text-align: center;
                margin-bottom: 20px;
            }

            .subheader-text {
                font-size: 24px;
                color: #666666;
                text-align: center;
                margin-bottom: 30px;
            }

            .university-logo {
                display: block;
                margin: 0 auto;
                max-width: 100%;
                height: auto;
                text-align: center;
                margin-top: 100px;
            }

            .footer-text {
                font-size: 18px;
                color: #999999;
                text-align: center;
                margin-top: 30px;
            }
        </style>
        """
        , unsafe_allow_html=True
    )

    # Menambahkan header dan subheader
    st.markdown('<p class="header-text">Selamat datang di Aplikasi Prediksi Kelulusan Mahasiswa</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">Universitas Darma Persada</p>', unsafe_allow_html=True)
    
    # Menampilkan logo universitas dari link discord
    st.markdown('<center> <img width="30%" src="https://i.imgur.com/3eTKJe2.png"> </center>', unsafe_allow_html=True)
    
    st.divider()  # Menambahkan garis pemisah warna abu2
    

    # Mengambil dan menampilkan data kelulusan
    df = get_graduation_data()  # Mengambil data kelulusan dari database
    if not df.empty:  # Jika DataFrame tidak kosong
        fig = plot_graduation_chart(df)  # Membuat pie chart dari data kelulusan
        st.plotly_chart(fig)  # Menampilkan pie chart di Streamlit
    else:
        st.write("Belum ada data yang tersimpan.")  # Menampilkan pesan jika tidak ada data

    st.divider()  # Menambahkan garis pemisah lagi
    st.markdown('<p class="footer-text">© 2024 Universitas Darma Persada. All rights reserved.</p>', unsafe_allow_html=True)  # Menambahkan footer
