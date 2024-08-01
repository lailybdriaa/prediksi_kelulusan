import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3

# Koneksi ke database SQLite
def get_db_connection(): #function deff dengan mengkoneksikan ke database db mahasiswa
    conn = sqlite3.connect('data/data_mahasiswa.db')#variabel conn atau connection untuk mengkoneksikan/menghubungkan ke sqlite dari folder data yang isinya file data_mahasiswa
    return conn #mengembalikan nilai data koneksi tersebut

# Membuat tabel admin jika belum ada


conn = get_db_connection()  #variabel yang memanggil koneksi database yang isinya data mahasiswa
c = conn.cursor() 

c.execute(''' 
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    nama TEXT,
    username TEXT,
    email TEXT,
    password TEXT,
    hak_akses TEXT
)
''')#query untuk membuat tabel yang belum ada contohnya tabel admin di database

conn.close()

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

def page_kajur():
    import streamlit as st  # Memanggil library Streamlit untuk membuat aplikasi web
    import pandas as pd  # Memanggil library Pandas untuk mengelola data dalam bentuk DataFrame
    import sqlite3  # Memanggil library sqlite3 untuk berinteraksi dengan database SQLite
    from io import BytesIO  # Memanggil modul BytesIO untuk menangani operasi input/output byte
    from fpdf import FPDF  # Memanggil library FPDF untuk membuat dokumen PDF
    from PIL import Image  # Memanggil library PIL untuk memproses gambar
    from datetime import datetime  # Memanggil modul datetime untuk mendapatkan waktu saat ini

    # Fungsi untuk koneksi ke database SQLite
    def get_db_connection():
        conn = sqlite3.connect('data/data_mahasiswa.db')  # Membuka koneksi ke database SQLite
        return conn

    # Fungsi untuk memberikan highlight pada baris yang drop out
    def highlight_dropout(row):
        return ['background-color: red' if row['Hasil'] == 'Drop Out' else '' for _ in row]

    # Fungsi untuk halaman tentang data mahasiswa

    def highlight_dropout(row):
        # Check if 'Hasil' column has the value 'DROPOUT'
        if row['Hasil'] == 'DROPOUT':
            return ['background-color: #f8d7da'] * len(row)
        else:
            return ['background-color: #d4edda'] * len(row)

    def page_about():
        st.header("Data Riwayat Mahasiswa")  # Menampilkan header halaman
        if st.button("LOGOUT"):
            logoutModal()
        
        conn = get_db_connection()  # Membuka koneksi ke database
        c = conn.cursor()  # Membuat cursor untuk eksekusi query SQL
        c.execute('''SELECT * FROM mahasiswa where kelulusan = "DROPOUT"''')  # Mengeksekusi query untuk mengambil semua data dari tabel mahasiswa
        rows = c.fetchall()  # Mengambil semua baris hasil query
        conn.close()  # Menutup koneksi ke database
        if len(rows) > 0:
            df_history = pd.DataFrame(rows, columns=['ID', 'Tanggal', 'Nama', 'NIM', 'IPS 1', 'IPS 2', 'IPS 3',
                                                    'IPS 4', 'Tagihan 1', 'Tagihan 2',
                                                    'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)', 'Hasil'])  # Membuat DataFrame dari hasil query
            df_history = df_history.drop(columns=['ID'])  # Menghapus kolom ID dari DataFrame karena sudah ada nomor di website

            data_placeholder = st.empty()

            today = datetime.now().strftime("%Y-%m-%d")
            # Menampilkan DataFrame sebagai tabel di dalam file yang sudah diunduh dengan highlight untuk mahasiswa yang drop out
        
            styled_df = df_history.style.apply(highlight_dropout, axis=1)
            
            data_placeholder.dataframe(styled_df)

        else:
            st.write("Belum ada data yang tersimpan.")  # Menampilkan pesan jika tidak ada data yang tersimpan atau diprediksi

    page_about()


# Fungsi untuk memeriksa kredensial login
def check_credentials(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_hak_akses(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT hak_akses FROM admin WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

@st.experimental_dialog("Berhasil Login!")
def loginModal(item):
    hak_akses = get_hak_akses(item)
    if hak_akses == "admin":
        st.write(f"Selamat Datang {item} di Website Prediksi Kelulusan Mahasiswa")
        if st.button("Ok"):
            st.session_state.page = "Home"
            st.rerun()
    elif hak_akses == "kajur":
        st.write(f"Selamat Datang KAJURRRR di Website Prediksi Kelulusan Mahasiswa")
        if st.button("Ok"):
            st.session_state.page = "Kajur"
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
elif st.session_state.page == "Kajur":
    page_kajur()
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
