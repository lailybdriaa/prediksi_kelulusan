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
                max-width: 50%;
                height: auto;
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
    st.image("Logo Unsada.png", caption="Logo Universitas Darma Persada")
    st.markdown('<p class="footer-text">© 2024 Universitas Darma Persada. All rights reserved.</p>', unsafe_allow_html=True)
