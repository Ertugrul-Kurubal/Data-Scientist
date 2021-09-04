WELCOME!
Welcome to "Fraud Detection Project". This is the last project of the Capstone Series.

One of the challenges in this project is the absence of domain knowledge. So without knowing what the column names are, you will only be interested in their values. The other one is the class frequencies of the target variable are quite imbalanced.

You will implement Logistic Regression, Random Forest, Neural Network algorithms and SMOTE technique. Also visualize performances of the models using Seaborn, Matplotlib and Yellowbrick in a variety of ways.

At the end of the project, you will have the opportunity to deploy your model by Flask API.

Before diving into the project, please take a look at the Determines and Tasks.

NOTE: This tutorial assumes that you already know the basics of coding in Python and are familiar with model deployement (flask api) as well as the theory behind Logistic Regression, Random Forest, Neural Network.
#Determines
The datasets contains transactions made by credit cards in September 2013 by european cardholders. This dataset presents transactions that occurred in two days, where it has 492 frauds out of 284,807 transactions. The dataset is highly unbalanced, the positive class (frauds) account for 0.172% of all transactions.

Feature Information:

Time: This feature is contains the seconds elapsed between each transaction and the first transaction in the dataset.

Amount: This feature is the transaction Amount, can be used for example-dependant cost-senstive learning.

Class: This feature is the target variable and it takes value 1 in case of fraud and 0 otherwise.

The aim of this project is to predict whether a credit card transaction is fraudulent. Of course, this is not easy to do. First of all, you need to analyze and recognize your data well in order to draw your roadmap and choose the correct arguments you will use. Accordingly, you can examine the frequency distributions of variables. You can observe variable correlations and want to explore multicollinearity. You can show the distribution of the target variable's classes over other variables. Also, it is useful to take missing values and outliers.

After these procedures, you can move on to the model building stage by doing the basic data pre-processing you are familiar with.

Start with Logistic Regression and evaluate model performance. You will apply the SMOTE technique used to increase the sample for unbalanced data. Next, rebuild your Logistic Regression model with SMOTE applied data to observe its effect.

Then, you will use three different algorithms in the model building phase. You have applied Logistic Regression and Random Forest in your previous projects. However, the Deep Learning Neural Network algorithm will appear for the first time.

In the final step, you will deploy your model using Flask API.
