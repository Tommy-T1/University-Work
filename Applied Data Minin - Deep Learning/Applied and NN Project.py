import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, hamming_loss
from sklearn.multioutput import MultiOutputClassifier
from scipy.stats import chi2_contingency
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

# Firstly tried to read data like this but it couldn't read the file that's in the same directory with it 
# data = pd.read_csv("athletes.csv")

# So I used these two small lines below to print the current directory so I can give the full directory to the read statement 
# import os
# print(os.getcwd())

df = pd.read_csv("f:/python workspace/athletes.csv")

# Here we are checking for empty values and their count
null_values = df.isnull().sum()
print(null_values)
print("comment")

# Let's fill in these values with the median
median_weight = df["weight"].median()
df["weight"] = df["weight"].fillna(median_weight)

# Let's check again for empty values
new_null_values = df.isnull().sum()
print(new_null_values)

# Here we see that the values have been filled, now we want to change how the data looks by dropping irrelevant columns
# but first we have to check the columns we have
print(df.columns)
"""
Through checking the columns we can see that some columns are irrelevant to us since another column already shows the same data but in a different form such as 
short name and country_full and nationality_full and other stuff that is not useful to us such as country code
"""

# Here we want to understand the difference between disciplines and function to know if they are relevant or not
print(df['disciplines'].unique())
print('This is a splitter')
print(df['function'].unique())

# Now we want to drop the irrelevant columns 
dropping_columns = ["country_code", "country_full", "nationality_full", "nationality_code", "name_short", "name_tv"]
new_df = df.drop(columns=dropping_columns)

# Now we want to check for duplicates 
duplicates = df.duplicated().sum()
print("Duplicate rows in the DataFrame:")
print(duplicates)
# So there should be no duplicates

# Checking the new columns
print(new_df.columns)

# Now we want to check the correlation between certain categories of data

label_encoders = {}
for column in ['gender', 'country']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Convert 'disciplines' to object type to handle lists
df['disciplines'] = df['disciplines'].astype('object')

df['height_bins'] = pd.qcut(df['height'], q=4, labels=False, duplicates='drop')
df['weight_bins'] = pd.qcut(df['weight'], q=4, labels=False, duplicates='drop')

contingency_gender = pd.crosstab(df['gender'], df['disciplines'])
contingency_height = pd.crosstab(df['height_bins'], df['disciplines'])
contingency_weight = pd.crosstab(df['weight_bins'], df['disciplines'])

chi2_gender, p_gender, dof_gender, expected_gender = chi2_contingency(contingency_gender)
print(f"Chi-Square test results for gender vs. disciplines: Chi2 = {chi2_gender}, p-value = {p_gender}")

chi2_height, p_height, dof_height, expected_height = chi2_contingency(contingency_height)
print(f"Chi-Square test results for height vs. disciplines: Chi2 = {chi2_height}, p-value = {p_height}")

chi2_weight, p_weight, dof_weight, expected_weight = chi2_contingency(contingency_weight)
print(f"Chi-Square test results for weight vs. disciplines: Chi2 = {chi2_weight}, p-value = {p_weight}")

print("The above results show that there is a strong relation between an athlete's height and discipline and their gender and discipline")
print("Based on that we now want to train the machine to categorize the discipline of an athlete based on their height and gender")

# Ensure that 'disciplines' are correctly formatted for multi-label (assuming they are separated by a comma)
df['disciplines'] = df['disciplines'].apply(lambda x: x.split(',') if isinstance(x, str) else x)

# Use MultiLabelBinarizer to transform the disciplines column into a multi-label format
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['disciplines'])

# Select features
X = df[['height', 'gender']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### Decision Tree Model ###
# Initialize the Decision Tree Classifier with MultiOutputClassifier wrapper
decision_tree = DecisionTreeClassifier(random_state=42)
multi_output_clf = MultiOutputClassifier(decision_tree)

# Use GridSearchCV for hyperparameter tuning
param_grid = {
    'estimator__criterion': ['gini', 'entropy'],
    'estimator__max_depth': [None, 10, 20, 30],
    'estimator__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(multi_output_clf, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best estimator after tuning
best_model = grid_search.best_estimator_

# Make predictions on the test set
y_pred_dt = best_model.predict(X_test)

# Evaluate the Decision Tree model
print("Best Parameters (Decision Tree):", grid_search.best_params_)
print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred_dt))
print("Decision Tree Hamming Loss:", hamming_loss(y_test, y_pred_dt))
print("Decision Tree Classification Report:")
print(classification_report(y_test, y_pred_dt, target_names=mlb.classes_, zero_division=1))

### Neural Network Model (Keras) ###

# Define the neural network model
model = Sequential()
model.add(Dense(16, input_dim=X_train.shape[1], activation='relu'))  # Hidden layer with 16 neurons
model.add(Dense(32, activation='relu'))  # Additional hidden layer with 32 neurons
model.add(Dense(y_train.shape[1], activation='sigmoid'))  # Output layer with sigmoid activation for multi-label classification

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=10, verbose=1)

# Make predictions on the test set
y_pred_nn = model.predict(X_test)
y_pred_nn = (y_pred_nn > 0.5).astype(int)  # Convert probabilities to binary predictions

# Evaluate the Neural Network model
accuracy_nn = accuracy_score(y_test, y_pred_nn)
hamming_loss_nn = hamming_loss(y_test, y_pred_nn)

print(f"Neural Network Test Accuracy: {accuracy_nn}")
print(f"Neural Network Test Hamming Loss: {hamming_loss_nn}")
print("Neural Network Test Classification Report:")
print(classification_report(y_test, y_pred_nn, target_names=mlb.classes_, zero_division=1))
