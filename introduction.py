import pandas as pd
import streamlit as st

csv_file = st.file_uploader("人口データを入力してください")
if csv_file:
    df = pd.read_csv(csv_file, index_col="Prefecture")
    cols = st.columns([1,3], vertical_alignment="center")
    cols[0].dataframe(df)
    cols[1].bar_chart(df)
    