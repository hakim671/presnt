import streamlit as st
name = st.text_input("Введите ваше имя")
if st.button("Нажать"):
  st.write(f"{name} Аутист")
