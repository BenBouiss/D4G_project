import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
file_path = "../../data/random_data_with_normalized_absences.csv"  # עדכן את הנתיב לקובץ
df = pd.read_csv(file_path)

# Sidebar filters
st.sidebar.title("Filters")
selected_company = st.sidebar.selectbox("Select Company", df['Company'].unique())
selected_year = st.sidebar.selectbox("Select Year", df['Year'].unique())
selected_age_range = st.sidebar.selectbox("Select Age Range", df['Age Range'].unique())
selected_contract_type = st.sidebar.selectbox("Select Contract Type", df['Contract Type'].unique())

# Filter the dataset based on sidebar inputs
filtered_df = df[(df['Company'] == selected_company) &
                 (df['Year'] == selected_year) &
                 (df['Age Range'] == selected_age_range) &
                 (df['Contract Type'] == selected_contract_type)]

# Graph 1: Percentage of Men and Women
st.header("1. Percentage of Men and Women by Job Category")
df_melted_gender = filtered_df.melt(id_vars='Category',
                                    value_vars=['Men', 'Women'],
                                    var_name='Gender',
                                    value_name='Percentage')
fig1 = px.bar(
    df_melted_gender,
    x='Category',
    y='Percentage',
    color='Gender',
    text='Percentage',
    barmode='group',
    color_discrete_map={'Men': 'gray', 'Women': 'pink'},
    labels={'Category': 'Job Category', 'Percentage': 'Percentage (%)'},
    title='Percentage of Men and Women by Job Category'
)
fig1.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
fig1.update_layout(
    yaxis=dict(title='Percentage (%)', range=[0, 100]),
    xaxis=dict(title='Job Category'),
    legend_title_text='Gender'
)
st.plotly_chart(fig1)

# Graph 2: Normalized Absences
st.header("2. Normalized Absences per Person by Job Category and Gender")
df_melted_absences = filtered_df.melt(id_vars='Category',
                                      value_vars=['Normalized Men Absence', 'Normalized Women Absence'],
                                      var_name='Gender',
                                      value_name='Normalized Absences (Hours)')
fig2 = px.bar(
    df_melted_absences,
    x='Category',
    y='Normalized Absences (Hours)',
    color='Gender',
    text='Normalized Absences (Hours)',
    barmode='group',
    color_discrete_map={'Normalized Men Absence': 'gray', 'Normalized Women Absence': 'pink'},
    labels={'Category': 'Job Category', 'Normalized Absences (Hours)': 'Absences per Person (Normalized)'},
    title='Normalized Absences per Person by Job Category and Gender'
)
fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig2.update_layout(
    yaxis=dict(title='Absences per Person (Normalized)'),
    xaxis=dict(title='Job Category'),
    legend_title_text='Gender'
)
st.plotly_chart(fig2)
