import numpy as np
import streamlit as st

from src.common import generate_slides, read_data


def main():
    open_val = "OPEN"
    return_val = "RETURN"
    category = "TICKER"
    feature_name = "Stock price"

    st.set_page_config(page_title="Metrics", page_icon="📊", layout="wide")

    df = read_data()

    min_date = df["DATETIME"].min()
    max_date = df["DATETIME"].max()
    values = st.sidebar.slider(
        "Set time range:",
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD",
        min_value=min_date,
        max_value=max_date,
    )
    rolling_window = st.sidebar.number_input("Rolling Window Size (days)", min_value=1, max_value=365, value=30)
    rolling_days = rolling_window.real

    currencies = {
        "USD": 1.0,  # Assume USD is default
        "EUR": 0.95,
        "NOK": 11.15
    }
    currency = st.sidebar.selectbox("Currency", currencies.keys())

    departments = df[category].unique()
    selected_departments = st.sidebar.multiselect("Select stocks to analyze", departments, departments)
    df = df[df[category].isin(selected_departments)]
    df = df[(df["DATETIME"] > values[0]) & (df["DATETIME"] < values[1])]
    df['Volatility'] = df[return_val].rolling(window=rolling_days).std() * np.sqrt(rolling_days)
    value = currency.upper()

    # Metrics for column 1
    df[open_val] = df[open_val].apply(lambda x: x * currencies[currency])
    df[return_val] = df[return_val].apply(lambda x: x * currencies[currency])
    return_instant = "RETURN_INSTANT"
    df[return_instant] = (
        df.groupby(category)[open_val]
        .transform(lambda x: ((x - x.iloc[0]) / x.iloc[0]) * 100)
    )

    st.title("Volatility Dashboard 📈")
    generate_slides(df)

    if not df.empty:
        # Data for Column 2
        volatiltiy = df[return_val].std() * np.sqrt(rolling_days)

        vol_values = df.pivot_table(index="DATETIME", columns=category, values="Volatility").fillna(0)

        # Column 1
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Volatility")
                st.metric("Metric", f"{volatiltiy:.2f}")

            # Column 2
            with col2:
                st.subheader(f"Volatility (Window: {rolling_days} days)")
                st.line_chart(vol_values)


main()
