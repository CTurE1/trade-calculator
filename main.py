import streamlit as st

# ─────────── базовые настройки ───────────
st.set_page_config(page_title="🧮 Трейд-калькулятор", layout="centered")

# ─────────── стили ───────────
st.markdown("""
<style>
    body            { background-color:#0e1015; }
    .title          { font-size:24px;font-weight:bold;color:white;margin-bottom:15px; }
    .card           { background-color:#1b1f26;padding:20px;border-radius:12px;margin-bottom:30px; }
    .card:empty     { background-color:#0e1015!important;padding:0!important;margin:0!important;border:none!important;height:0!important; }
    .label          { font-size:16px;font-weight:500;color:#cccccc; }
    .value          { font-size:20px;font-weight:bold;margin-top:10px; }
    .green          { color:#2ecc71; }
    .orange         { color:#f39c12; }
    .red            { color:#e74c3c; }
    .neutral        { color:#bdc3c7; }
</style>
""", unsafe_allow_html=True)

# ─────────── функции ───────────
def get_color_class(value: float, thresholds: dict, neutral_check: bool = True) -> str:
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    elif value > thresholds["low"]:
        return "orange"
    return "red"

def convert_proxy_format(proxy_str: str) -> str:
    """Преобразует IP:PORT:USER:PASS → http://USER:PASS@IP:PORT"""
    parts = proxy_str.strip().split(":")
    if len(parts) == 4:
        ip, port, user, password = parts
        return f"http://{user}:{password}@{ip}:{port}"
    return ""


# ─────────── заголовок ───────────
st.markdown('<div class="title">📦 Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)

# ─────────── блок «Комиссия / Прибыль» ───────────
platform = st.radio(
    "Выберите площадку:",
    ["Buff163 (10 %)", "CS.MONEY (15 %)", "Своя комиссия"],
    horizontal=True
)

fee = 10.0 if platform == "Buff163 (10 %)" else 15.0
if platform == "Своя комиссия":
    fee = st.number_input("🛠 Ваша комиссия (%)", value=15.0, step=0.1)

buy_price  = st.number_input("🪙 Цена закупки",  value=0.0, step=0.1)
sell_price = st.number_input("💰 Цена продажи", value=0.0, step=0.1)

net_profit     = (sell_price * (1 - fee/100)) - buy_price
profit_percent = ((net_profit / buy_price) * 100) if buy_price else 0
color_np       = get_color_class(profit_percent, {"high":25, "low":10})

st.markdown(f'<div class="label">📊 Чистая прибыль:</div><div class="value {color_np}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div><div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)

# ─────────── блок «Изменение цены» ───────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📊 Изменение цены</div>', unsafe_allow_html=True)

    old_price = st.number_input("🔙 Было ($)",  value=0.0, step=0.1, key="old_price")
    new_price = st.number_input("🔜 Стало ($)", value=0.0, step=0.1, key="new_price")

    if old_price > 0:
        delta           = new_price - old_price
        percent_change  = (delta / old_price) * 100
        color_pc        = get_color_class(percent_change, {"high":15, "low":5})

        st.markdown(f'<div class="value {color_pc}">{new_price:.2f}$ // {percent_change:.2f}% // {delta:+.2f}$</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────── блок «Конвертация прокси под MarketApp» ───────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🔄 Конвертация прокси под MarketApp</div>', unsafe_allow_html=True)

    # 1. Пользователь вводит исходную строку
    proxy_input = st.text_input(
        "🧩 Введите прокси (IP:PORT:USER:PASS)",
        placeholder="185.239.137.172:8000:4zF6NZ:CYCU7u",
        key="proxy_input",               # ← это отдельно, конфликтов не создаёт
    )

    # 2. Память для результата
    st.session_state.setdefault("converted_proxy", "")

    # 3. Конвертация
    if proxy_input:
        parts = proxy_input.strip().split(":")
        if len(parts) == 4:
            ip, port, user, password = parts
            st.session_state.converted_proxy = f"http://{user}:{password}@{ip}:{port}"
            st.code(st.session_state.converted_proxy, language="text")
        else:
            st.warning("❌ Неверный формат. Требуется: IP:PORT:USER:PASS")

    # 4. Единственный text_area c НОВЫМ key
    st.text_area(
    label="📋 Скопируйте прокси вручную или с Ctrl+C",
    value=str(st.session_state.get("converted_proxy", "")),  # ← приведение к str
    height=40,
    key="proxy_output_area",
)


    st.markdown('</div>', unsafe_allow_html=True)
