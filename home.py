import streamlit as st

st.set_page_config(page_title="teste site")

st.subheader("meu primeiro site")
st.title(" teste 1")

arquivo = st.file_uploader('adicione seu arquivo',
                           type=['jpg','png','py','wav','csv','json']
                           )
