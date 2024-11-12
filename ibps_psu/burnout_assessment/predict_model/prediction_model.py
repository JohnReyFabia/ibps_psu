import numpy as np
import os
import joblib


def map_burnout_profile(ex_high, cy_high, ef_high):
    if ex_high and cy_high and not ef_high:
        return "Burned out"
    elif ex_high and not cy_high and ef_high:
        return "Overextended"
    elif not ex_high and cy_high and ef_high:
        return "Disengaged"
    elif not ex_high and not cy_high and not ef_high:
        return "Ineffective"
    elif ex_high and cy_high and ef_high:
        return "Overextended and Disengaged"
    elif ex_high and not cy_high and not ef_high:
        return "Overextended and Ineffective"
    elif not ex_high and cy_high and not ef_high:
        return "Disengaged and Ineffective"
    elif not ex_high and not cy_high and ef_high:
        return "Engaged"
    else:
        return "Unmatched"


def multiple_linear_regression(X, y, learning_rate=0.01, epochs=1000):
    num_samples, num_features = X.shape
    weights = np.zeros(num_features)
    bias = 0

    for epoch in range(epochs):
        # Predictions
        y_pred = np.dot(X, weights) + bias

        # Derivatives
        d_weights = -(2 / num_samples) * np.dot(X.T, (y_pred - y))
        d_bias = -(2 / num_samples) * np.sum(y_pred - y)

        # Update parameters
        weights -= learning_rate * d_weights
        bias -= learning_rate * d_bias

    return weights, bias


def load_trained_model():
    try:
        # Get the base directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)

        # Define the path to the 'model' directory
        model_dir = os.path.join(base_dir, "model")

        # Load the trained model
        weights_path = os.path.join(model_dir, "model_weights.joblib")
        bias_path = os.path.join(model_dir, "model_bias.joblib")

        weights = joblib.load(weights_path)
        bias = joblib.load(bias_path)

        return weights, bias
    except FileNotFoundError:
        print("Trained model files not found!")
        return None, None


def predict_burnout_profiles(test_data, weights, bias):
    y_pred_test = np.dot(test_data, weights) + bias
    predicted_profiles = [map_burnout_profile(*data) for data in test_data]
    return predicted_profiles


if __name__ == "__main__":
    # Manually create a fake dataset for training
    fake_data_train = np.array(
        [
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
            [1, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 0, 0],
            [0, 1, 1],
            [1, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ]
    )

    # Corresponding target variable using the provided function
    target_variable_train = np.array(
        [map_burnout_profile(*data) for data in fake_data_train]
    )

    # Define label mapping
    label_mapping = {
        "Burned out": 0,
        "Overextended": 1,
        "Disengaged": 2,
        "Ineffective": 3,
        "Overextended and Disengaged": 4,
        "Overextended and Ineffective": 5,
        "Disengaged and Ineffective": 6,
        "Engaged": 7,
        "Unmatched": -1,
    }

    # Convert target variable to numerical labels
    target_variable_train = np.array(
        [label_mapping[label] for label in target_variable_train]
    )

    # Reshape features for modeling
    X_train = fake_data_train

    # Train the model
    weights, bias = multiple_linear_regression(X_train, target_variable_train)

    # Check if the 'model' directory exists; if not, create it
    if not os.path.exists("model"):
        os.makedirs("model")
    # Save the trained model
    joblib.dump(weights, "model/model_weights.joblib")
    joblib.dump(bias, "model/model_bias.joblib")
