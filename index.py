
import streamlit as st
import pandas as pd

tabel=pd.DataFrame({"Column 1" : [1,2,3,4,5,6,7], "Column 2" : [11,12,13,14,15,16,17]})
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("Prediksi Kelulusan")
st.subheader("Universitas Darma Persada")
st.header("Header")
st.text("Ini adalah website untuk memprediksi kelulusan mahasiswa di Univerita Darma Persada")
st.markdown("**Hello** World")

st.write("## H2")

st.table(tabel)

st.dataframe(tabel)

st.image("Logo Unsada.png")
def btn_click():
    print("Button Clicked")
btn=st.button("Click Me!", on_click=btn_click)

st.markdown("<h1 style='text-align: center;'> Login Admin </h1>", unsafe_allow_html=True)

form = st.form("Form 1")
with st.form("Form 2"):
    col1, col2 = st.columns(2)
    col1.text_input("NIP")
    col2.text_input("Password")
    col1.text_input("Email")
    col1.text_input("TTL")
    st.form_submit_button("Submit")

# form.text_input("NIP")
# form.form_submit_button("Submit")