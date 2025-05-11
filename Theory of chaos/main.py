import numpy as np
from sklearn.neural_network import MLPRegressor
from LogisticMap import LogisticMap
from LogisticMapPredictor import LogisticMapPredictor
from BifurcationVisualizer import BifurcationVisualizer

if __name__ == '__main__':
    a_train_min = 0.0
    a_train_max = 4.0
    num_a_train_points = 200 
    points_per_a_train = 150  
    transients_for_train_data = 500 
    initial_x_train_data = 0.2 

    sklearn_nn_model = MLPRegressor(
        hidden_layer_sizes=(128, 64, 32), 
        activation='relu',
        solver='adam',
        alpha=1e-5, 
        learning_rate_init=0.001,
        max_iter=1000, 
        random_state=42,
        early_stopping=True, 
        n_iter_no_change=50, 
        tol=1e-5, 
        verbose=False 
    )
    use_data_scaling = True 

    a_plot_min = 0.0
    a_plot_max = 4.0
    num_a_plot_points = 1000 
    total_iterations_plot = 600 
    transients_plot = 300      
    initial_x_for_plotting = 0.5 

    logistic_map_gen = LogisticMap(default_x0=initial_x_for_plotting)

    print("Generování trénovacích dat...")
    a_values_for_training = np.linspace(a_train_min, a_train_max, num_a_train_points)
    X_data, y_data = logistic_map_gen.generate_training_data(
        a_values_for_training, points_per_a_train, transients_for_train_data, initial_x_train_data
    )
    print(f"Vygenerováno {X_data.shape[0]} trénovacích vzorků.")

    X_train, y_train = X_data, y_data

    predictor = LogisticMapPredictor(sklearn_nn_model, use_scaling=use_data_scaling)
    print("Trénování modelu...")
    predictor.train(X_train, y_train)

    visualizer = BifurcationVisualizer(logistic_map_gen, predictor)

    a_values_for_plotting = np.linspace(a_plot_min, a_plot_max, num_a_plot_points)

    print("\nVykreslování bifurkačních diagramů...")
    visualizer.plot_diagrams(
        a_values_for_plotting, total_iterations_plot, transients_plot, initial_x_for_plotting
    )

    print("\nHotovo.")