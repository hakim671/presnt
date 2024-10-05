import streamlit as st
import os
import pickle
file_path = os.path.join("C:", "Users", "Sanoi", "model.pkl")

with open(file_path, 'rb') as f:
    clf = pickle.load(f)

komn = st.number_input("Количество комнат")
etag = st.number_input("Этаж")
plosh = st.number_input("Площадь")
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
