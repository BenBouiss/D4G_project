import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from db_interaction import load_data

def process_event_nationality(df):

    # Group by nationality and gender, then sum the values
    number_col = "NBR_EMPLOYEE"
    nationality_gender_totals = df.groupby(["NATIONALITY", "GENDER"])[number_col].sum().reset_index()

    # Create a grouped bar chart to compare genders
    fig_nationality_gender = px.bar(
        nationality_gender_totals,
        x="NATIONALITY",
        y=number_col,
        color="GENDER",
        barmode="group",
        title="Total Employees by Nationality and Gender",
        labels={number_col: "Number of Employees", "NATIONALITY": "Nationality", "GENDER": "Gender"}
    )

    # Display the chart
    st.plotly_chart(fig_nationality_gender)

    # Group by year and nationality, then sum the values
    yearly_nationality_trend = df.groupby(["YEAR", "NATIONALITY"])["NBR_EMPLOYEE"].sum().reset_index()

    # Create a line chart to show the trend over years
    fig_yearly_nationality = px.line(
        yearly_nationality_trend,
        x="YEAR",
        y=number_col,
        color="NATIONALITY",
        title="Yearly Trend of Employees by Nationality",
        labels={number_col: "Number of Employees", "YEAR": "Year", "NATIONALITY": "Nationality"}
    )

    # Display the chart
    st.plotly_chart(fig_yearly_nationality)


def process_event_absence(df):
        # Group by nationality and gender, then sum the values
    number_col = "ABSENCE_HOURS"
    nationality_gender_totals = df.groupby(["JOB_TYPE", "GENDER"])[number_col].sum().reset_index()

    # Create a grouped bar chart to compare genders
    fig_nationality_gender = px.bar(
        nationality_gender_totals,
        x="JOB_TYPE",
        y=number_col,
        color="GENDER",
        barmode="group",
        title="Absence hours by job type and Gender",
        labels={number_col: "Absence hours", "JOB_TYPE": "JOB_TYPE", "GENDER": "Gender"}
    )

    # Display the chart
    st.plotly_chart(fig_nationality_gender)

    # Group by year and nationality, then sum the values
    yearly_absence_trend = df.groupby(["YEAR", "GENDER"])[number_col].sum().reset_index()

    # Create a line chart to show the trend over years
    fig_yearly_nationality = px.line(
        yearly_absence_trend,
        x="YEAR",
        y=number_col,
        color="GENDER",
        title="Yearly trend of absence hours by gender",
        labels={number_col: "Absence hours", "YEAR": "Year", "JOB_TYPE": "JOB_TYPE"}
    )
    
    # Display the chart
    st.plotly_chart(fig_yearly_nationality)
    
    # normalized bu number of employee
    df_nbr_employee = load_data("age_range_table")
    df_nbr_employee = df_nbr_employee.groupby(["YEAR", "GENDER"])["NBR_EMPLOYEE"].sum()
    
    yearly_absence_trend_normed = (df.groupby(["YEAR", "GENDER"])[number_col].sum() / df_nbr_employee).reset_index()

    
    fig_yearly_per_job_nationality_normed = px.line(
        yearly_absence_trend_normed,
        x="YEAR",
        y=0,
        color="GENDER",
        title="Yearly normalized trend of absence hours by gender",
        labels={number_col: "Number of Employees", "YEAR": "Year", "JOB_TYPE": "JOB_TYPE", "0": "Absence hour per\nemployee on average (Hr/employee)"}
    )
    st.plotly_chart(fig_yearly_per_job_nationality_normed)

def process_event_promotion(df):
        # Group by nationality and gender, then sum the values
    number_col = "NBR_PROMOTION"
    nationality_gender_totals = df.groupby(["JOB_TYPE", "GENDER"])[number_col].sum().reset_index()

    # Create a grouped bar chart to compare genders
    fig_nationality_gender = px.bar(
        nationality_gender_totals,
        x="JOB_TYPE",
        y=number_col,
        color="GENDER",
        barmode="group",
        title="Promotion by job type and Gender",
        labels={number_col: "Promotion", "JOB_TYPE": "JOB_TYPE", "GENDER": "Gender"}
    )

    # Display the chart
    st.plotly_chart(fig_nationality_gender)

    # Group by year and nationality, then sum the values
    yearly_absence_trend = df.groupby(["YEAR", "GENDER"])[number_col].sum().reset_index()

    # Create a line chart to show the trend over years
    fig_yearly_nationality = px.line(
        yearly_absence_trend,
        x="YEAR",
        y=number_col,
        color="GENDER",
        title="Yearly trend of promotion by gender",
        labels={number_col: "Promotion", "YEAR": "Year", "JOB_TYPE": "JOB_TYPE"}
    )
    
    # Display the chart
    st.plotly_chart(fig_yearly_nationality)
    
    # normalized bu number of employee
    df_nbr_employee = load_data("age_range_table")
    df_nbr_employee = df_nbr_employee.groupby(["YEAR", "GENDER"])["NBR_EMPLOYEE"].sum()
    
    yearly_absence_trend_normed = (df.groupby(["YEAR", "GENDER"])[number_col].sum() / df_nbr_employee).reset_index()

    
    
    fig_yearly_per_job_nationality_normed = px.line(
        yearly_absence_trend_normed,
        x="YEAR",
        y=0,
        color="GENDER",
        title="Yearly normalized trend of promotion by gender",
        labels={number_col: "Promotion", "YEAR": "Year", "JOB_TYPE": "JOB_TYPE", "0": "Promotion per\nemployee on average (promotion/employee)"}
    )
    st.plotly_chart(fig_yearly_per_job_nationality_normed)
