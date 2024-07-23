import streamlit as st  # Mengimpor library Streamlit untuk membuat aplikasi web
import pandas as pd  # Mengimpor library Pandas untuk mengelola data dalam bentuk DataFrame
import joblib  # Mengimpor library Joblib untuk memuat model yang sudah dilatih
import sqlite3  # Mengimpor library SQLite3 untuk berinteraksi dengan database SQLite
from datetime import datetime  # Mengimpor modul datetime untuk mendapatkan waktu saat ini

# Memuat model, scaler, dan pca
best_model = joblib.load('models/best_model.pkl')  # Memuat model terbaik
scaler = joblib.load('models/scaler.pkl')  # Memuat scaler untuk normalisasi data
pca = joblib.load('models/pca.pkl')  # Memuat PCA untuk reduksi dimensi

# Koneksi ke database SQLite
conn = sqlite3.connect('data/data_mahasiswa.db', check_same_thread=False)  # Membuka koneksi ke database SQLite
c = conn.cursor()  # Membuat cursor untuk eksekusi query SQL

def page_excel():
    st.header("Prediksi Kelulusan dari File Excel")  # Menampilkan header halaman

    uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"])  # Membuat uploader file untuk mengunggah file Excel
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # Periksa apakah kolom 'NIM' ada dalam DataFrame
        if 'NIM' not in df.columns:
            st.error("Kolom 'NIM' tidak ditemukan di file Excel.")
            return

        # Ubah tipe data kolom NIM menjadi string
        df['NIM'] = df['NIM'].astype(str)

        st.write("Data Mahasiswa:")  # Menampilkan dataframe dalam bentuk tabel
        st.dataframe(df)

        if st.button("Prediksi"):  # Membuat tombol untuk melakukan prediksi
            # Mengubah nilai tagihan > 0 menjadi 1
            df[['Tagihan 1', 'Tagihan 2', 'Tagihan 3', 'Tagihan 4']] = df[['Tagihan 1', 'Tagihan 2', 'Tagihan 3', 'Tagihan 4']].applymap(lambda x: 1 if x > 0 else 0)

            # Asumsi kolom sesuai dengan urutan yang dibutuhkan
            required_columns = ['IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'Tagihan 1', 'Tagihan 2', 'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Kolom-kolom berikut tidak ditemukan di DataFrame: {missing_columns}")
            else:
                # Ganti nama kolom 'Kehadiran (%)' menjadi 'Kehadiran'
                df.rename(columns={'Kehadiran (%)': 'Kehadiran'}, inplace=True)
                data_baru_df = df[['IPS 1', 'IPS 2', 'IPS 3', 'IPS 4', 'Tagihan 1', 'Tagihan 2', 'Tagihan 3', 'Tagihan 4', 'Kehadiran']]

                # Transformasi data menggunakan scaler dan PCA
                data_baru_scaled = scaler.transform(data_baru_df)  # Mengskala data
                data_baru_pca = pca.transform(data_baru_scaled)  # Menerapkan PCA pada data
                prediksi = best_model.predict(data_baru_pca)  # Melakukan prediksi menggunakan model

                df['Kelulusan'] = ["LULUS" if p == 1 else "DROPOUT" for p in prediksi]  # Menentukan status kelulusan berdasarkan prediksi
                st.write("Hasil Prediksi:")  # Menampilkan hasil prediksi
                st.dataframe(df)  # Menampilkan DataFrame sebagai tabel

                date = datetime.now().strftime("%Y-%m-%d")
                # Simpan ke database
                for idx, row in df.iterrows():
                    c.execute('''
                    INSERT INTO mahasiswa (nama, tanggal, nim, ips_semester_1, ips_semester_2, ips_semester_3, ips_semester_4,
                                           tagihan_semester_1, tagihan_semester_2, tagihan_semester_3, tagihan_semester_4, kehadiran, kelulusan)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (row['Nama'], date, row['NIM'], row['IPS 1'], row['IPS 2'], row['IPS 3'],
                          row['IPS 4'], row['Tagihan 1'], row['Tagihan 2'], row['Tagihan 3'],
                          row['Tagihan 4'], row['Kehadiran'], row['Kelulusan']))
                conn.commit()  # Menyimpan perubahan ke database
                st.success("Data berhasil disimpan ke dalam database!")  # Menampilkan pesan sukses
