import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

def load_data(table_name):
    db_url = "postgresql://postgres:BenBouiss@localhost:5453/D4G"
    engine = create_engine(db_url)
    query = f'SELECT * FROM "raw"."{table_name}"'
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()