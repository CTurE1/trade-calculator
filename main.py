import re
import streamlit as st
import pandas as pd

# ---------------- НАСТРОЙКА СТРАНИЦЫ ----------------
st.set_page_config(
    page_title="Trading Tools",
    layout="wide",
    page_icon="🧮"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }
body, .stApp { background:#0e1015; }
.block-container {
    padding-top: 0.8rem;
    max-width: 760px;
    margin: 0 auto;
}
.title-main {
    font-size:30px;
    font-weight:700;
    text-align:center;
    margin:10px 0 30px;
    color:#ffffff;
}
.subtitle {
    font-size:19px;
    font-weight:600;
    margin-bottom:14px;
    color:#ffffff;
}
.card {
    background:#1b1f26;
    padding:22px 26px;
    border-radius:14px;
    margin-bottom:26px;
    border:1px solid #252b33;
}
.label { font-size:15px; font-weight:500; color:#d0d3d6; margin-top:4px; }
.value { font-size:22px; font-weight:600; margin-top:4px; }
.green { color:#2ecc71; }
.orange{ color:#f39c12; }
.red   { color:#e74c3c; }
.neutral{color:#95a5a6;}
/* Скрыть хедер (если хотите оставить - закомментируйте две строки ниже) */
header[data-testid="stHeader"] { height:0px; }
header[data-testid="stHeader"] div { display:none; }
</style>
""", unsafe_allow_html=True)

# ---------------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------------
def get_color_class(value: float, thresholds: dict, neutral_check: bool = True) -> str:
    if neutral_check and abs(value) < 1e-12:
        return "neutral"
    if value > thresholds["high"]:
        return "green"
    if value > thresholds["low"]:
        return "orange"
    return "red"

def normalize_proxy(raw: str) -> str:
    """Нормализует строку прокси в формат http://user:pass@ip:port.
       Поддерживаемые входы: IP:PORT:USER:PASS или USER:PASS@IP:PORT (с optional http://)."""
    if not raw:
        return ""
    raw = raw.strip()
    raw = raw.replace("http://", "").replace("https://", "").replace(" ", "")
    # USER:PASS@IP:PORT
    m = re.match(r'^([^:@]+):([^:@]+)@([0-9a-zA-Z\.\-]+):(\d+)$', raw)
    if m:
        user, pwd, ip, port = m.groups()
        return f"http://{user}:{pwd}@{ip}:{port}"
    # IP:PORT:USER:PASS
    m = re.match(r'^([0-9a-zA-Z\.\-]+):(\d+):([^:@]+):([^:@]+)$', raw)
    if m:
        ip, port, user, pwd = m.groups()
        return f"http://{user}:{pwd}@{ip}:{port}"
    return ""

# Инициализация session_state
st.session_state.setdefault("converted_proxy", "")
st.session_state.setdefault("proxy_input", "")
st.session_state.setdefault("old_price_main", 0.0)
st.session_state.setdefault("new_price_main", 0.0)
st.session_state.setdefault("buy_price", 0.0)
st.session_state.setdefault("sell_price", 0.0)

# ---------------- ВКЛАДКИ ----------------
tab_calc, tab_buff, tab_about = st.tabs(["🧮 Калькулятор", "💱 BUFF163 CSV", "ℹ️ О программе"])

# =====================================================================
# ВКЛАДКА 1: КАЛЬКУЛЯТОР
# =====================================================================
with tab_calc:
    st.markdown('<div class="title-main">🧮 Универсальный трейд-калькулятор</div>', unsafe_allow_html=True)

    # ----- Комиссия / Прибыль -----
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">📊 Комиссия / Прибыль</div>', unsafe_allow_html=True)

        platform = st.radio(
            "Площадка:",
            ["Buff163 (10%)", "CS.MONEY (15%)", "Своя комиссия"],
            horizontal=True,
            label_visibility="collapsed",
            key="platform_choice"
        )
        fee = 10.0 if platform == "Buff163 (10%)" else 15.0
        if platform == "Своя комиссия":
            fee = st.number_input("🛠 Ваша комиссия (%)", value=15.0, step=0.1, key="custom_fee")

        col_buy, col_sell = st.columns(2)
        with col_buy:
            buy_price = st.number_input("🪙 Цена закупки", value=st.session_state["buy_price"], step=0.1, key="buy_price")
        with col_sell:
            sell_price = st.number_input("💰 Цена продажи", value=st.session_state["sell_price"], step=0.1, key="sell_price")

        net_profit = (sell_price * (1 - fee / 100)) - buy_price
        profit_percent = (net_profit / buy_price * 100) if buy_price else 0.0
        color_np = get_color_class(profit_percent, {"high": 25, "low": 10})

        st.markdown(
            f'<div class="label">Чистая прибыль:</div>'
            f'<div class="value {color_np}">{net_profit:.2f} $</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="label">Доходность:</div>'
            f'<div class="value">{profit_percent:.2f}%</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ----- Изменение цены -----
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">📈 Изменение цены</div>', unsafe_allow_html=True)

        old_price = st.number_input("🔙 Было ($)", value=st.session_state["old_price_main"], step=0.1, key="old_price_main")
        new_price = st.number_input("🔜 Стало ($)", value=st.session_state["new_price_main"], step=0.1, key="new_price_main")

        if old_price > 0:
            delta = new_price - old_price
            percent_change = (delta / old_price) * 100
            color_pc = get_color_class(percent_change, {"high": 15, "low": 5})

            st.markdown(
                f'<div class="value {color_pc}">'
                f'{new_price:.2f}$  //  {percent_change:.2f}%  //  {delta:+.2f}$'
                f'</div>',
                unsafe_allow_html=True
            )

            # Комиссия для корректировки цены — используем ту же fee или задайте отдельный инпут при желании
            fee_percent = 5.0
            adj_price = new_price * (1 - fee_percent / 100)
            delta_fee = adj_price - old_price
            percent_fee = (delta_fee / old_price) * 100
            color_fee = get_color_class(percent_fee, {"high": 15, "low": 5})

            st.markdown(
                f'<div class="value {color_fee}">'
                f'{adj_price:.2f}$  //  {percent_fee:.2f}%  //  {delta_fee:+.2f}$ (с комиссией {fee_percent:.0f}%)'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.caption("Введите значение «Было ($)» > 0, чтобы увидеть динамику.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ----- Конвертация прокси -----
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">🔄 Конвертация прокси для MarketApp</div>', unsafe_allow_html=True)

        proxy_input = st.text_input(
            "Прокси (формат IP:PORT:USER:PASS или USER:PASS@IP:PORT)",
            placeholder="185.239.137.172:8000:login:pass",
            key="proxy_input"
        )

        if proxy_input:
            converted = normalize_proxy(proxy_input)
            if converted:
                st.session_state["converted_proxy"] = converted
                st.code(converted, language="text")
            else:
                st.warning("❌ Неверный формат. Примеры: 1.2.3.4:8000:user:pass  ИЛИ  user:pass@1.2.3.4:8000")

        # Кнопка сброса — центрируем
        reset_col = st.columns(3)[1]
        with reset_col:
            if st.button("♻️ Сбросить поля", use_container_width=True, key="reset_btn"):
                # ЯВНО обнуляем все поля, которые хотим очистить
                st.session_state["converted_proxy"] = ""
                st.session_state["proxy_input"] = ""
                st.session_state["old_price_main"] = 0.0
                st.session_state["new_price_main"] = 0.0
                st.session_state["buy_price"] = 0.0
                st.session_state["sell_price"] = 0.0
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<p style="text-align:center; color:#6c737a; font-size:12px; margin-top:4px;">'
        'Made for internal trading tooling · v1</p>',
        unsafe_allow_html=True
    )

# =====================================================================
# ВКЛАДКА 2: BUFF163 CSV
# =====================================================================
with tab_buff:
    st.markdown('<div class="title-main">💱 BUFF163 CSV конвертер</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Загрузите .csv файл", type="csv", key="csv_uploader")
    exchange_rate = st.number_input("Курс CNY → USD", value=7.08, step=0.01, key="exchange_rate")

    if uploaded_file:
        encodings_to_try = ['utf-8-sig', 'gb18030', 'utf-8']
        df = None
        last_error = ""
        for enc in encodings_to_try:
            try:
                df = pd.read_csv(uploaded_file, encoding=enc)
                break
            except Exception as e:
                last_error = str(e)

        if df is None:
            st.error(f"Не удалось прочитать файл. Последняя ошибка: {last_error}")
        else:
            st.subheader("Предпросмотр (первые 5 строк)")
            st.dataframe(df.head())

            price_candidates = ['Price', '价格', 'Цена', '價格']
            price_col = None
            for col in df.columns:
                if col.strip() in price_candidates:
                    price_col = col
                    break
            if not price_col:
                for col in df.columns:
                    if df[col].astype(str).head(15).str.contains('¥').any():
                        price_col = col
                        break

            if not price_col:
                st.error("Не найдена колонка с ценами.")
            else:
                st.info(f"Найдена колонка: **{price_col}**")
                df['Price_clean'] = (
                    df[price_col].astype(str)
                      .str.replace('¥', '', regex=False)
                      .str.replace('￥', '', regex=False)
                      .str.replace(',', '', regex=False)
                      .str.replace('\u00a0', '', regex=False)
                      .str.strip()
                )
                df['Price_clean'] = pd.to_numeric(df['Price_clean'], errors='coerce')
                df['Price_usd'] = df['Price_clean'] / exchange_rate

                total_cny = df['Price_clean'].sum(skipna=True)
                total_usd = df['Price_usd'].sum(skipna=True)

                st.success(f"Общая сумма: {total_cny:.2f} CNY / {total_usd:.2f} USD")

                st.subheader("Пример пересчёта")
                st.dataframe(df[[price_col, 'Price_clean', 'Price_usd']].head())

                with st.expander("Дополнительная аналитика"):
                    for gcol in ['Game', 'Status']:
                        if gcol in df.columns:
                            grouped = df.groupby(gcol).agg(
                                Количество=("Price_clean", "count"),
                                Сумма_CNY=("Price_clean", "sum"),
                                Сумма_USD=("Price_usd", "sum"),
                            )
                            st.markdown(f"**Группировка по `{gcol}`**")
                            st.dataframe(grouped)

                out_csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Скачать расширенный CSV",
                    data=out_csv,
                    file_name="buff163_converted.csv",
                    mime="text/csv",
                    key="download_btn"
                )

# =====================================================================
# ВКЛАДКА 3: О ПРОГРАММЕ
# =====================================================================
with tab_about:
    st.markdown('<div class="title-main">ℹ️ О программе</div>', unsafe_allow_html=True)
    st.markdown("""
**Содержит:**
- 🧮 Калькулятор (комиссия, чистая прибыль, изменение цены)
- 🔄 Конвертер прокси
- 💱 Анализ BUFF163 CSV (CNY → USD)

**Идеи развития:**
- История расчётов
- Пакетный расчёт нескольких комиссий
- Автоподгрузка курса через API
""")
