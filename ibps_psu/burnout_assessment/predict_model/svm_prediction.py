import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder 
import joblib

# Load the training data
data = pd.read_csv('training_data.csv')

# Use LabelEncoder to encode the target variable
label_encoder = LabelEncoder()
data['profiles_encoded'] = label_encoder.fit_transform(data['profiles'])
print(data['profiles_encoded'])


# Define features and target
features = data[['ex_high', 'cy_high', 'ef_high']]
target = data['profiles_encoded']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Define parameter grid for GridSearchCV
param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
    'gamma': [0.1, 0.01, 0.001, 1],
}

# Use GridSearchCV to find best hyperparameters
grid_search = GridSearchCV(SVC(), param_grid, scoring='accuracy', cv=10)
grid_search.fit(X_train, y_train)

# Get best model and its parameters
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

# Print best parameters
print("Best parameters:", best_params)

# Save the label encoder
label_encoder_filename = 'label_encoder.joblib'
label_encoder_path = os.path.join('model', label_encoder_filename)
joblib.dump(label_encoder, label_encoder_path)

# Save the trained model
def save_trained_model(model, folder='model', filename='trained_model.joblib'):
    # Create the folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Save the trained model to the model folder
    joblib.dump(model, os.path.join(folder, filename))

# Save the train model to a file in the model folder
save_trained_model(best_model, 'model', 'trained_model.joblib')
