# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from joblib import dump, load  # For model persistence

# Load your data (assuming you have a CSV file named 'data.csv' with columns 'ex_high', 'cy_high', 'ef_high', and 'profile')
data = pd.read_csv('data.csv')

# Data Preparation
X = data[['ex_high', 'cy_high', 'ef_high']]
y = data['profile']

# Label Encoding
le = LabelEncoder()
y = le.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVM Model
svm_model = SVC(kernel='linear', C=1.0)  # You can choose different kernels and hyperparameters
svm_model.fit(X_train, y_train)

# Save the trained model to a file for later use
dump(svm_model, 'svm_model.joblib')

# Make Predictions on new data (assuming you have a DataFrame 'new_data' with the same feature columns)
new_data = pd.read_csv('new_data.csv')
X_new = new_data[['ex_high', 'cy_high', 'ef_high']]
y_new_pred = svm_model.predict(X_new)

# Inverse transform the encoded predictions to get original labels
y_new_pred_labels = le.inverse_transform(y_new_pred)

# You can now use the trained model to predict profiles for new data and handle the predictions as needed.
