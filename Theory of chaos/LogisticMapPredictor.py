import numpy as np
from sklearn.preprocessing import StandardScaler

class LogisticMapPredictor:
    def __init__(self, sklearn_model, use_scaling=True):
        self.model = sklearn_model
        self.use_scaling = use_scaling
        if self.use_scaling:
            self.scaler_X = StandardScaler()
            self.scaler_y = StandardScaler()

    def train(self, X_train, y_train):
        if self.use_scaling:
            X_scaled = self.scaler_X.fit_transform(X_train)
            y_scaled = self.scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()
            self.model.fit(X_scaled, y_scaled)
        else:
            self.model.fit(X_train, y_train)
        print("Trénování modelu dokončeno.")

    def predict_next_x(self, a, current_x):
        input_features = np.array([[a, current_x]])
        if self.use_scaling:
            input_scaled = self.scaler_X.transform(input_features)
            predicted_scaled = self.model.predict(input_scaled)
            predicted_x = self.scaler_y.inverse_transform(predicted_scaled.reshape(-1, 1)).ravel()[0]
        else:
            predicted_x = self.model.predict(input_features)[0]
        
        return np.clip(predicted_x, 0, 1)

    def generate_predicted_attractor_points(self, a, num_total_iterations, num_transients, initial_x_pred=0.5):
        x_pred = initial_x_pred
        for _ in range(num_transients):
            x_pred = self.predict_next_x(a, x_pred)

        predicted_points = []
        for _ in range(num_total_iterations - num_transients):
            x_pred = self.predict_next_x(a, x_pred)
            predicted_points.append(x_pred)
        return predicted_points