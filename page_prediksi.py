import streamlit as st  # Memanggil library Streamlit untuk membuat aplikasi web
import pandas as pd  # Memanggil library Pandas untuk mengelola data dalam bentuk DataFrame
import joblib  # Memanggil library joblib untuk memuat model dan scaler yang telah disimpan
import sqlite3  # Memanggil library sqlite3 untuk berinteraksi dengan database SQLite
from datetime import datetime  # Memanggil modul datetime untuk mendapatkan waktu saat ini

# Memuat model dan scaler yang telah disimpan
best_model = joblib.load('models/best_model.pkl')  # Memuat model terbaik yang telah disimpan
scaler = joblib.load('models/scaler.pkl')  # Memuat scaler untuk normalisasi data
pca = joblib.load('models/pca.pkl')  # Memuat PCA untuk reduksi dimensi

# Koneksi ke database SQLite
conn = sqlite3.connect('data/data_mahasiswa.db', check_same_thread=False)  # Membuka koneksi ke database SQLite
c = conn.cursor()  # Membuat cursor untuk eksekusi query SQL

def page_form():
    st.header("Prediksi Kelulusan Mahasiswa")  # Menampilkan header pada halaman web

    with st.form("student_form"):  # Membuat form input
        # Input fields
        col0, col1, col2 = st.columns(3)  # Membuat 3 kolom
        nama = col0.text_input("Nama")  # Input untuk nama mahasiswa
        nim = col0.text_input("NIM")  # Input untuk NIM mahasiswa
        kehadiran = col0.number_input("Kehadiran (%)", min_value=0, max_value=100, step=5)  # Input untuk persentase kehadiran dengan selisih selisih 5 angka
        tanggal = col0.date_input("Tanggal")

        st.markdown("---")  # Menampilkan garis pemisah
        ips_semesters = []
        for i in range(1, 5):  # Looping untuk input IPS setiap semester
            ips = col1.number_input(f"IPS Semester {i}", min_value=0.0, max_value=4.0, step=0.05)  # Input IPS dengan selisih 0,05 angka
            ips_semesters.append(ips)  # Menyimpan IPS ke dalam list
        
        tagihan_semesters = []
        for i in range(1, 5):  # Looping untuk input tagihan setiap semester
            tagihan = col2.number_input(f"Tagihan Semester {i}", min_value=0, step=5000000)  # Input tagihan
            tagihan_semesters.append(tagihan)  # Menyimpan tagihan ke dalam list
            

        # Tombol submit
        submit_button = st.form_submit_button(label="Submit")  # Tombol untuk submit form

    # Menampilkan data yang telah di-submit
    if submit_button:
        date = datetime.now().strftime("%Y-%m-%d")  # Mendapatkan tanggal saat ini dalam format YYYY-MM-DD

        # Menyiapkan data untuk prediksi kelulusan
        tagihan_1 = 1 if tagihan_semesters[0] > 0 else 0  # Mengubah tagihan menjadi 0 atau 1
        tagihan_2 = 1 if tagihan_semesters[1] > 0 else 0
        tagihan_3 = 1 if tagihan_semesters[2] > 0 else 0
        tagihan_4 = 1 if tagihan_semesters[3] > 0 else 0

        data_baru = {
            'IPS 1': [ips_semesters[0]],  # Menyiapkan data IPS untuk prediksi
            'IPS 2': [ips_semesters[1]],
            'IPS 3': [ips_semesters[2]],
            'IPS 4': [ips_semesters[3]],
            'Tagihan 1': [tagihan_1],
            'Tagihan 2': [tagihan_2],
            'Tagihan 3': [tagihan_3],
            'Tagihan 4': [tagihan_4],
            'Kehadiran': [kehadiran]
        }

        data_baru_df = pd.DataFrame(data_baru)  # Membuat DataFrame dari data baru 

        data_baru_scaled = scaler.transform(data_baru_df)  # Menskalakan data menggunakan scaler

        data_baru_pca = pca.transform(data_baru_scaled)  # Mengubah data dengan PCA

        prediksi = best_model.predict(data_baru_pca)  # Melakukan prediksi kelulusan dengan model

        status_kelulusan = "LULUS" if prediksi[0] == 1 else "DROPOUT"  # Menentukan status kelulusan berdasarkan prediksi (kalo prediksi 1 maka lulus selain 1 do)

        st.write("Hasil prediksi :")  # Menampilkan hasil prediksi
        if status_kelulusan == "LULUS":
            st.success(status_kelulusan)  # Menampilkan pesan sukses jika lulus dengan warna hijau
        else:
            st.error(status_kelulusan)  # Menampilkan pesan error jika dropout dengan warna merah

        # Membuat DataFrame untuk menampilkan data yang di-submit
        df = pd.DataFrame({ #df untuk membuat data baru 
            "Tanggal": [date],
            "Nama": [nama],
            "NIM": [nim],
            "IPS Semester 1": [ips_semesters[0]],
            "IPS Semester 2": [ips_semesters[1]],
            "IPS Semester 3": [ips_semesters[2]],
            "IPS Semester 4": [ips_semesters[3]],
            "Tagihan Semester 1": [tagihan_semesters[0]],
            "Tagihan Semester 2": [tagihan_semesters[1]],
            "Tagihan Semester 3": [tagihan_semesters[2]],
            "Tagihan Semester 4": [tagihan_semesters[3]],
            "Kehadiran (%)": [kehadiran],
            "Kelulusan": [status_kelulusan]
        })
        
        st.write("Tabel Data Mahasiswa:")  # Menampilkan tabel data mahasiswa
        st.dataframe(df)  # Menampilkan DataFrame sebagai tabel berdasarkan df yang isinya data baru untuk prediksi

        # Memasukkan data ke dalam tabel database mahasiswa
        c.execute('''
        INSERT INTO mahasiswa (nama, nim, ips_semester_1, ips_semester_2, ips_semester_3, ips_semester_4,
                                tagihan_semester_1, tagihan_semester_2, tagihan_semester_3, tagihan_semester_4, kehadiran, kelulusan, tanggal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        ''', (nama, nim, ips_semesters[0], ips_semesters[1], ips_semesters[2], ips_semesters[3],
                tagihan_semesters[0], tagihan_semesters[1], tagihan_semesters[2], tagihan_semesters[3], kehadiran, status_kelulusan, date))
        #tanda tanya yang disesuaikan dengan banyaknya data insert yang ingin dimasukan ke database
        conn.commit()  # Menyimpan perubahan ke database
        st.success("Data berhasil disimpan ke dalam database!")  # Menampilkan pesan sukses