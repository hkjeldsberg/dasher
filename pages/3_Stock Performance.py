import plotly.express as px
import streamlit as st

from src.common import read_data, generate_slides


def set_currency(df, currency_factor):
    for key in ["OPEN", "HIGH", "LOW", "CLOSE"]:
        df[key] = df[key].apply(lambda x: x * currency_factor)

    return df


def main():
    category = "TICKER"

    st.set_page_config(page_title="Metrics", page_icon="📊", layout="wide")
    st.title("Stock Performance Dashboard 🥇")

    df = read_data()

    # Set time period
    min_date = df["DATETIME"].min()
    max_date = df["DATETIME"].max()
    values = st.sidebar.slider(
        "Set time range:",
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD",
        min_value=min_date,
        max_value=max_date,
    )
    df = df[(df["DATETIME"] > values[0]) & (df["DATETIME"] < values[1])]
    # Set currency
    currencies = {
        "USD": 1.0,  # Assume USD is default
        "EUR": 0.97,
        "NOK": 11.37
    }
    currency = st.sidebar.selectbox("Currency", currencies.keys())
    df = set_currency(df, currencies[currency])

    # Set stock
    tickers = df[category].unique()
    selected_stock = st.sidebar.selectbox("Select stock to analyze", tickers)
    df_selected = df[df[category] == selected_stock]

    # Metrics
    values = df_selected["CLOSE"]
    start_price = values.iloc[0]
    end_price = values.iloc[-1]
    return_metric = (end_price - start_price) / start_price * 100

    stock_value = (df_selected["VOLUME"].unique() * end_price).sum()
    df_n = df.groupby("TICKER")[['CLOSE', 'VOLUME']].nth[-1]
    total_stock_value = (df_n['CLOSE'] * df_n['VOLUME']).sum()
    portfolio_weight = stock_value / total_stock_value
    portfolio_contrib = (portfolio_weight * return_metric)

    generate_slides(df)


    # Create components
    if not df.empty:

        with st.container():
            col1, col2 = st.columns(2)

            with col1:
                # Display metrics
                st.subheader("Metrics")
                a, b = st.columns(2)
                c, d = st.columns(2)

                # Hardcoded increases/decreases
                d_start = start_price * 0.05
                d_end = end_price * (-0.025)
                d_return = return_metric * 0.07
                d_contrib = portfolio_contrib * 0.1
                a.metric(f"Start price ({currency})", f"{start_price:.2f}", delta=f"{d_start:.2f}")
                c.metric(f"End price ({currency})", f"{end_price:.2f}", delta=f"{d_end:.2f}")
                b.metric("Return (%)", f"{return_metric:.2f}", delta=f"{d_return:.2f}")
                d.metric("Contribution to portfolio (%)", f"{portfolio_weight:.2f}", delta=f"{d_contrib:.2f}")
            with col2:
                # Display graph
                st.subheader("Stock market value")

                df_melt = df_selected.melt(id_vars="DATETIME", value_vars=["OPEN", "CLOSE"], var_name="TYPE",
                                           value_name="PRICE")
                fig = px.line(df_melt, x='DATETIME', y='PRICE', color="TYPE")
                fig.update_layout(
                    xaxis_title=f"Date",
                    yaxis_title=f"Stock price ({currency})"
                )

                event = st.plotly_chart(fig, theme="streamlit", use_container_width=True)


main()
