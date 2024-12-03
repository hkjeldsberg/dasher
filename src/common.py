import streamlit as st

from src.generate_power_point import generate_ppt


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
