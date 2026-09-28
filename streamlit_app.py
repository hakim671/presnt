import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import math

# ---------- Настройка страницы ----------
st.set_page_config(
    page_title="Оценка стоимости недвижимости",
    page_icon="🏠",
    layout="centered",
)

# ---------- Стили ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f4f7fb 0%, #eef2f9 100%);
}

.hero {
    text-align: center;
    padding: 1.6rem 1rem 0.4rem 1rem;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 800;
    color: #1b2540;
    margin-bottom: 0.2rem;
}
.hero p {
    color: #5a6478;
    font-size: 0.95rem;
    margin-top: 0;
}

div[data-testid="stForm"] {
    background: #ffffff;
    border-radius: 18px;
    padding: 1.8rem 1.8rem 1.2rem 1.8rem;
    box-shadow: 0 10px 30px rgba(20, 30, 60, 0.08);
    border: 1px solid #eef0f5;
}

.stButton>button, div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #4f6df5, #6f4ff5);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 0;
    font-size: 1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton>button:hover, div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(79, 109, 245, 0.35);
}

.result-card {
    margin-top: 1.4rem;
    background: linear-gradient(135deg, #eef2ff, #f5f0ff);
    border: 1px solid #dfe4fb;
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
}
.result-card .label {
    color: #5a6478;
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
}
.result-card .price {
    color: #1b2540;
    font-size: 1.5rem;
    font-weight: 800;
}

.footer {
    text-align: center;
    color: #9aa2b1;
    font-size: 0.85rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Заголовок ----------
st.markdown("""
<div class="hero">
    <h1>🏠 Оценка стоимости недвижимости</h1>
    <p>Заполните параметры квартиры — модель подскажет ориентировочный диапазон цены</p>
</div>
""", unsafe_allow_html=True)


# ---------- Загрузка данных и обучение модели (один раз, с кэшем) ----------
@st.cache_resource(show_spinner="Обучаем модель, это займёт немного времени...")
def load_and_train():
    df = pd.read_excel("Homes_enc.xlsx")
    X = df.drop('Цена', axis=1)

    scaler = StandardScaler()
    scaler.fit(X)

    df2 = pd.read_excel("Best_forest.xlsx")
    prices = df2['Цена']
    features = df2.drop(['Цена'], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        features, prices, test_size=0.25, random_state=42
    )

    model = RandomForestRegressor(n_estimators=400, max_depth=14, random_state=42)
    model.fit(X_train, y_train)

    return model, scaler


model, scaler = load_and_train()

# ---------- Форма ввода ----------
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        komn = st.number_input("Комнаты", min_value=1, value=1, step=1)
    with col2:
        etag = st.number_input("Этаж", min_value=1, value=1, step=1)
    with col3:
        plosh = st.number_input("Площадь, м²", min_value=10, value=50, step=10)

    col4, col5 = st.columns(2)
    with col4:
        city = st.selectbox("Город", ["Душанбе", "Худжанд", "Бохтар"])
        tip = st.selectbox("Тип застройки", ["Новостройка", "Вторичный рынок"])
    with col5:
        sost = st.selectbox("Состояние", ["Построено", "На стадии"])
        rem = st.selectbox("Ремонт", ["Новый", "Средний", "Без ремонта"])

    submitted = st.form_submit_button("Начать прогноз")

# ---------- Кодирование признаков и предсказание ----------
if submitted:
    df_pred = pd.DataFrame({
        'Комнаты': [komn],
        'Этаж': [etag],
        'Площадь': [plosh],
    })

    df_pred['Город_Рудаки'] = 1 if city == "Рудаки" else 0
    df_pred['Город_Худжанд'] = 1 if city == "Худжанд" else 0
    df_pred['Тип_Новостройка'] = 1 if tip == "Новостройка" else 0
    df_pred['Состояние_Построено'] = 1 if sost == "Построено" else 0
    df_pred['Ремонт_Новый_ремонт'] = 1 if rem == "Новый" else 0
    df_pred['Ремонт_С_ремонтом'] = 1 if rem == "Средний" else 0

    df_sc = scaler.transform(df_pred)
    pred = model.predict(df_sc)[0]

    low = math.ceil(round(pred * 0.92, 0) / 10000) * 10000
    high = math.floor(round(pred * 1.08, 0) / 10000) * 10000

    def fmt(n):
        return f"{n:,.0f}".replace(",", " ")

    st.markdown(f"""
    <div class="result-card">
        <div class="label">Ориентировочная стоимость</div>
        <div class="price">{fmt(low)} — {fmt(high)}</div>
    </div>
    """, unsafe_allow_html=True)

