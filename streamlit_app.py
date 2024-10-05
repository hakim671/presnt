import streamlit as st

komn = st.number_input("Количество комнат",value=30)
etag = st.number_input("Этаж")
plosh = st.number_input("Площадь")
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
tip = st.selectbox("Тип застройки", ["Новостройка", "Вторичный рынок"])
sost = st.selectbox("Состояние", ["Построено", "На стадии"])
rem = st.selectbox("Ремонт", ["Новый", "Средний","Без ремонта"])
