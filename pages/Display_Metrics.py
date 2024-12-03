import streamlit as st

from src.common import generate_slides
from src.load_data import fetch_data, plot_data, prepare_data


@st.cache_data()
def read_data(plot=False):
    df = fetch_data()
    df = prepare_data(df)

    if plot:
        plot_data(df)

    return df


def main():
    st.set_page_config(page_title="Metrics", page_icon="📊", layout="wide")

    st.title("Financial Metrics Display 📈")

    df = read_data()

    min_date = df.datetime.iloc[0]
    max_date = df.datetime.iloc[-1]
    values = st.slider(
        "Set time range:",
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD",
        min_value=min_date,
        max_value=max_date,
    )

    departments = df.department.unique()
    selected_departments = st.multiselect("Select departments to analyze", departments, departments)
    df = df[df["department"].isin(selected_departments)]
    df = df[(df["datetime"] > values[0]) & (df["datetime"] < values[1])]

    st.subheader("Financial metric")
    data = df.pivot_table(index="date", columns="department", values="financial_metric").fillna(0)
    st.line_chart(data)

    feature = "financial_metric"
    feature_name = "metrics"
    generate_slides(df, feature, feature_name)


main()
