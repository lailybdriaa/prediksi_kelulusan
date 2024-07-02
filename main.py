import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3

st.button("Button TES")
# Koneksi ke database SQLite
def get_db_connection(): #function deff dengan mengkoneksikan ke database db mahasiswa
    conn = sqlite3.connect('data/data_mahasiswa.db')#variabel conn atau connection untuk mengkoneksikan/menghubungkan ke sqlite dari folder data yang isinya file data_mahasiswa
    return conn #mengembalikan nilai data koneksi tersebut

conn = get_db_connection()  #variabel yang memanggil koneksi database yang isinya data mahasiswa
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
''')#query untuk membuat tabel yang belum ada contohnya tabel admin di database

# Fungsi untuk memeriksa kredensial login
def check_credentials(username, password):
    c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    return c.fetchone() is not None # dengan fuction def mengecek kredensial username dan pw yg dibuat untuk di panggil saat login 

# Halaman Login
def page_login(): #fuction def login yang digunakan untuk menampilkan antarmuka halaman login
    st.header("Login Admin")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button(label="Login")#submit data yang sudah diinput ke text input

    if login_button:
        if check_credentials(username, password):
            loginModal(username)#selamat dtg (username)
        else:
            st.error("Username atau password salah!")

@st.experimental_dialog("Berhasil Login!")
def loginModal(item):
    st.write(f"Selamat Datang di Website Prediksi Kelulusan Mahasiswa {item}")
    if st.button("Ok"):
        st.session_state.page = "Home"
        st.rerun()

@st.experimental_dialog("Apakah yakin ingin logout?")
def logoutModal():
    col1, col2, col4, col3, col5 = st.columns(5)
    if col1.button("Logout"):
        st.session_state.page = "Login"
        st.rerun()


# Inisialisasi halaman
if 'page' not in st.session_state:
    st.session_state.page = "Login" #halaman pertama yang ditampilkan saat membuat website

# Konten halaman
if st.session_state.page == "Login":
    page_login()
else:
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Manual Prediction', 'Upload Excel', 'History Prediction', 'Logout'], 
            icons=['house', 'gear', 'bi-upload', 'bi-clock-history', 'bi-box-arrow-right'], menu_icon="cast", default_index=0)
        st.session_state.page = selected #aksi yang memindahkan halaman
        
    if st.session_state.page == "Home":
        import page_home #import untuk mengimport data/file baru di home grafik data prediksi
        page_home.page_home() #untuk memanggil halaman baru(home)
    elif st.session_state.page == "Manual Prediction":
        import page_prediksi
        page_prediksi.page_form()
    elif st.session_state.page == "Upload Excel":
        import page_excel
        page_excel.page_excel()
    elif st.session_state.page == "History Prediction":
        import page_riwayat
        page_riwayat.page_about()
    elif st.session_state.page == "Logout":
        logoutModal() #pop up logout

# Menutup koneksi database
conn.close()