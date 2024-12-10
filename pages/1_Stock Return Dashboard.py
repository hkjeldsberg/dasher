import streamlit as st

from src.common import generate_slides, read_data


def main():
    feature = "OPEN"
    category = "TICKER"
    feature_name = "Stock price"

    st.set_page_config(page_title="Metrics", page_icon="📊", layout="wide")

    st.title("Financial Metrics Dashboard 📈")

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

    departments = df[category].unique()
    selected_departments = st.sidebar.multiselect("Select stocks to analyze", departments, departments)
    df = df[df[category].isin(selected_departments)]
    df = df[(df["DATETIME"] > values[0]) & (df["DATETIME"] < values[1])]

    # Metrics for column 1
    if not df.empty:
        df.set_index("DATETIME", inplace=True)
        avg_metric = df[feature].mean()
        max_feature = df.loc[df[feature].idxmax()]
        max_department = max_feature[category]
        max_value = max_feature[feature]

        # Data for Column 2
        line_chart_data = df.pivot_table(index="DATETIME", columns=category, values=feature).fillna(0)

        # Data for Column 3
        avg_metric_per_department = df.groupby(category)[feature].mean().reset_index()

        # Hardcoded max values
        AVG_MAX = 39731.452249880334
        MAX_VAL = 55143.865481222725

        # Dashboard layout
        with st.container():
            col1, col2, col3 = st.columns(3)

            # Column 1
            with col1:
                st.subheader("Overview")
                st.metric(label="Average Metric Value", value=f"{1:.0f}", delta=f"{1:.02f} %")
                st.metric(label=f"Max Risk Department: OK", value=f"{1:.0f}", delta=f"{1:.02f} %")

            # Column 2
            with col2:
                st.subheader("Metric Analysis")
                st.line_chart(line_chart_data)

            # Column 3
            with col3:
                st.subheader("Average Metric per Department")
                st.bar_chart(avg_metric_per_department, x=category, y=feature, color=category, stack=False,
                             width=150)

    generate_slides(df, feature, feature_name)


main()
