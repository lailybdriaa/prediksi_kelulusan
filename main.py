import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import sqlite3
import joblib

# Load model dan scaler
best_model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca.pkl')

# Koneksi ke database SQLite
conn = sqlite3.connect('data_mahasiswa.db')
c = conn.cursor()

# Membuat tabel admin jika belum ada
c.execute('''
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    nama TEXT,
    username TEXT,
    email TEXT,
    password TEXT
)
''')

# Membuat tabel mahasiswa jika belum ada
c.execute('''
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INTEGER PRIMARY KEY,
    nama TEXT,
    nim TEXT,
    ips_semester_1 REAL,
    ips_semester_2 REAL,
    ips_semester_3 REAL,
    ips_semester_4 REAL,
    tagihan_semester_1 INTEGER,
    tagihan_semester_2 INTEGER,
    tagihan_semester_3 INTEGER,
    tagihan_semester_4 INTEGER,
    kehadiran INTEGER,
    kelulusan TEXT
)
''')

# Fungsi untuk mengubah halaman
if 'page' not in st.session_state:
    st.session_state.page = "Login"

def set_page(page):
    st.session_state.page = page
    st.rerun()

# Fungsi untuk memeriksa kredensial login
def check_credentials(username, password):
    c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    return c.fetchone() is not None

# Halaman Login
def page_login():
    st.header("Login Admin")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(label="Login")

    if login_button:
        if check_credentials(username, password):
            loginModal(username)
        else:
            st.error("Username atau password salah!")

@st.experimental_dialog("Berhasil Login!")
def loginModal(item):
    st.write(f"Selamat Datang di Website Prediksi Kelulusan Mahasiswa {item}")
    if st.button("Next"):
        st.session_state.page = "Home"
        st.rerun()

@st.experimental_dialog("Apakah yakin ingin logout?")
def logoutModal():
    col1, col2, col4, col3, col5 = st.columns(5)
    if col1.button("Logout"):
        st.session_state.page = "Login"
        st.rerun()
    if col2.button("Cancel"):
        st.rerun()

def page_home():
    st.header("Home")
    st.write("Selamat datang di aplikasi Website Prediksi Kelulusan Mahasiswa")
    st.image("Logo Unsada.png")
    st.write("UNIVERSITAS DARMA PERSADA")

# Halaman Form
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

        st.write("Prediksi Kelulusan:", prediksi[0])

        status_kelulusan = "LULUS" if prediksi[0] == 1 else "DROPOUT"

        # Convert to DataFrame for display
        df = pd.DataFrame({
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
                               tagihan_semester_1, tagihan_semester_2, tagihan_semester_3, tagihan_semester_4, kehadiran, kelulusan)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nama, nim, ips_semesters[0], ips_semesters[1], ips_semesters[2], ips_semesters[3],
              tagihan_semesters[0], tagihan_semesters[1], tagihan_semesters[2], tagihan_semesters[3], kehadiran, status_kelulusan))
        
        conn.commit()
        st.success("Data berhasil disimpan ke dalam database!")

# Halaman About
def page_about():
    st.header("Data Riwayat Mahasiswa")
    c.execute('''SELECT * FROM mahasiswa''')
    rows = c.fetchall()
    if len(rows) > 0:
        df_history = pd.DataFrame(rows, columns=['ID', 'Nama', 'NIM', 'IPS 1', 'IPS 2', 'IPS 3',
                                                  'IPS 4', 'Tagihan 1', 'Tagihan 2',
                                                  'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)', 'Hasil'])
        df_history = df_history.drop(columns=['ID'])
        st.dataframe(df_history)
    else:
        st.write("Belum ada data yang tersimpan.")

if st.session_state.page != "Login":
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Prediksi', 'Riwayat','Logout'], 
            icons=['house', 'gear','bi-clock-history', 'bi-box-arrow-right'], menu_icon="cast", default_index=1)
        st.session_state.page = selected

# Konten halaman
if st.session_state.page == "Login":
    page_login()
elif st.session_state.page == "Home":
    page_home()
elif st.session_state.page == "Prediksi":
    page_form()
elif st.session_state.page == "Riwayat":
    page_about()
elif st.session_state.page == "Logout":
    logoutModal()

# Menutup koneksi database
conn.close()
