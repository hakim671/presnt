import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import math
import pickle

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open("model_rf.pkl", "rb") as file:
    model = pickle.load(file)


komn = st.number_input("Количество комнат",value=1)
etag = st.number_input("Этаж",value=1)
plosh = st.number_input("Площадь",value=50,step=10)
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
tip = st.selectbox("Тип застройки", ["Новостройка", "Вторичный рынок"])
sost = st.selectbox("Состояние", ["Построено", "На стадии"])
rem = st.selectbox("Ремонт", ["Новый", "Средний","Без ремонта"])
df_pred = pd.DataFrame({'Комнаты':[komn],
                        'Этаж':[etag],
                        'Площадь':[plosh],
                        'Город':[city],
                        'Тип':[tip],
                        'Состояние':[sost],
                        'Ремонт':[rem]})
df_pred['Город_Рудаки'] = 0
df_pred['Город_Худжанд'] = 0
df_pred['Тип_Новостройка'] = 1
df_pred['Состояние_Построено'] = 1
df_pred['Ремонт_Новый_ремонт'] = 1
df_pred['Ремонт_С_ремонтом'] = 0

# Присвоение значений на основе условий
if df_pred['Город'].iloc[0] == "Душанбе":
    df_pred['Город_Рудаки'] = 0
    df_pred['Город_Худжанд'] = 0
elif df_pred['Город'].iloc[0] == "Рудаки":
    df_pred['Город_Рудаки'] = 1
    df_pred['Город_Худжанд'] = 0
elif df_pred['Город'].iloc[0] == "Худжанд":
    df_pred['Город_Рудаки'] = 0
    df_pred['Город_Худжанд'] = 1

if df_pred['Тип'].iloc[0] == "Новостройка":
    df_pred['Тип_Новостройка'] = 1

if df_pred['Состояние'].iloc[0] == "Построено":
    df_pred['Состояние_Построено'] = 1

if df_pred['Ремонт'].iloc[0] == "Новый":
    df_pred['Ремонт_Новый_ремонт'] = 1
    df_pred['Ремонт_С_ремонтом'] = 0
elif df_pred['Ремонт'].iloc[0] == "Средний":
    df_pred['Ремонт_Новый_ремонт'] = 0
    df_pred['Ремонт_С_ремонтом'] = 1
elif df_pred['Ремонт'].iloc[0] == "Без ремонта":
    df_pred['Ремонт_Новый_ремонт'] = 0
    df_pred['Ремонт_С_ремонтом'] = 0

# Удаление ненужных колонок
df_pred = df_pred.drop(['Город', 'Тип', 'Состояние', 'Ремонт'], axis=1)
df_sc = scaler.transform(df_pred)
if st.button("Начать прогноз"):
  k = math.floor(int(round(model.predict(df_sc)[0]*0.90,0)) / 100000) * 100000
  t = math.ceil(int(round(model.predict(df_sc)[0]*1.1,0)) / 100000) * 100000
  st.write(f"Цена находится в диапозоне от {k} до {t}")
st.write("Автор Хаким")
