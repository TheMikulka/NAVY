import numpy as np

class LogisticMap:
    def __init__(self, default_x0=0.5):
        self.default_x0 = default_x0

    @staticmethod
    def _logistic_eq(x, a):
        return a * x * (1 - x)

    def generate_attractor_points(self, a, num_total_iterations, num_transients, initial_x=None):
        if initial_x is None:
            x = self.default_x0
        else:
            x = initial_x

        for _ in range(num_transients):
            x = self._logistic_eq(x, a)

        attractor_points = []
        for _ in range(num_total_iterations - num_transients):
            x = self._logistic_eq(x, a)
            attractor_points.append(x)
        return attractor_points

    def generate_training_data(self, a_values_for_training, n_points_per_a, n_transients_for_data_gen, initial_x_for_data_gen=0.2):
        X_train_samples = []
        y_train_samples = []

        for a_val in a_values_for_training:
            x_current = initial_x_for_data_gen
            for _ in range(n_transients_for_data_gen):
                x_current = self._logistic_eq(x_current, a_val)

            for _ in range(n_points_per_a):
                x_next = self._logistic_eq(x_current, a_val)
                X_train_samples.append([a_val, x_current])
                y_train_samples.append(x_next)
                x_current = x_next
                if not (0 <= x_current <= 1):
                    x_current = np.random.rand() 

        return np.array(X_train_samples), np.array(y_train_samples)
