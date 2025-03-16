import numpy as np
import matplotlib.pyplot as plt
def sigmoid(x):
    """
    Sigmoidní aktivační funkce
    """
    return 1/(1 + np.exp(-x))

def forward_pass(wH, bH, wO, bO, x, y):
    """
    Výpočet  výstupu dopředného průchodu neuronovou sítí
    """
    netH = np.dot(x, wH) + bH * 1
    outH = sigmoid(netH)
    
    netO = np.dot(outH, wO) + bO * 1
    outO = sigmoid(netO)

    errTotal = np.sum(0.5*(y - outO)**2)
    return errTotal, outO, outH

def backward_pass(y, outO, outH, wO, x):
    """
    Výpočet gradientu pro zpětnou propagaci
    """
    delta0 = -(y - outO)
    delta1 = outO * (1 - outO)
    delta2 = outH
    
    delta_output = (delta0 * delta1 * delta2).reshape((2, 1))
    delta_hidden = (delta0 * delta1 * wO) * (outH * (1 - outH)) * x

    return delta_output, delta_hidden

def update_weights(delta_output, delta_hidden, lr, wO, wH, bH, bO):
    """
    Aktualizace vah a biasů na základě gradientu
    """
    wO -= lr * delta_output
    bO -= lr * np.sum(delta_output)
    wH -= lr * delta_hidden
    bH -= lr * np.sum(delta_hidden)

def plot_decision_boundary(wH, bH, wO, bO):
    """
    Vykreslení rozhodovací hranice
    """
    x_min, x_max = -0.5, 1.5
    y_min, y_max = -0.5, 1.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
                            np.arange(y_min, y_max, 0.01))
    Z = np.c_[xx.ravel(), yy.ravel()]
    Z = np.array([forward_pass(wH, bH, wO, bO, z, 0)[1] for z in Z])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, levels=[0, 0.5, 1], alpha=0.2, colors=['blue', 'red'])
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Decision Boundary')
    
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    for i in range(len(x)):
        plt.scatter(x[i][0], x[i][1], c='green' if y[i] == 1 else 'yellow', edgecolors='k')
    

def XOR_problem(x, y, lr=0.1, epochs=4_000):
    """
    Trénování neuronové sítě na XOR problém
    :param x: Vstupní data
    :param y: Očekávané výstupy
    :param lr: Learning rate
    :param epochs: Počet epoch
    """
    np.random.seed(81)
    wH = np.random.uniform(-1,1,(2,2)) # Váhy pro skrytou vrstvu
    bH = np.random.uniform(-1,1,(1,2)) # Bias pro skrytou vrstvu
    wO = np.random.uniform(-1,1,(2,1)) # Váhy pro výstupní vrstvu
    bO = np.random.uniform(-1,1,(1,1)) # Bias pro výstupní vrstvu
    print("Initial Weights: ", wH, bH, wO, bO)

    errors = []

    for epoch in range(epochs):
        final_error = 0
        for i in range(len(x)):
            err, outO, outH = forward_pass(wH, bH, wO, bO, x[i], y[i])
            delta_output, delta_hidden = backward_pass(y[i], outO, outH, wO, x[i])
            update_weights(delta_output, delta_hidden, lr, wO, wH, bH, bO)
            final_error += err
        errors.append(final_error)
        if epoch % 1000 == 0:
            print("Epoch: ", epoch)
            print("Error: ", final_error)
        
    print("Final Error: ", final_error)
    for i in range(len(x)):
        print("Input: ", x[i], "Output: ", np.round(forward_pass(wH, bH, wO, bO, x[i], y[i])[1]), "Expected: ", y[i])


    plot_decision_boundary(wH, bH, wO, bO)
    plt.figure()
    plt.plot(errors)
    plt.xlabel("Epoch")
    plt.ylabel("Total Error")
    plt.title("Training Error Progression")
    plt.show()

if __name__ == "__main__":
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    XOR_problem(x, y)

