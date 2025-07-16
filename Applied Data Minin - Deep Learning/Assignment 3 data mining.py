import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Simulate a Titanic dataset
np.random.seed(42)
data = pd.DataFrame({
    'Survived': np.random.choice([0, 1], size=100),
    'Pclass': np.random.choice([1, 2, 3], size=100),
    'Sex': np.random.choice(['male', 'female'], size=100),
    'Age': np.random.uniform(1, 80, size=100),
    'SibSp': np.random.randint(0, 5, size=100),
    'Parch': np.random.randint(0, 5, size=100),
    'Fare': np.random.uniform(15, 100, size=100),
    'Embarked': np.random.choice(['C', 'Q', 'S'], size=100)
})

# Introduce some missing values
data.loc[::10, 'Age'] = np.nan
data.loc[::15, 'Embarked'] = np.nan

# Define preprocessors
numeric_features = ['Age', 'SibSp', 'Parch', 'Fare']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', MinMaxScaler())
])

categorical_features = ['Pclass', 'Sex', 'Embarked']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combine preprocessors
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Split the data into training and testing sets
X = data.drop('Survived', axis=1)
y = data['Survived']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit and transform the training data and transform the test data
X_train_prepared = preprocessor.fit_transform(X_train)
X_test_prepared = preprocessor.transform(X_test)

print("Training features shape:", X_train_prepared.shape)
print("Testing features shape:", X_test_prepared.shape)
