import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

df = pd.read_excel("Homes_enc.xlsx")
X = df.drop('Цена', axis=1)  # Признаки
y = df['Цена']
scaler.fit_transform(X)

df2 = pd.read_excel("Best_forest.xlsx")
prices = df2['Цена']
features = df2.drop(['Цена'],axis=1)

X_train, X_test, y_train, y_test = train_test_split(features,prices,
                                                    test_size=0.25, random_state=42)
model = RandomForestRegressor(n_estimators=400, max_depth=14, random_state=42)
model.fit(X_train,y_train)

komn = st.number_input("Количество комнат",value=1)
etag = st.number_input("Этаж",value=1)
plosh = st.number_input("Площадь",value=50,step=10)
city = st.selectbox("Выберите город", ["Душанбе", "Худжанд", "Бохтар"])
tip = st.selectbox("Тип застройки", ["Новостройка", "Вторичный рынок"])
sost = st.selectbox("Состояние", ["Построено", "На стадии"])
rem = st.selectbox("Ремонт", ["Новый", "Средний","Без ремонта"])
df_pred = pd.DataFrame({'Комнаты':komn,
                        'Этаж':etag,
                        'Площадь':plosh,
                        'Город':city,
                        'Тип':tip,
                        'Состояние':sost,
                        'Ремонт':rem})
if(df_pred['Город'] == "Душанбе"):
  df_pred['Город_Рудаки'] == 0
  df_pred['Город_Худжанд'] == 0
if(df_pred['Город'] == "Рудаки"):
  df_pred['Город_Рудаки'] == 1
  df_pred['Город_Худжанд'] == 0
if(df_pred['Город'] == "Худжанд"):
  df_pred['Город_Рудаки'] == 0
  df_pred['Город_Худжанд'] == 1
if(df_pred['Тип'] == "Новостройка"):
  df_pred["Новостройка"] = 1
if(df_pred['Состояние'] == "Построено"):
  df_pred["Состояние_Построено"] = 1
if(df_pred['Ремонт'] == "Новый"):
  df_pred["Ремонт_Новый_ремонт"] = 1
  df_pred["Ремонт_С_ремонтом"] = 0
if(df_pred['Ремонт'] == "Средний"):
  df_pred["Ремонт_Новый_ремонт"] = 0
  df_pred["Ремонт_С_ремонтом"] = 1
if(df_pred['Ремонт'] == "Без ремонта"):
  df_pred["Ремонт_Новый_ремонт"] = 0
  df_pred["Ремонт_С_ремонтом"] = 0
df_pred.drop(['Город','Тип','Состояние','Ремонт'],axis=1)
st.write('hello')
