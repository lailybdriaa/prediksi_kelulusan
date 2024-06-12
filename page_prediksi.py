import streamlit as st
import pandas as pd
import joblib
import sqlite3
from datetime import datetime

# Load model dan scaler
best_model = joblib.load('models/best_model.pkl')
scaler = joblib.load('models/scaler.pkl')
pca = joblib.load('models/pca.pkl')

# Koneksi ke database SQLite
conn = sqlite3.connect('data/data_mahasiswa.db', check_same_thread=False)
c = conn.cursor()

def page_form():
    st.header("Prediksi Kelulusan")
        
    with st.form("student_form"):
        # Input fields
        col0, col1, col2 = st.columns(3)
        nama = col0.text_input("Nama")
        nim = col0.text_input("NIM")
        st.markdown("---")
        ips_semesters = []
        for i in range(1, 5):
            ips = col1.number_input(f"IPS Semester {i}", min_value=0.0, max_value=4.0, step=1.00)
            ips_semesters.append(ips)
        
        tagihan_semesters = []
        for i in range(1, 5):
            tagihan = col2.number_input(f"Tagihan Semester {i}", min_value=0, step=1000000)
            tagihan_semesters.append(tagihan)
        
        kehadiran = col0.number_input("Kehadiran (%)", min_value=0, max_value=100, step=10)
        
        # Submit button
        submit_button = st.form_submit_button(label="Submit")

    # Display submitted data
    if submit_button:
        date = datetime.now().strftime("%Y-%m-%d")
        # Prediksi kelulusan
        tagihan_1 = 1 if tagihan_semesters[0] > 0 else 0
        tagihan_2 = 1 if tagihan_semesters[1] > 0 else 0
        tagihan_3 = 1 if tagihan_semesters[2] > 0 else 0
        tagihan_4 = 1 if tagihan_semesters[3] > 0 else 0

        data_baru = {
            'IPS 1': [ips_semesters[0]],
            'IPS 2': [ips_semesters[1]],
            'IPS 3': [ips_semesters[2]],
            'IPS 4': [ips_semesters[3]],
            'Tagihan 1': [tagihan_1],
            'Tagihan 2': [tagihan_2],
            'Tagihan 3': [tagihan_3],
            'Tagihan 4': [tagihan_4],
            'Kehadiran': [kehadiran]
        }

        data_baru_df = pd.DataFrame(data_baru)

        data_baru_scaled = scaler.transform(data_baru_df)

        data_baru_pca = pca.transform(data_baru_scaled)

        prediksi = best_model.predict(data_baru_pca)

        status_kelulusan = "LULUS" if prediksi[0] == 1 else "DROPOUT"

        st.write("Hasil prediksi :")
        if status_kelulusan == "LULUS":
            st.success(status_kelulusan)
        else:
            st.error(status_kelulusan)

        # Convert to DataFrame for display
        df = pd.DataFrame({
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
        
        st.write("Tabel Data Mahasiswa:")
        st.dataframe(df)
        # Masukkan data ke dalam tabel
        c.execute('''
        INSERT INTO mahasiswa (nama, nim, ips_semester_1, ips_semester_2, ips_semester_3, ips_semester_4,
                                tagihan_semester_1, tagihan_semester_2, tagihan_semester_3, tagihan_semester_4, kehadiran, kelulusan, tanggal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nama, nim, ips_semesters[0], ips_semesters[1], ips_semesters[2], ips_semesters[3],
                tagihan_semesters[0], tagihan_semesters[1], tagihan_semesters[2], tagihan_semesters[3], kehadiran, status_kelulusan, date))
        
        conn.commit()
        st.success("Data berhasil disimpan ke dalam database!")
