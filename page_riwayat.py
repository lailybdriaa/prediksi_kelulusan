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

# Fungsi untuk mengubah dataframe ke format Excel
def to_excel(df):
    output = BytesIO()  # Membuat data dalam bentuk excel lalu diolah otomatis agar bisa didwnld tanpa harus membuat file dikomputer 
    writer = pd.ExcelWriter(output, engine='openpyxl')  # Membuat writer untuk menulis data ke format Excel
    df.to_excel(writer, index=False, sheet_name='Sheet1')  # Menulis data ke dalam sheet Excel
    writer.close()  # Menutup writer
    processed_data = output.getvalue()  # Mengambil data dari objek BytesIO
    return processed_data  # Mengembalikan data dalam bentuk byte

# Fungsi untuk mengubah dataframe ke format PDF atau mendnld data prediksi menjadi pdf
class PDF(FPDF):
    def header(self):
        # Menambahkan header ke PDF
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Riwayat Mahasiswa', 0, 1, 'C')
        self.ln(10) 
    
    def footer(self):
        # Menambahkan footer ke PDF
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_image(self, image_path):
        # Menambahkan gambar ke PDF
        self.image(image_path, 10, 8, 190)
        self.ln(65)  # Menyesuaikan nilai ini berdasarkan tinggi gambar

    def add_table(self, df):
        # Menambahkan tabel ke PDF
        self.set_font('Arial', '', 10)
        # Tentukan lebar kolom khusus untuk kolom "Nama"
        column_widths = {'Nama': 30, 'IPS 1': 12, 'IPS 2': 12, 'IPS 3': 12, 'IPS 4': 12}
        total_width = 190  # Lebar total halaman PDF dalam mm
        default_col_width = (total_width - sum(column_widths.values())) / (len(df.columns) - len(column_widths))

        row_height = self.font_size + 2
        for col in df.columns:
            col_width = column_widths.get(col, default_col_width)
            self.cell(col_width, row_height * 2, col, border=1)
        self.ln(row_height * 2)

        for row in df.itertuples():
            for col, value in zip(df.columns, row[1:]):
                col_width = column_widths.get(col, default_col_width)
                self.cell(col_width, row_height, str(value), border=1)
            self.ln(row_height)

# Fungsi untuk mengubah DataFrame ke format PDF
def dataframe_to_pdf(df, image_path):
    pdf = PDF()
    pdf.add_page()
    pdf.add_image(image_path)
    pdf.add_table(df)
    return pdf.output(dest='S').encode('latin1')  # Mengembalikan data PDF dalam bentuk byte

# Fungsi untuk mengubah kolom tagihan
def convert_tagihan_columns(df):
    tagihan_columns = ['Tagihan 1', 'Tagihan 2', 'Tagihan 3', 'Tagihan 4']
    for col in tagihan_columns:
        df[col] = df[col].apply(lambda x: 1 if x != 0 else 0)
    return df

# Fungsi untuk memberikan warna merah pada baris "Drop Out"
def highlight_drop_out(s):
    if s['Hasil'] == 'Drop Out':
        return ['background-color: red'] * len(s)
    else:
        return [''] * len(s)

# Fungsi untuk halaman tentang data mahasiswa
def page_about():
    st.header("Data Riwayat Mahasiswa")  # Menampilkan header halaman
    conn = get_db_connection()  # Membuka koneksi ke database
    c = conn.cursor()  # Membuat cursor untuk eksekusi query SQL
    c.execute('''SELECT * FROM mahasiswa''')  # Mengeksekusi query untuk mengambil semua data dari tabel mahasiswa
    rows = c.fetchall()  # Mengambil semua baris hasil query
    conn.close()  # Menutup koneksi ke database
    if len(rows) > 0:
        df_history = pd.DataFrame(rows, columns=['ID', 'Tanggal', 'Nama', 'NIM', 'IPS 1', 'IPS 2', 'IPS 3',
                                                 'IPS 4', 'Tagihan 1', 'Tagihan 2',
                                                 'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)', 'Hasil'])  # Membuat DataFrame dari hasil query
        df_history = df_history.drop(columns=['ID'])  # Menghapus kolom ID dari DataFrame karna sudah ada nomor di website

        # Mengonversi kolom tagihan menjadi 1 atau 0
        df_history = convert_tagihan_columns(df_history)

        df_history_pdf = pd.DataFrame(rows, columns=['ID', 'Tanggal', 'Nama', 'NIM', 'IPS 1', 'IPS 2', 'IPS 3',
                                                     'IPS 4', 'Tagihan 1', 'Tagihan 2',
                                                     'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)', 'Hasil'])  # Membuat DataFrame lain untuk PDF
        df_history_pdf = df_history_pdf.drop(columns=['ID', 'Tanggal', 'NIM'])  # Menghapus kolom yang tidak diperlukan untuk PDF seperti id, tgl, nim di pdf yang di dwnld

        df_history_pdf = df_history_pdf.rename(columns={'Kehadiran (%)': 'Kehadiran'})  # Mengubah nama kolom Kehadiran (%) menjadi kehadiran saja 

        # Mengonversi kolom tagihan menjadi 1 atau 0 untuk PDF
        df_history_pdf = convert_tagihan_columns(df_history_pdf)

        # Mengonversi DataFrame ke format Excel
        excel_data = to_excel(df_history)

        # Mengonversi DataFrame ke format PDF
        image_path = 'kopUnsada.png'  # kop surat gambar yang ingin ditampilkan di PDF 
        pdf_data = dataframe_to_pdf(df_history_pdf, image_path)  #donwload data jadi pdf

        # Mendapatkan tanggal hari ini
        today = datetime.now().strftime("%Y-%m-%d")

        # Tombol untuk mengunduh file Excel dengan menambahkan tanggal unduhnya 
        st.download_button(label='Download Excel', data=excel_data, file_name=f'data_mahasiswa {today}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key='excel_download_button')

        # Tombol untuk mengunduh file PDF dengan menambahkan tanggal unduhnya 
        st.download_button(label='Download PDF', data=pdf_data, file_name=f'Prediksi Kelulusan {today}.pdf', mime='application/pdf', key='pdf_download_button')

        # Menerapkan highlight pada DataFrame
        styled_df = df_history.style.apply(highlight_drop_out, axis=1)
        st.write(styled_df)  # Menampilkan DataFrame dengan highlight di Streamlit
    else:
        st.write("Belum ada data yang tersimpan.")  # Menampilkan pesan jika tidak ada data yang tersimpan atau diprediksi

# Menjalankan fungsi halaman tentang
page_about()
