import streamlit as st

st.set_page_config(page_title="🧮 Калькулятор трейда", layout="centered")

# ==== Стилизация в стиле MarketCSGO ====
st.markdown("""
    <style>
        body {
            background-color: #0e1015;
        }
        .section {
            margin-top: 40px;
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


def get_color_class(value, thresholds, neutral_check=True):
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    elif value > thresholds["low"]:
        return "orange"
    else:
        return "red"

# ==== 1. Закуп в Steam под TM ====
st.markdown('<div class="section"><div class="title">🛒 Закуп в Steam под TM</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

steam_buy_price = st.number_input("🎮 Цена покупки в Steam", value=0.0, step=0.1)
tm_sale_price = st.number_input("📦 Цена продажи на TM", value=0.0, step=0.1)
tm_fee = 10.0

net_tm_profit = (tm_sale_price * (1 - tm_fee / 100)) - steam_buy_price
tm_profit_percent = ((net_tm_profit / steam_buy_price) * 100) if steam_buy_price != 0 else 0
tm_color = get_color_class(net_tm_profit, {"high": 0, "low": -10})

st.markdown(f'<div class="label">💵 Чистый заработок:</div><div class="value {tm_color}">{net_tm_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{tm_profit_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ==== 2. Занос в Steam ====
st.markdown('<div class="section"><div class="title">🚀 Занос в Steam</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

tm_purchase_price = st.number_input("📥 Цена закупа (например, TM)", value=0.0, step=0.1)
steam_sale_price = st.number_input("🧾 Цена продажи в Steam", value=0.0, step=0.1)
steam_fee = 15.0

steam_deposit_profit = (steam_sale_price * (1 - steam_fee / 100)) - tm_purchase_price
steam_profit_percent = ((steam_deposit_profit / tm_purchase_price) * 100) if tm_purchase_price != 0 else 0
steam_color = get_color_class(steam_profit_percent, {"high": 25, "low": 15})

st.markdown(f'<div class="label">🎯 +к депу:</div><div class="value {steam_color}">{steam_deposit_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{steam_profit_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ==== 3. LisSkins ➜ MarketCSGO ====
st.markdown('<div class="section"><div class="title">🔄 LisSkins, Buff and others ➜ MarketCSGO</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

lisskins_price = st.number_input("💼 Цена покупки (LisSkins)", value=0.0, step=0.1)
marketcsgo_price = st.number_input("💰 Цена продажи (MarketCSGO)", value=0.0, step=0.1)
market_fee = 10.0

market_profit = (marketcsgo_price * (1 - market_fee / 100)) - lisskins_price
market_profit_percent = ((market_profit / lisskins_price) * 100) if lisskins_price != 0 else 0
market_color = get_color_class(market_profit_percent, {"high": 10, "low": 0})

st.markdown(f'<div class="label">📊 Чистая прибыль:</div><div class="value {market_color}">{market_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{market_profit_percent:.2f}%</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
