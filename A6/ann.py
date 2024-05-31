"""CS 131 A6 - ANN IRIS SPECIES CLASSIFICATION
    Author: Perucy Mussiba
    Date: May 1st 2024
    Purpose: The program implements artificial neural networks to classify Iris plant species
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

learning_rate = 0.1
epochs = 400

"""
    weight initializer
    purpose: initialize weights and biases
    arguments: a list of number of neurons in each layer
    returns: a matrix of weights and biases
"""
def weight_initializer(layers):
    num_layers = len(layers)
    weight = []

    for i in range(1, num_layers):
        w = [[np.random.uniform(-1, 1) for j in range(layers[i - 1] + 1)]
             for z in range(layers[i])]
        weight.append(np.matrix(w))

    return weight


"""
    sigmoid
    purpose: calculate activation using sigmoid function
    arguments: input value to a neuron
    returns: activation value
"""
def sigmoid(value):
    return 1 / (1 + np.exp(-value))


"""
    forward propagation
    arguments: input (x) values, weight and number of layers
    purpose: implements forward propagation
    returns: a list of activation of neurons in each layer
"""
def forwardpropagation(x, weight, num_layers):
    activations = [x]  # list for activations of each layer including the input layer
    x_input = x  # the input at each layer
    for i in range(num_layers):
        a_value = np.dot(x_input, weight[i].T)
        active = sigmoid(a_value)
        activations.append(active)
        x_input = np.append(1, active)

    return activations


"""
    backwardpropagation
    purpose: implements backward propagation
    arguments: input (x) values, weight, activations list and number of layers
    returns: updated weights
"""
def backwardpropagation(y, weight, activations_list, num_layers):
    # error of the output layer
    error = np.matrix(y - activations_list[-1])

    for i in range(num_layers, 0, -1):
        # assessing the current activation value
        curr_activ = activations_list[i]

        # if not input layer append the bias term and activations of next layer
        if i > 1:
            prev_activ = np.append(1, activations_list[i - 1])
        else:
            prev_activ = activations_list[0]

        # error for hidden layers
        sigmoid_derivative = np.multiply(curr_activ, 1 - curr_activ)
        delta = np.multiply(error, sigmoid_derivative)

        # Updating weights
        weight[i - 1] += (learning_rate * np.multiply(delta.T, prev_activ))

        # updating error value excluding the bias
        error = np.dot(delta, np.delete(weight[i - 1], [0], axis=1))

    return weight


"""
    train_function
    purpose: implements training function of the ANN
    arguments: x (input values), y (output values), weights
    returns: updated weights
"""
def train_function(x, y, weight):
    num_layers = len(weight)

    # forward and backward propagation
    for i in range(len(x)):
        x_t = x[i]
        y_t = y[i]
        x_t = np.matrix(np.append(1, x_t))
        activations_list = forwardpropagation(x_t, weight, num_layers)
        weight = backwardpropagation(y_t, weight, activations_list, num_layers)

    return weight

"""
    accuracy_function
    purpose: determines the accuracy of a prediction in ANN
    arguments: input. predicted value and weights
    returns: the accuracy of the prediction
"""
def accuracy_function(x_dt, y_dt, weight):
    correct = 0
    for i in range(len(x_dt)):
        x_value = x_dt[i]
        y_value = list(y_dt[i])
        if y_value == (prediction_function(x_value, weight)):
            correct += 1
    return correct / len(x_dt)

"""
    prediction_function
    purpose: predicts the correctness of the validation set
    arguments: validation set and weights
    returns: the predicted output of validation set
"""
def prediction_function(x_valdt, weight):
    num_layers = len(weight)
    x_valdt = np.append(1, x_valdt)
    activations = forwardpropagation(x_valdt, weight, num_layers)
    result = activations[-1].A1
    max_act = result[0]
    index = 0
    for i in range(1, len(result)):
        if result[i] > max_act:
            max_act = result[i]
            index = i
    y_vdt = [0 for i in range(len(result))]
    y_vdt[index] = 1
    return y_vdt


"""
    neuralnetwork_function
    purpose: function containing the training loop, calls initializing weights and biases function
    arguments: training, validation data and list of number of neurons in each layer
    returns: accuracy of prediction
"""
def neuralnetwork_function(x, y, x_valdt, y_valdt, layers):

    # initializing weights
    weights_list = weight_initializer(layers)

    for epoch in range(1, epochs + 1):
        weight = train_function(x, y, weights_list)

        if epoch % 100 == 0:
            print("Epoch value: ", epoch)
            print("training data accuracy: ", accuracy_function(x, y, weight))
            print("validation data accuracy: ", accuracy_function(x_valdt, y_valdt, weight))
    return weights_list


"""
                    MAIN FUNCTION OF THE PROGRAM  
"""
if __name__ == '__main__':
    # data preprocessing
    iris = pd.read_csv('ANN - Iris data.txt', header=None)
    iris = iris.rename(columns={0: 'SepalL', 1: 'SepalW', 2: 'PetalL', 3: 'PetalW', 4: 'Species'})
    x_data = np.array(iris[['SepalL', 'SepalW', 'PetalL', 'PetalW']])
    y_data = OneHotEncoder(sparse_output=False).fit_transform(np.array(iris.Species).reshape(-1, 1))

    # set sizes of test and validation sets
    test_size = 0.15
    val_size = 0.1

    # data splitting
    # splitting into test and training sets
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=test_size)
    # splitting training into validation and training sets
    x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=val_size)

    # initializing the number of input and output neurons
    num_inputs = len(x_data[0])
    num_outputs = len(y_data[0])

    # initializing layers as a list
    layers_list = [num_inputs, 5, 10, num_outputs]

    # neural network function
    net_weights = neuralnetwork_function(x_train, y_train, x_test, y_test, layers_list)

    iris_features = []
    feature = 0
    print('Enter plant feature')
    for i in range(4):
        if i == 0:
            user_input = input('Enter the Sepal Length: ')
            feature = float(user_input)
        elif i == 1:
            user_input = input('Enter the Sepal Width: ')
            feature = float(user_input)
        elif i == 2:
            user_input = input('Enter the Petal Length: ')
            feature = float(user_input)
        else:
            user_input = input('Enter the Petal Width: ')
            feature = float(user_input)

        iris_features.append(feature)

    iris_data = np.array(iris_features)
    pred_value = prediction_function(iris_data, net_weights)

    if pred_value[0] == 1:
        print('Predicted iris specie is Iris Setosa')
    elif pred_value[1] == 1:
        print('Predicted iris specie is Iris Versicolor')
    else:
        print('Predicted iris specie is Iris Virginica')
