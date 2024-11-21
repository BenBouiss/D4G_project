import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from db_interaction import load_data

import streamlit_event_process

# Function to load data from PostgreSQL


# Sidebar filters for table selection and filtering
st.sidebar.title("Filters")
table_options = [
    "promotion_table", "absence_table", "nationality_table", "seniority_table",
    "age_range_table", "exterior_worker_table", "handicap_table", "other_condition_table"
]
AVAILABLE_TABLES = [
    "Absence", "Nationality", "Promotion"
]
NAME_TO_TABLENAME = {
    "Absence": "absence_table", 
    "Nationality": "nationality_table",
    "Promotion": "promotion_table"
}
selected_name = st.sidebar.selectbox("Select Table for Analysis", AVAILABLE_TABLES)

selected_table = NAME_TO_TABLENAME.get(selected_name)
# Load data from the selected table
data = load_data(selected_table)



# Check if data is loaded
if not data.empty:
   # Filters for Nationality_table
    if selected_name == "Nationality": 
    # Sidebar filters
        number_col = "NBR_EMPLOYEE"
        selected_company = st.sidebar.multiselect(
            "Select Company",
            options=data["ENTERPRISE"].unique(),
            default=data["ENTERPRISE"].unique()
        )

        selected_gender = st.sidebar.multiselect(
            "Select Gender",
            options=data["GENDER"].unique(),
            default=data["GENDER"].unique()
        )

        selected_contract_type = st.sidebar.multiselect(
            "Select Contract Type",
            options=data["CONTRACT_TYPE"].unique(),
            default=data["CONTRACT_TYPE"].unique()
        )

        selected_year = st.sidebar.multiselect(
            "Select Year",
            options=data["YEAR"].unique(),
            default=data["YEAR"].unique()
        )

        selected_nationality = st.sidebar.multiselect(
            "Select Nationality",
            options=data["NATIONALITY"].unique(),
            default=data["NATIONALITY"].unique()
        )

        # Apply filters
        filtered_data = data[
            (data["ENTERPRISE"].isin(selected_company)) &
            (data["GENDER"].isin(selected_gender)) &
            (data["CONTRACT_TYPE"].isin(selected_contract_type)) &
            (data["NATIONALITY"].isin(selected_nationality)) &
            (data["YEAR"].isin(selected_year))
        ]
        streamlit_event_process.process_event_nationality(df=filtered_data)
    # Filters for absence_table
    elif selected_name == "Absence":
         number_col = "ABSENCE_HOURS"
         selected_company = st.sidebar.multiselect(
             "Select Company",
             options=data["ENTERPRISE"].unique(),
             default=data["ENTERPRISE"].unique()
         )
         selected_gender = st.sidebar.multiselect(
             "Select Gender",
             options=data["GENDER"].unique(),
             default=data["GENDER"].unique()
         )
         selected_absence_type = st.sidebar.multiselect(
             "Select Absence Type",
             options=data["ABSENCE_INFO"].unique(),
             default=data["ABSENCE_INFO"].unique()
         )
         selected_year = st.sidebar.multiselect(
             "Select Year",
             options=data["YEAR"].unique(),
             default=data["YEAR"].unique()
         )
         
         # Apply filters
         filtered_data = data[
             (data["ENTERPRISE"].isin(selected_company)) &
             (data["GENDER"].isin(selected_gender)) &
             (data["ABSENCE_INFO"].isin(selected_absence_type)) &
             (data["YEAR"].isin(selected_year))
         ]
         streamlit_event_process.process_event_absence(filtered_data)

    elif selected_name == "Promotion":
         number_col = "NBR_PROMOTION"
         data = data[~ data[number_col].isna()]
         
         selected_company = st.sidebar.multiselect(
             "Select Company",
             options=data["ENTERPRISE"].unique(),
             default=data["ENTERPRISE"].unique()
         )
         selected_gender = st.sidebar.multiselect(
             "Select Gender",
             options=data["GENDER"].unique(),
             default=data["GENDER"].unique()
         )
         selected_year = st.sidebar.multiselect(
             "Select Year",
             options=data["YEAR"].unique(),
             default=data["YEAR"].unique()
         )

         selected_class = st.sidebar.multiselect(
             "Select class",
             options=data["M3E_CLASS"].unique(),
             default=data["M3E_CLASS"].unique()
         )
         # Apply filters
         filtered_data = data[
             (data["ENTERPRISE"].isin(selected_company)) &
             (data["GENDER"].isin(selected_gender)) &
             (data["YEAR"].isin(selected_year)) &
             (data["M3E_CLASS"].isin(selected_class))
         ]
         
         streamlit_event_process.process_event_promotion(filtered_data)
    
    else:
        st.error(f"No data available for {selected_table}.")
 
    # Check if filtered data is empty
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")

else:
    st.error("No data available for the selected table.")



# Display available columns to debug
    st.write("Available Columns in the Table:", data.columns)





# Display the first few rows and columns of the table
    if not data.empty:
        st.write("Sample Data from Absence Table:", data.head())
        st.write("Available Columns:", data.columns)
    else:
        st.error("No data available in the selected table.")





    # # 4. Absence Analysis / ניתוח היעדרויות
    # if "ABSENCES" in filtered_data.columns:
    #     st.header("Absence Analysis")  # Dashboard section title / כותרת חלק הדאשבורד
    #     # Calculate average absences by category and gender
    #     # חישוב ממוצע ההיעדרויות לפי קטגוריה ומגדר
    #     absence_data = filtered_data.groupby(["JOB_TYPE", "GENDER"])["ABSENCES"].mean().reset_index()
    #     # Create a bar chart to compare absences
    #     # יצירת גרף עמודות להשוואת היעדרויות
    #     fig_absences = px.bar(
    #         absence_data,
    #         x="JOB_TYPE",
    #         y="ABSENCES",
    #         color="GENDER",
    #         barmode="group",
    #         title="Average Absences by Gender and Category",
    #         labels={"ABSENCES": "Average Absences", "JOB_TYPE": "Category"}
    #     )
    #     st.plotly_chart(fig_absences)

# # 2. Promotion Analysis / ניתוח קידומים
    # if "PROMOTIONS" in filtered_data.columns:
    #     st.header("Promotion Analysis")  # Dashboard section title / כותרת חלק הדאשבורד
    #     # Calculate the number of promotions by category and gender
    #     # חישוב כמות הקידומים לפי קטגוריה ומגדר
    #     promotion_data = filtered_data.groupby(["JOB_TYPE", "GENDER"])["PROMOTIONS"].sum().reset_index()
    #     # Create a bar chart to compare promotions
    #     # יצירת גרף עמודות להשוואת קידומים
    #     fig_promotions = px.bar(
    #         promotion_data,
    #         x="JOB_TYPE",
    #         y="PROMOTIONS",
    #         color="GENDER",
    #         barmode="group",
    #         title="Promotion Rates by Gender and Category",
    #         labels={"PROMOTIONS": "Total Promotions", "JOB_TYPE": "Category"}
    #     )
    #     st.plotly_chart(fig_promotions)




    # if "SALARY" in filtered_data.columns:
    #     st.header("Salary Analysis")  # Dashboard section title / כותרת חלק הדאשבורד
    #     # Calculate average salary by category and gender
    #     # חישוב ממוצע השכר לפי קטגוריה ומגדר
    #     salary_data = filtered_data.groupby(["JOB_TYPE", "GENDER"])["SALARY"].mean().reset_index()
    #     # Create a bar chart to compare salaries
    #     # יצירת גרף עמודות להשוואת שכר
    #     fig_salary = px.bar(
    #         salary_data,
    #         x="JOB_TYPE",
    #         y="SALARY",
    #         color="GENDER",
    #         barmode="group",
    #         title="Average Salary by Gender and Category",
    #         labels={"SALARY": "Average Salary", "JOB_TYPE": "Category"}
    #     )
    #     st.plotly_chart(fig_salary)




    





        # # 3. Representation in Higher Categories / ייצוג בקטגוריות גבוהות
        # st.header("Representation in Higher Categories")  # Dashboard section title / כותרת חלק הדאשבורד
        # # Calculate representation percentages for each category
        # # חישוב אחוזי הייצוג בכל קטגוריה
        # representation_data = filtered_data["JOB_TYPE"].value_counts(normalize=True).reset_index()
        # representation_data.columns = ["JOB_TYPE", "PERCENTAGE"]
        # # Create a pie chart for representation
        # # יצירת גרף פאי לייצוג
        # fig_representation = px.pie(
        #     representation_data,
        #     names="JOB_TYPE",
        #     values="PERCENTAGE",
        #     title="Representation by Category"
        # )
        # st.plotly_chart(fig_representation)







#     # 5. Contract Type Analysis / ניתוח סוגי חוזה
#     st.header("Contract Type Distribution")  # Dashboard section title / כותרת חלק הדאשבורד
#     # Calculate the number of employees by contract type and gender
#     # חישוב כמות העובדים לפי סוג חוזה ומגדר
#     contract_data = filtered_data.groupby(["CONTRACT_TYPE", "GENDER"])["CONTRACT_TYPE"].count().reset_index(name="COUNT")
#     # Create a bar chart for contract types
#     # יצירת גרף עמודות לסוגי חוזה
#     fig_contract = px.bar(
#         contract_data,
#         x="CONTRACT_TYPE",
#         y="COUNT",
#         color="GENDER",
#         barmode="group",
#         title="Contract Type Distribution by Gender",
#         labels={"COUNT": "Number of Employees", "CONTRACT_TYPE": "Contract Type"}
#     )
#     st.plotly_chart(fig_contract)
# else:
#     # Display when no data matches the filters / תצוגה כאשר אין נתונים מתאימים
#     st.warning(f"No data available for the selected table: {selected_table}")

