import streamlit as st

from src.common import generate_slides, read_data


def main():
    st.set_page_config(page_title="Risk Score", page_icon="☢️", layout="wide")

    st.title("Risk Score Analysis ⚠️")

    df = read_data()

    min_date = df["DATETIME"].iloc[0]
    max_date = df["DATETIME"].iloc[-1]
    values = st.slider(
        "Set time range:",
        value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
        format="YYYY-MM-DD",
        min_value=min_date,
        max_value=max_date,
    )

    departments = df["DEPARTMENT"].unique()
    selected_departments = st.multiselect("Select departments to analyze", departments, departments)
    df = df[df["DEPARTMENT"].isin(selected_departments)]
    df = df[(df["DATETIME"] > values[0]) & (df["DATETIME"] < values[1])]

    st.subheader("Risk score")
    data = df.pivot_table(index="DATE", columns="DEPARTMENT", values="RISK_SCORE").fillna(0)
    st.line_chart(data)

    feature = "RISK_SCORE"
    feature_name = "Risk Score"
    generate_slides(df, feature, feature_name)


main()
