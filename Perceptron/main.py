import numpy as np
import matplotlib.pyplot as plt

def label_point(x,y):
    """
    Označení bodu podle přímky y = 3x + 2
    """
    l_y = 3*x + 2 # přímka
    if y > l_y:
        return 1 # nad přímkou
    elif y < l_y:
        return -1 # pod přímkou
    else:
        return 0 # na přímce
def vizualize_data(point, label, w1, w2, bias):
    """
    Vykreslení bodu a rozhodovací hranice
    """
    plt.figure(figsize=(8,5))

    # Barevné značení bodů podle labelu
    plt.scatter(point[label == 1][:,0], point[label == 1][:,1], c='r', label='1')
    plt.scatter(point[label == -1][:,0], point[label == -1][:,1], c='b', label='-1')
    plt.scatter(point[label == 0][:,0], point[label == 0][:,1], c='g', label='0')

    # Přímka y = 3x + 2
    x = np.linspace(-10, 10, 100)
    y = 3*x + 2
    plt.plot(x, y, '-k', label='y=3x+2')

    # Vykreslení rozhodovací hranice
    y_perceptron = -(w1/w2)*x - (bias/w2)
    plt.plot(x, y_perceptron, '--r', label='Perceptron Line')

    plt.legend()
    plt.title('Perceptron')
    plt.show()
def train_perceptron(point, label, lr=0.1, epochs=100):
    """
    Trénování perceptronu
    """
    w1 = 0.2 # Počáteční váha pro x
    w2 = 0.4 # Počáteční váha pro y
    bias = 0.5 # Počáteční bias

    for epoch in range(epochs):
        y_guess = np.sign(point[:,0]*w1 + point[:,1]*w2 + bias) # Výpočet predikce
        error = label - y_guess # Výpočet chyby
        
        if np.all(error == 0): # Pokud nejsou chyby konec trénování
            break

        for i in range(len(point)): # Aktualizace vah a biasu
            w1 += lr*error[i]*point[i,0]
            w2 += lr*error[i]*point[i,1]
            bias += lr*error[i]
    return w1, w2, bias
        
def predict_perceptron(w1, w2, bias, point):
    """
    Predikce pomocí naučeného perceptronu
    """
    return np.sign(point[:,0]*w1 + point[:,1]*w2 + bias)
    
if __name__ == "__main__":
    point = np.random.uniform(-10,10,(100,2))
    true_label = np.array([label_point(x,y) for x,y in point])
    w1, w2, bias = train_perceptron(point, true_label)
    predict_label = predict_perceptron(w1, w2, bias, point)
    vizualize_data(point, predict_label, w1, w2, bias)