import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Function to load data from PostgreSQL
def load_data(table_name):
    db_url = "postgresql://postgres:BenBouiss@localhost:5455/D4G"
    engine = create_engine(db_url)
    query = f'SELECT * FROM "raw"."{table_name}"'
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Sidebar filters for table selection and filtering
st.sidebar.title("Filters")
table_options = [
    "promotion_table", "absence_table", "Nationality_table", "Seniority_table",
    "age_range_table", "exterior_worker_table", "handicap_table", "other_condition_table"
]
selected_table = st.sidebar.selectbox("Select Table for Analysis", table_options)

# Load data from the selected table
data = load_data(selected_table)

# Check if data is loaded
if not data.empty:
    # Sidebar filters
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

    # Check if filtered data is empty
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Ensure VALUE column exists
        if "VALUE" in filtered_data.columns:
            # Group by nationality and gender, then sum the values
            nationality_gender_totals = filtered_data.groupby(["NATIONALITY", "GENDER"])["VALUE"].sum().reset_index()

            # Create a grouped bar chart to compare genders
            fig_nationality_gender = px.bar(
                nationality_gender_totals,
                x="NATIONALITY",
                y="VALUE",
                color="GENDER",
                barmode="group",
                title="Total Employees by Nationality and Gender",
                labels={"VALUE": "Number of Employees", "NATIONALITY": "Nationality", "GENDER": "Gender"}
            )

            # Display the chart
            st.plotly_chart(fig_nationality_gender)

            # Group by year and nationality, then sum the values
            yearly_nationality_trend = filtered_data.groupby(["YEAR", "NATIONALITY"])["VALUE"].sum().reset_index()

            # Create a line chart to show the trend over years
            fig_yearly_nationality = px.line(
                yearly_nationality_trend,
                x="YEAR",
                y="VALUE",
                color="NATIONALITY",
                title="Yearly Trend of Employees by Nationality",
                labels={"VALUE": "Number of Employees", "YEAR": "Year", "NATIONALITY": "Nationality"}
            )

            # Display the chart
            st.plotly_chart(fig_yearly_nationality)
        else:
            st.warning("The 'VALUE' column is not available in the selected table.")
else:
    st.error("No data available for the selected table.")




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

