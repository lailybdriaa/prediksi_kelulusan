import streamlit as st

def page_home():
    st.markdown(
        """
        <style>
            .header-text {
                font-size: 36px;
                color: #333333;
                text-align: center;
                margin-bottom: 20px;
            }

            .subheader-text {
                font-size: 24px;
                color: #666666;
                text-align: center;
                margin-bottom: 30px;
            }

            .university-logo {
                display: block;
                margin: 0 auto;
                max-width: 100%;
                height: auto;
                text-align: center;
                margin-top: 100px;
            }

            .footer-text {
                font-size: 18px;
                color: #999999;
                text-align: center;
                margin-top: 30px;
            }
        </style>
        """
        , unsafe_allow_html=True
    )

    st.markdown('<p class="header-text">Selamat datang di Aplikasi Prediksi Kelulusan Mahasiswa</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">Universitas Darma Persada</p>', unsafe_allow_html=True)
    st.markdown('<center> <img src="https://media.discordapp.net/attachments/955844341635633236/1250380933782310942/LogoUnsada.png?ex=666abb7d&is=666969fd&hm=0ec5b76162b5a5137b190ee4aef65d50201a9a79554b57fe07ff501c80fb9aed&=&format=webp&quality=lossless"> </center>', unsafe_allow_html=True)
    st.markdown('<p class="footer-text">© 2024 Universitas Darma Persada. All rights reserved.</p>', unsafe_allow_html=True)
