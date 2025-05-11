import matplotlib.pyplot as plt

class BifurcationVisualizer:
    def __init__(self, logistic_map_instance, predictor_instance=None):
        self.logistic_map = logistic_map_instance
        self.predictor = predictor_instance

    def _generate_bifurcation_data(self, a_values_plot, num_total_iterations_plot, num_transients_plot, initial_x_plot, source="actual"):
        bifurcation_a_coords = []
        bifurcation_x_coords = []

        for i, a_val in enumerate(a_values_plot):
            if (i + 1) % 100 == 0:
                 print(f"Generování dat pro bifurkační diagram ({source}): {i+1}/{len(a_values_plot)} hodnot 'a' zpracováno.")

            if source == "actual":
                points = self.logistic_map.generate_attractor_points(
                    a_val, num_total_iterations_plot, num_transients_plot, initial_x_plot
                )
            elif source == "predicted" and self.predictor:
                points = self.predictor.generate_predicted_attractor_points(
                    a_val, num_total_iterations_plot, num_transients_plot, initial_x_pred=initial_x_plot
                )
            else:
                raise ValueError("Neplatný zdroj (source) nebo není nastaven prediktor.")

            for p in points:
                bifurcation_a_coords.append(a_val)
                bifurcation_x_coords.append(p)
        return bifurcation_a_coords, bifurcation_x_coords

    def plot_diagrams(self, a_values_plot, num_total_iterations_plot, num_transients_plot, initial_x_plot=0.5, plot_predicted_flag=True):
        plt.style.use('seaborn-v0_8-whitegrid') 
        fig_height = 12 if plot_predicted_flag and self.predictor else 6
        plt.figure(figsize=(14, fig_height))

        print("Generování dat pro skutečný bifurkační diagram...")
        actual_a, actual_x = self._generate_bifurcation_data(
            a_values_plot, num_total_iterations_plot, num_transients_plot, initial_x_plot, source="actual"
        )
        
        ax1_idx = (2, 1, 1) if plot_predicted_flag and self.predictor else (1, 1, 1)
        plt.subplot(*ax1_idx)
        plt.plot(actual_a, actual_x, ',k', alpha=0.3, markersize=0.5)
        plt.title("Skutečný bifurkační diagram logistické mapy", fontsize=14)
        plt.xlabel("Parametr $a$", fontsize=12)
        plt.ylabel("$x$", fontsize=12)
        plt.xlim(a_values_plot.min(), a_values_plot.max())
        plt.ylim(0, 1)

        if plot_predicted_flag and self.predictor:
            print("\nGenerování dat pro predikovaný bifurkační diagram...")
            predicted_a, predicted_x = self._generate_bifurcation_data(
                a_values_plot, num_total_iterations_plot, num_transients_plot, initial_x_plot, source="predicted"
            )
            plt.subplot(2, 1, 2)
            plt.plot(predicted_a, predicted_x, ',r', alpha=0.3, markersize=0.5) 
            plt.title("Predikovaný bifurkační diagram (pomocí sklearn modelu)", fontsize=14)
            plt.xlabel("Parametr $a$", fontsize=12)
            plt.ylabel("Predikovaný $x$", fontsize=12)
            plt.xlim(a_values_plot.min(), a_values_plot.max())
            plt.ylim(0, 1) 

        plt.tight_layout(pad=2.0)
        plt.show()