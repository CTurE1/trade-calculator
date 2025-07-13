import streamlit as st

# ─────────── базовые настройки ───────────
st.set_page_config(page_title="🧮 Трейд-калькулятор", layout="centered")

# ─────────── стили ───────────
st.markdown("""
<style>
 body { background-color:#0e1015; }
 .title   { font-size:24px;font-weight:bold;color:#ffffff;margin-bottom:15px; }
 .card    { background-color:#1b1f26;padding:20px;border-radius:12px;margin-bottom:30px; }
 .label   { font-size:16px;font-weight:500;color:#cccccc; }
 .value   { font-size:20px;font-weight:bold;margin-top:10px; }
 .green   { color:#2ecc71; }
 .orange  { color:#f39c12; }
 .red     { color:#e74c3c; }
 .neutral { color:#bdc3c7; }
</style>
""", unsafe_allow_html=True)

# ─────────── функции ───────────
def get_color_class(value: float, thresholds: dict, neutral_check: bool = True) -> str:
    if neutral_check and value == 0:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    if value > thresholds["low"]:
        return "orange"
    return "red"

def convert_proxy_format(proxy: str) -> str:
    """IP:PORT:USER:PASS → http://USER:PASS@IP:PORT  (возвращает '' при ошибке)"""
    parts = proxy.strip().split(":")
    if len(parts) == 4:
        ip, port, user, password = parts
        return f"http://{user}:{password}@{ip}:{port}"
    return ""

# ─────────── подготовка session_state ───────────
st.session_state.setdefault("converted_proxy", "")
if not isinstance(st.session_state["converted_proxy"], str):
    st.session_state["converted_proxy"] = ""

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

net_profit     = (sell_price * (1 - fee / 100)) - buy_price
profit_percent = ((net_profit / buy_price) * 100) if buy_price else 0
color_np       = get_color_class(profit_percent, {"high": 25, "low": 10})

st.markdown(f'<div class="label">📊 Чистая прибыль:</div>'
            f'<div class="value {color_np}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">📈 Доходность:</div>'
            f'<div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)

# ─────────── блок «Изменение цены» ───────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">📊 Изменение цены</div>', unsafe_allow_html=True)

    old_price = st.number_input("🔙 Было ($)",  value=0.0, step=0.1, key="old_price")
    new_price = st.number_input("🔜 Стало ($)", value=0.0, step=0.1, key="new_price")

    if old_price > 0:
        # ── без комиссии ──
        delta          = new_price - old_price
        percent_change = (delta / old_price) * 100
        color_pc       = get_color_class(percent_change, {"high": 15, "low": 5})

        st.markdown(
            f'<div class="value {color_pc}">'
            f'{new_price:.2f}$ // {percent_change:.2f}% // {delta:+.2f}$'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── с комиссией 5 % ──
        fee_percent    = 5.0                        # меняйте здесь, если нужно другое значение
        adj_price      = new_price * (1 - fee_percent / 100)
        delta_fee      = adj_price - old_price
        percent_fee    = (delta_fee / old_price) * 100
        color_fee      = get_color_class(percent_fee, {"high": 15, "low": 5})

        st.markdown(
            f'<div class="value {color_fee}">'
            f'{adj_price:.2f}$ // {percent_fee:.2f}% // {delta_fee:+.2f}$ '
            f'(с учётом комиссии {fee_percent:.0f}%)'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────── блок «Конвертация прокси» ───────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">🔄 Конвертация прокси под MarketApp</div>', unsafe_allow_html=True)

    proxy_input = st.text_input(
        "🧩 Введите прокси (IP:PORT:USER:PASS)",
        placeholder="185.239.137.172:8000:4zF6NZ:CYCU7u",
        key="proxy_input"
    )

    if proxy_input:
        converted = convert_proxy_format(proxy_input)
        if converted:
            st.session_state["converted_proxy"] = converted
            st.code(converted, language="text")
        else:
            st.warning("❌ Неверный формат. Требуется: IP:PORT:USER:PASS")

st.text_area(
    label="📋 Скопируйте прокси вручную или с Ctrl+C",
    value=st.session_state["converted_proxy"],  # если нужно сразу подставлять строку
    height=80,
    key="converted_proxy"
)


    st.markdown('</div>', unsafe_allow_html=True)
