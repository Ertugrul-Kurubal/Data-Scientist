import streamlit as st
from PIL import Image
import pickle
import pandas as pd

# Title
st.header("Churn Prediction")
st.subheader("Employee Churn Analysis")

# Inputs
st.sidebar.header("Features Selection")
depertment = st.sidebar.selectbox('Department', ['sales', 'accounting', 'hr', 'technical', 'support', 'management', 'IT', 'product_mng', 'marketing', 'RandD'])
salary = st.sidebar.selectbox('Salary', ['low', 'medium', 'high'])
satisfaction_level = st.sidebar.slider("Satisfaction",0,100,1)
last_evaluation = st.sidebar.slider("Last Evaluation",0,100,1)
number_project = st.sidebar.slider("Project Number",0,10,1)
average_montly_hours = st.sidebar.slider("Average Montly Working Hours",70,320,1)
time_spend_company = st.sidebar.slider("Time Spend In Company Year",1,25,1)
work_accident = st.sidebar.radio('Work Accident', ['Yes', 'No'])
promotion_last_5years = st.sidebar.radio('Promotion Last 5 Years', ['Yes', 'No'])

if work_accident == "Yes":
    work_accident_1 = 1
else:
    work_accident_1 = 0

if promotion_last_5years == "Yes":
    promotion_last_5years_1 = 1
else:
    promotion_last_5years_1 = 0
    
satisfaction_level_1 = round(satisfaction_level/100, 2)
last_evaluation_1 = round(last_evaluation/100, 2)

# Image
img = Image.open("D:\Data Scientist\Data Science\Machine-Learning\Project\Capstone Project\Churn Prediction\Streamlit\Churn.png")
st.image(img, caption="Churn Analysis")

pred_model = st.selectbox('Select ML Model', ["GradientBoostingClassifier","RandomForestClassifier"])

if pred_model == "RandomForestClassifier":
    model = pickle.load(open("rf_final_model.pkl", "rb"))
else:
    model = pickle.load(open("gb_final_model.pkl", "rb"))

X_columns = pickle.load(open("Xcolums.pkl", "rb"))

# Data
deparment_assignee = {'sales':0, 'accounting':1, 'hr':2, 'technical':3, 'support':4, 'management':5, 'IT':6, 'product_mng':7, 'marketing':8, 'RandD':9}

salary_assignee = {'low':0, 'medium':1, 'high':2}


my_dict = {'satisfaction_level':satisfaction_level_1,
           'last_evaluation':last_evaluation_1, 
           'number_project':number_project,
           'average_montly_hours':average_montly_hours,
           'time_spend_company':time_spend_company,
           'work_accident':work_accident_1,
           'promotion_last_5years':promotion_last_5years_1,
           'department':depertment, 
           'salary':salary}

my_dict_1 = pd.DataFrame.from_dict([my_dict])
my_dict_1[['salary','department']] = pd.concat([my_dict_1.salary.map(salary_assignee),my_dict_1.department.map(deparment_assignee)],axis=1)
# my_dict_1


st.table(my_dict_1)

# st.dataframe(my_dict_1)

# Predict
pred_result = model.predict(my_dict_1)

if pred_result == 0:
    pred_1 = "No"
else:
    pred_1 = "Yes"

# Button
if st.button("Predict"):
    prediction = pred_1    
    if prediction == "Yes":
        st.error("Will the employee leave? : '{}'".format(prediction))
    else:
        st.success("Will the employee leave? : '{}'".format(prediction))