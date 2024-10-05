import streamlit as st
import pickle

with open("model.pkl", 'rb') as f:
    clf = pickle.load(f)

komn = st.number_input("Количество комнат")
etag = st.number_input("Этаж")
plosh = st.number_input("Площадь")
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
