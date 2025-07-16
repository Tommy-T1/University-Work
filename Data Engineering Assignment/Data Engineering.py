"""Data Engineering Script for State Employee Pay Analysis"""


import pandas as pd

#Loading Data
data = pd.read_csv('2024_State_Employee_Pay.csv')
print(f"Data loaded with {data.shape[0]} rows and {data.shape[1]} columns.")

#Cleaning the data
#Removing duplicates
data_cleaned = data.drop_duplicates()
print(f"Removed duplicates. Rows remaining: {data_cleaned.shape[0]}")

#Ensuring 'YTD Gross Pay' is numeric
if 'YTD Gross Pay' in data_cleaned.columns:
    data_cleaned['YTD Gross Pay'] = pd.to_numeric(data_cleaned['YTD Gross Pay'], errors='coerce')
else:
    raise ValueError("'YTD Gross Pay' column is missing!")

#Drop rows with invalid 'YTD Gross Pay'
data_cleaned = data_cleaned.dropna(subset=['YTD Gross Pay'])
print(f"Invalid 'YTD Gross Pay' rows removed. Rows remaining: {data_cleaned.shape[0]}")

#Drop unnecessary columns
if 'Employee Name' in data_cleaned.columns:
    data_cleaned = data_cleaned.drop(columns=['Employee Name'])
    print("'Employee Name' column dropped.")

#Grouping data by 'Position Title' and 'Agency Name'
output_dir = 'c:/Users/tareq/venv/DE Proj/'
for group_by in ['Position Title', 'Agency Name']:
    group = data_cleaned.groupby(group_by)['YTD Gross Pay'].mean().reset_index()
    group = group.rename(columns={'YTD Gross Pay': 'Average Gross Pay'})
    group.to_csv(f'{output_dir}{group_by.lower().replace(" ", "_")}_grouped.csv', index=False)
    print(f"Grouped data by {group_by} saved to '{output_dir}{group_by.lower().replace(" ", "_")}_grouped.csv'.")