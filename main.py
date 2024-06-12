import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('data/data_mahasiswa.db')
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
    if st.button("Ok"):
        st.session_state.page = "Home"
        st.experimental_rerun()

@st.experimental_dialog("Apakah yakin ingin logout?")
def logoutModal():
    col1, col2, col4, col3, col5 = st.columns(5)
    if col1.button("Logout"):
        st.session_state.page = "Login"
        st.rerun()
    if col2.button("Cancel"):
        st.session_state.page = "Home"
        st.rerun()

# Inisialisasi halaman
if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Konten halaman
if st.session_state.page == "Login":
    page_login()
else:
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Prediksi', 'Riwayat','Logout'], 
            icons=['house', 'gear','bi-clock-history', 'bi-box-arrow-right'], menu_icon="cast", default_index=0)
        st.session_state.page = selected
        
    if st.session_state.page == "Home":
        import page_home
        page_home.page_home()
    elif st.session_state.page == "Prediksi":
        import page_prediksi
        page_prediksi.page_form()
    elif st.session_state.page == "Riwayat":
        import page_riwayat
        page_riwayat.page_about()
    elif st.session_state.page == "Logout":
        logoutModal()

# Menutup koneksi database
conn.close()
