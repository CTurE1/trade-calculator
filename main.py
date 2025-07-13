import streamlit as st

# ─────────── базовые настройки ───────────
st.set_page_config(page_title="Трейд-калькулятор", layout="centered")

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
 .copy-btn { background-color:#2ecc71;color:white;padding:5px 10px;border:none;border-radius:5px;cursor:pointer; }
 .copy-btn:hover { background-color:#27ae60; }
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

# ─────────── инициализация session_state ───────────
if "copy_success" not in st.session_state:
    st.session_state.copy_success = False

# ─────────── заголовок ───────────
st.markdown('<div class="title">Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)

# ─────────── блок «Комиссия / Прибыль» ───────────
platform = st.radio(
    "Выберите площадку:",
    ["Buff163 (10 %)", "CS.MONEY (15 %)", "Своя комиссия"],
    horizontal=True
)

fee = 10.0 if platform == "Buff163 (10 %)" else 15.0
if platform == "Своя комиссия":
    fee = st.number_input("Ваша комиссия (%)", value=15.0, step=0.1)

buy_price  = st.number_input("Цена закупки", value=0.0, step=0.1)
sell_price = st.number_input("Цена продажи", value=0.0, step=0.1)

net_profit     = (sell_price * (1 - fee / 100)) - buy_price
profit_percent = ((net_profit / buy_price) * 100) if buy_price else 0
color_np       = get_color_class(profit_percent, {"high": 25, "low": 10})

st.markdown(f'<div class="label">Чистая прибыль:</div>'
            f'<div class="value {color_np}">{net_profit:.2f} $</div>', unsafe_allow_html=True)
st.markdown(f'<div class="label">Доходность:</div>'
            f'<div class="value">{profit_percent:.2f}%</div>', unsafe_allow_html=True)

# ─────────── блок «Изменение цены» ───────────
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Изменение цены</div>', unsafe_allow_html=True)

    old_price = st.number_input("Было ($)", value=0.0, step=0.1, key="old_price")
    new_price = st.number_input("Стало ($)", value=0.0, step=0.1, key="new_price")

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
        fee_percent    = 5.0
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
    st.markdown('<div class="title">Конвертация прокси под MarketApp</div>', unsafe_allow_html=True)

    proxy_input = st.text_input(
        "Введите прокси (IP:PORT:USER:PASS)",
        placeholder="185.239.137.172:8000:4zF6NZ:CYCU7u",
        key="proxy_input"
    )

    if proxy_input:
        converted = convert_proxy_format(proxy_input)
        if converted:
            st.markdown("Скопируйте прокси с помощью кнопки или Ctrl+C")
            st.text_area(label="", value=converted, height=80, key="converted_proxy", placeholder="Converted proxy will appear here")
            # Кнопка копирования с JavaScript и уведомлением
            st.markdown(
                f"""
                <button class="copy-btn" onclick="navigator.clipboard.writeText('{converted}').then(() => {{
                    document.getElementById('copy-status').innerText = 'Скопировано!';
                    setTimeout(() => {{ document.getElementById('copy-status').innerText = ''; }}, 2000);
                }}, () => {{
                    document.getElementById('copy-status').innerText = 'Ошибка копирования!';
                    setTimeout(() => {{ document.getElementById('copy-status').innerText = ''; }}, 2000);
                }})">
                    Копировать
                </button>
                <span id="copy-status" style="color: #2ecc71; margin-left: 10px;"></span>
                """,
                unsafe_allow_html=True
            )
            # Дополнительное уведомление через Streamlit
            if st.session_state.copy_success:
                st.success("Прокси скопирован в буфер обмена! (Используйте Ctrl+V для вставки)")
                st.session_state.copy_success = False
        else:
            st.warning("Неверный формат. Требуется: IP:PORT:USER:PASS")

    st.markdown('</div>', unsafe_allow_html=True)
