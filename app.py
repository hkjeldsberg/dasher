import streamlit as st

from src.load_data import fetch_data, prepare_data, plot_data


def read_data(plot=False):
    df = fetch_data()
    df = prepare_data(df)

    if plot:
        plot_data(df)

    return df


@st.cache_data
def load_st_data():
    df = read_data()
    return df


def main():
    st.title('Financial Python dashboard')

    data_load_state = st.text('Loading data...')
    df = load_st_data()
    data_load_state.text("Done! (using st.cache_data)")

    st.subheader('Raw data')
    st.write(df)

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    min_date = df.datetime[0]
    max_date = df.datetime[-1]
    values = st.slider(
        "Set time range:",
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD",
        min_value=min_date,
        max_value=max_date
    )
    df = df[(df['datetime'] > values[0]) & (df['datetime'] < values[1])]

    st.subheader("Financial metric")
    data = df.pivot_table(
        index='date',
        columns='department',
        values='financial_metric'
    ).fillna(0)
    chart_metric = st.line_chart(data)

    st.subheader("Risk score")
    data = df.pivot_table(
        index='date',
        columns='department',
        values='risk_score'
    ).fillna(0)
    chart_risk = st.line_chart(data)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Rerun")


main()
