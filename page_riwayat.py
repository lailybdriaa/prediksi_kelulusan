import streamlit as st
import pandas as pd
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('data/data_mahasiswa.db')
c = conn.cursor()

def page_about():   
    st.header("Data Riwayat Mahasiswa")
    c.execute('''SELECT * FROM mahasiswa''')
    rows = c.fetchall()
    if len(rows) > 0:
        df_history = pd.DataFrame(rows, columns=['ID', 'Tanggal', 'Nama', 'NIM', 'IPS 1', 'IPS 2', 'IPS 3',
                                                  'IPS 4', 'Tagihan 1', 'Tagihan 2',
                                                  'Tagihan 3', 'Tagihan 4', 'Kehadiran (%)', 'Hasil'])
        df_history = df_history.drop(columns=['ID'])
        st.dataframe(df_history)
    else:
        st.write("Belum ada data yang tersimpan.")
