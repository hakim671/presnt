import streamlit as st

komn = st.number_input("Количество комнат",value=1)
etag = st.number_input("Этаж",value=1)
plosh = st.number_input("Площадь",value=50,step=10)
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
tip = st.selectbox("Тип застройки", ["Новостройка", "Вторичный рынок"])
sost = st.selectbox("Состояние", ["Построено", "На стадии"])
rem = st.selectbox("Ремонт", ["Новый", "Средний","Без ремонта"])
