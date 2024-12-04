import streamlit as st

from src.common import read_data


def main():
    st.set_page_config(page_title="Home", page_icon="📈", layout="wide")

    st.title("Financial Python Dashboard ℹ️")

    with st.expander("About this board"):
        st.write(
            """
        Welcome to the **Financial Dashboard**! This interactive platform is designed to provide insights into
         financial metrics and risk scores across various departments. Here's what you can do:

        - **Data Exploration**: View raw data and filter it by department or date range for targeted analysis.
        - **Visual Analytics**: Analyze trends with dynamic line charts with key financial metrics and risk scores.
        - **Customization**: Adjust timeframes and focus on specific departments to suit your analysis needs.

        Built with Streamlit, this app leverages Python's data processing capabilities to provide an intuitive and 
        customizable financial analysis experience. Explore and gain valuable insights into your data!
        """
        )

    df = read_data()

    st.subheader("Raw data")
    st.write(df)


main()
