import streamlit as st

st.set_page_config(page_title="🧮 Универсальный трейд-калькулятор", layout="centered")

# ===== Стили =====
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


# ===== Функции =====
def get_color_class(value, thresholds, neutral_check=True):
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    elif value > thresholds["low"]:
        return "orange"
    else:
        return "red"


# ===== Универсальный калькулятор =====
st.markdown('<div class="title">📦 Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

buy_price = st.number_input("💸 Цена закупки", value=0.0, step=0.1)
sell_price = st.number_input("💰 Цена продажи", value=0.0, step=0.1)

fee_option = st.radio(
    "Выберите комиссию площадки:",
    ["Steam (15%)", "TM (10%)", "MarketCSGO (10%)", "LisSkins (0%)", "Своя"],
    index=0,
    horizontal=True
)

fee_map = {
    "Steam (15%)": 15.0,
    "TM (10%)": 10.0,
    "MarketCSGO (10%)": 10.0,
    "LisSkins (0%)": 0.0
}

if fee_option == "Своя":
    fee = st.number_input("🔧 Ваша комиссия (%)", value=15.0, step=0.1)
else:
    fee = fee_map[fee_option]

net_profit = (sell_price * (1 - fee / 100)) - buy_price
profit_percent = ((net_profit / buy_price) * 100) if buy_price != 0 else 0
color = get_color_class(profit_percent, {"high": 25, "low": 10})

st.markdown(f'<div class="label">📊 Чистая прибыль:</div><div class="value {color}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
