import streamlit as st

st.set_page_config(page_title="🧮 Трейд-калькулятор", layout="centered")

# ====== Стили ======
st.markdown("""
<style>
    body {
        background-color: #0e1015;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-bottom: 15px;
    }
    .card {
        background-color: #1b1f26;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
    }
    .card:empty {
        background-color: #0e1015 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    .label {
        font-size: 16px;
        font-weight: 500;
        color: #cccccc;
    }
    .value {
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    .green { color: #2ecc71; }
    .orange { color: #f39c12; }
    .red { color: #e74c3c; }
    .neutral { color: #bdc3c7; }
</style>
""", unsafe_allow_html=True)


# ====== Функции ======
def get_color_class(value, thresholds, neutral_check=True):
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    elif value > thresholds["low"]:
        return "orange"
    else:
        return "red"


# ====== Интерфейс ======
st.markdown('<div class="title">📦 Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)
#st.markdown('<div class="card">', unsafe_allow_html=True)

platform = st.radio(
    "Выберите площадку:",
    ["Buff163 (10%)", "CS.MONEY (15%)", "Своя комиссия"],
    horizontal=True
)

if platform == "Buff163 (10%)":
    fee = 10.0
elif platform == "CS.MONEY (15%)":
    fee = 15.0
else:
    fee = st.number_input("🛠 Ваша комиссия (%)", value=15.0, step=0.1)

buy_price = st.number_input("🪙 Цена закупки", value=0.0, step=0.1)
sell_price = st.number_input("💰 Цена продажи", value=0.0, step=0.1)

# Расчёт
net_profit = (sell_price * (1 - fee / 100)) - buy_price
profit_percent = ((net_profit / buy_price) * 100) if buy_price != 0 else 0
color = get_color_class(profit_percent, {"high": 25, "low": 10})

# Вывод результатов
st.markdown(f'<div class="label">📊 Чистая прибыль:</div><div class="value {color}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===== Блок: сравнение цен "Было / Стало" =====
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">📊 Изменение цены</div>', unsafe_allow_html=True)

old_price = st.number_input("🔙 Было ($)", value=0.0, step=0.1, key="old_price")
new_price = st.number_input("🔜 Стало ($)", value=0.0, step=0.1, key="new_price")

if old_price > 0:
    delta = new_price - old_price
    percent_change = (delta / old_price) * 100
    color = get_color_class(percent_change, {"high": 15, "low": 5})

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📊 Изменение цены</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="value {color}">{new_price:.2f}$ // {percent_change:.2f}% // {delta:+.2f}$</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== Блок: Конвертация прокси под MarketApp =====
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="title">🔄 Конвертация прокси под MarketApp</div>', unsafe_allow_html=True)

proxy_input = st.text_input("🧩 Введите прокси (IP:PORT:USER:PASS)", placeholder="185.239.137.172:8000:4zF6NZ:CYCU7u")

def convert_proxy_format(proxy_str):
    parts = proxy_str.strip().split(":")
    if len(parts) == 4:
        ip, port, user, password = parts
        return f"http://{user}:{password}@{ip}:{port}"
    return "❌ Неверный формат. Требуется: IP:PORT:USER:PASS"

if proxy_input:
    converted_proxy = convert_proxy_format(proxy_input)
    st.markdown(f'<div class="value green">{converted_proxy}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


