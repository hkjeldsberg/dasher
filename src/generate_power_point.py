from datetime import datetime

import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches


def generate_ppt(df, feature, output_file="generated_report.pptx"):
    ppt = Presentation()
    # Page 1
    title_slide_layout = ppt.slide_layouts[0]
    slide = ppt.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = "Dynamic Report"
    slide.placeholders[1].text = "Generated using  Streamlit + Python + python-pptx"

    # Page 2 - Raw data
    table_slide_layout = ppt.slide_layouts[5]
    slide = ppt.slides.add_slide(table_slide_layout)
    title = slide.shapes.title
    title.text = "Data Overview"

    rows, cols = df.shape
    max_rows = 12
    table = slide.shapes.add_table(max_rows + 1, cols, Inches(0.2), Inches(0.2), Inches(9), Inches(4)).table

    for col_idx, column_name in enumerate(df.columns):
        table.cell(0, col_idx).text = column_name

    for row_idx, row_data in enumerate(df.head(max_rows).values, start=1):
        for col_idx, value in enumerate(row_data):
            if isinstance(value, float):
                value = f"{float(value):.2f}"
            elif isinstance(value, datetime):
                value = value.strftime("%m/%d/%Y")
            else:
                value = str(value)
            table.cell(row_idx, col_idx).text = value

    # Page 3: Chart
    if not df.empty:
        fig, ax = plt.subplots()
        df.groupby("department")[feature].plot(ax=ax)

        plt.title(f"{feature.capitalize()} time series")
        plt.legend(loc="upper left")

        chart_image = "slides/chart.png"
        plt.savefig(chart_image)
        plt.close()

        chart_slide_layout = ppt.slide_layouts[5]
        slide = ppt.slides.add_slide(chart_slide_layout)
        title = slide.shapes.title
        title.text = "Chart Representation"
        slide.shapes.add_picture(chart_image, Inches(1), Inches(1.5), Inches(7), Inches(5))

    ppt.save(output_file)
    return output_file
