import streamlit as st

st.set_page_config(page_title="🧮 Калькулятор трейда", layout="centered")

# ======= СТИЛИ =======
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


# ======= ФУНКЦИИ =======
def get_color_class(value, thresholds, neutral_check=True):
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    elif value > thresholds["low"]:
        return "orange"
    else:
        return "red"


def universal_trade_card(title, default_fee, thresholds):
    st.markdown(f'<div class="card"><div class="title">{title}</div>', unsafe_allow_html=True)

    buy_price = st.number_input("💸 Цена закупки", key=title + "_buy", value=0.0, step=0.1)
    sell_price = st.number_input("💰 Цена продажи", key=title + "_sell", value=0.0, step=0.1)

    st.markdown("**Выберите комиссию площадки:**")
    fee_option = st.radio(
        "Комиссия:",
        ["Steam (15%)", "TM (10%)", "MarketCSGO (10%)", "LisSkins (0%)", "Своя"],
        index=0,
        horizontal=True,
        key=title + "_fee_option"
    )

    fee_map = {
        "Steam (15%)": 15.0,
        "TM (10%)": 10.0,
        "MarketCSGO (10%)": 10.0,
        "LisSkins (0%)": 0.0
    }

    if fee_option == "Своя":
        fee = st.number_input("🔧 Укажите свою комиссию (%)", value=default_fee, step=0.1, key=title + "_custom_fee")
    else:
        fee = fee_map[fee_option]

    net_profit = (sell_price * (1 - fee / 100)) - buy_price
    profit_percent = ((net_profit / buy_price) * 100) if buy_price != 0 else 0
    color = get_color_class(profit_percent, thresholds)

    st.markdown(f'<div class="label">📊 Чистая прибыль:</div><div class="value {color}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ======= РАЗДЕЛЫ =======
st.markdown('<div class="title">🧮 Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)

# Карточки
universal_trade_card("🛒 Закуп в Steam под TM", default_fee=10.0, thresholds={"high": 0, "low": -10})
universal_trade_card("🚀 Занос в Steam", default_fee=15.0, thresholds={"high": 25, "low": 15})
universal_trade_card("🔄 LisSkins ➜ MarketCSGO", default_fee=10.0, thresholds={"high": 10, "low": 0})
