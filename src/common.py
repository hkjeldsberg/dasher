import streamlit as st

from src.generate_power_point import generate_ppt
from src.load_data import (fetch_data_from_snowflake, fetch_data_from_sqlite,
                           plot_data, prepare_data)


def generate_slides(df, feature, feature_name):
    if st.button("Generate PowerPoint slide"):
        if df.empty:
            st.error("No data available")
        else:
            save_path = f"{feature_name}.pptx"
            ppt_path = generate_ppt(df, feature)
            st.success("PowerPoint generated successfully!")
            st.download_button(
                label="Download PowerPoint",
                data=open(ppt_path, "rb").read(),
                file_name=save_path,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )


@st.cache_data()
def read_data(use_snowflake=False, plot=False, store_to_csv=False):
    if use_snowflake:
        df = fetch_data_from_snowflake()
    else:
        df = fetch_data_from_sqlite()

    if store_to_csv:
        df.to_csv("src/db/stocks.csv", index=False)

    df = prepare_data(df)

    if plot:
        plot_data(df)

    return df
