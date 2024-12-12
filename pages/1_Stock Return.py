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
    value = currency.upper()

    # Metrics for column 1
    df[open_val] = df[open_val].apply(lambda x: x * currencies[currency])
    df[return_val] = df[return_val].apply(lambda x: x * currencies[currency])
    return_instant = "RETURN_INSTANT"
    df[return_instant] = (
        df.groupby(category)[open_val]
        .transform(lambda x: ((x - x.iloc[0]) / x.iloc[0]) * 100)
    )


    st.title("Stock Return Dashboard 💰")
    generate_slides(df)

    if not df.empty:
        df.set_index("DATETIME", inplace=True)

        # Data for Column 2
        open_values = df.pivot_table(index="DATETIME", columns=category, values=open_val).fillna(0)
        return_values = df.pivot_table(index="DATETIME", columns=category, values=return_instant).fillna(0)

        # Data for Column 3
        avg_metric_per_department = df.groupby(category)[open_val].mean().reset_index()

        # Dashboard layout
        with st.container():
            col1, col2, col3 = st.columns(3)

            # Column 1
            with col1:
                st.subheader("Stock price")
                st.line_chart(open_values, y_label=value)

            # Column 2
            with col2:
                st.subheader("Stock return")
                st.line_chart(return_values)

            # Column 3
            with col3:
                st.subheader("Average return per stock")
                st.bar_chart(avg_metric_per_department, x=category, y=open_val, color=category, stack=False,
                             width=150)



main()
