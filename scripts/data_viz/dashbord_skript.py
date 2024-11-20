import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine






# Function to load data from PostgreSQL
# פונקציה לטעינת נתונים מתוך PostgreSQL
def load_data(table_name):
    # Define the database connection
    # הגדרת חיבור למסד הנתונים
    db_url = "postgresql://postgres:BenBouiss@localhost:5455/D4G"
    engine = create_engine(db_url)  # Create a database engine / יצירת מנוע למסד הנתונים
    
    # Create a dynamic query for the selected table
    # יצירת שאילתה דינמית עבור הטבלה שנבחרה
    query = f'SELECT * FROM "raw"."{table_name}"'
    try:
        # Read the data into a DataFrame
        # קריאת הנתונים למסגרת נתונים
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        # Handle errors / טיפול בשגיאות
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()




# Sidebar filters for table selection and filtering
# פילטרים בצד ימין לבחירת טבלה וסינון
st.sidebar.title("Filters")  # Sidebar title / כותרת לפילטרים בצד
table_options = [
    "promotion_table", "absence_table", "Nationality_table", "Seniority_table", "age_range_table", "exterior_worker_table", "handicap_table", "other_condition_table"
]  # List of available tables / רשימת טבלאות זמינות
selected_table = st.sidebar.selectbox("Select Table for Analysis", table_options)  # Table selection / בחירת טבלה
print(f'{selected_table=}')

# Load data from the selected table
# טעינת נתונים מהטבלה שנבחרה
data = load_data(selected_table)



# If the data is not empty, display the dashboard
# אם הנתונים אינם ריקים, הצג את הדאשבורד
if not data.empty:
    # Filters to refine the data from the selected table
    # פילטרים לסינון נתונים מתוך הטבלה שנבחרה
    gender_filter = st.sidebar.multiselect(
        "GENDER",
        data["GENDER"].unique(),  # Unique gender list / רשימת מגדרים ייחודיים
        default=data["GENDER"].unique()  # Default: All genders / ברירת מחדל: כל המגדרים
    )
    category_filter = st.sidebar.multiselect(
        "Category",
        data["JOB_TYPE"].unique(),  # Unique categories list / רשימת קטגוריות ייחודיות
        default=data["JOB_TYPE"].unique()  # Default: All categories / ברירת מחדל: כל הקטגוריות
    )
    contract_filter = st.sidebar.multiselect(
        "Contract Type",
        data["CONTRACT_TYPE"].unique(),  # Unique contract types / רשימת סוגי חוזה ייחודיים
        default=data["CONTRACT_TYPE"].unique()  # Default: All contract types / ברירת מחדל: כל סוגי החוזים
    )

    # Filter the data based on the user's selections
    # סינון הנתונים בהתבסס על הבחירות של המשתמש
    filtered_data = data[
        (data["GENDER"].isin(gender_filter)) &  # Filter by gender / סינון לפי מגדר
        (data["JOB_TYPE"].isin(category_filter)) &  # Filter by category / סינון לפי קטגוריה
        (data["CONTRACT_TYPE"].isin(contract_filter))  # Filter by contract type / סינון לפי סוג חוזה
    ]

    print(f'{filtered_data=}')
    # Displaying the dashboard title
    # הצגת כותרת הדאשבורד
    st.title("Gender Discrimination Dashboard")
    
    # 1. Salary Analysis / ניתוח שכר
    if selected_table == 'Nationality_table':
        print('Ok, nationality table is running')
    
    
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




    # 2. Promotion Analysis / ניתוח קידומים
    if "PROMOTIONS" in filtered_data.columns:
        st.header("Promotion Analysis")  # Dashboard section title / כותרת חלק הדאשבורד
        # Calculate the number of promotions by category and gender
        # חישוב כמות הקידומים לפי קטגוריה ומגדר
        promotion_data = filtered_data.groupby(["JOB_TYPE", "GENDER"])["PROMOTIONS"].sum().reset_index()
        # Create a bar chart to compare promotions
        # יצירת גרף עמודות להשוואת קידומים
        fig_promotions = px.bar(
            promotion_data,
            x="JOB_TYPE",
            y="PROMOTIONS",
            color="GENDER",
            barmode="group",
            title="Promotion Rates by Gender and Category",
            labels={"PROMOTIONS": "Total Promotions", "JOB_TYPE": "Category"}
        )
        st.plotly_chart(fig_promotions)

        # 3. Representation in Higher Categories / ייצוג בקטגוריות גבוהות
        st.header("Representation in Higher Categories")  # Dashboard section title / כותרת חלק הדאשבורד
        # Calculate representation percentages for each category
        # חישוב אחוזי הייצוג בכל קטגוריה
        representation_data = filtered_data["JOB_TYPE"].value_counts(normalize=True).reset_index()
        representation_data.columns = ["JOB_TYPE", "PERCENTAGE"]
        # Create a pie chart for representation
        # יצירת גרף פאי לייצוג
        fig_representation = px.pie(
            representation_data,
            names="JOB_TYPE",
            values="PERCENTAGE",
            title="Representation by Category"
        )
        st.plotly_chart(fig_representation)

    # 4. Absence Analysis / ניתוח היעדרויות
    if "ABSENCES" in filtered_data.columns:
        st.header("Absence Analysis")  # Dashboard section title / כותרת חלק הדאשבורד
        # Calculate average absences by category and gender
        # חישוב ממוצע ההיעדרויות לפי קטגוריה ומגדר
        absence_data = filtered_data.groupby(["JOB_TYPE", "GENDER"])["ABSENCES"].mean().reset_index()
        # Create a bar chart to compare absences
        # יצירת גרף עמודות להשוואת היעדרויות
        fig_absences = px.bar(
            absence_data,
            x="JOB_TYPE",
            y="ABSENCES",
            color="GENDER",
            barmode="group",
            title="Average Absences by Gender and Category",
            labels={"ABSENCES": "Average Absences", "JOB_TYPE": "Category"}
        )
        st.plotly_chart(fig_absences)

    # 5. Contract Type Analysis / ניתוח סוגי חוזה
    st.header("Contract Type Distribution")  # Dashboard section title / כותרת חלק הדאשבורד
    # Calculate the number of employees by contract type and gender
    # חישוב כמות העובדים לפי סוג חוזה ומגדר
    contract_data = filtered_data.groupby(["CONTRACT_TYPE", "GENDER"])["CONTRACT_TYPE"].count().reset_index(name="COUNT")
    # Create a bar chart for contract types
    # יצירת גרף עמודות לסוגי חוזה
    fig_contract = px.bar(
        contract_data,
        x="CONTRACT_TYPE",
        y="COUNT",
        color="GENDER",
        barmode="group",
        title="Contract Type Distribution by Gender",
        labels={"COUNT": "Number of Employees", "CONTRACT_TYPE": "Contract Type"}
    )
    st.plotly_chart(fig_contract)
else:
    # Display when no data matches the filters / תצוגה כאשר אין נתונים מתאימים
    st.warning(f"No data available for the selected table: {selected_table}")

