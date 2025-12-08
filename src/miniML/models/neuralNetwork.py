# Not comfortable with this structure, but will do for now
import numpy as np 

class NeuralNetwork:
    def __init__(self, X, y, type: str, epochs: int, lr: float, layers: list):
        self.type = type # "binary", "multi", "regression"
        self.epochs = epochs
        self.learn_rate = lr
        self.network = {"weights":[], "biases":[], "activations":[]}
        self.X = X 
        self.y = y 

        # Change to = layers when finished 
        self.layers = layers
        self.init_network()


    # TODO: Split into three functions, one for size, weights & biases, activations 
    def init_network(self) -> None:
        """ Initializing all weights, biases and activations for the network """
        # adding up total "neurons" in network
        input = self.X.shape[1]
        output = self.y.shape[1] if self.type == "multi" else 1 
        hidden = [n[0] for n in self.layers]  # n[0]= num of neurons in layer
        total = [input] + hidden + [output]

        # insert comment
        for n in range(len(total) - 1):   # -1 to connect weights forward one layer
            W = np.random.rand(total[n], total[n+1]) * np.sqrt(2 / total[n])
            b = np.zeros((1, total[n+1])) 
            self.network["weights"].append(W)
            self.network["biases"].append(b)

        # Setting activations for hidden layers and output layer 
        match self.type:
            case "binary": output_activation = "sigmoid"
            case "multi" : output_activation = "softmax"
            case _       : output_activation = "linear" 

        self.network["activations"] = [a[1] for a in self.layers]
        self.network["activations"].append(output_activation)

    
    def forward_pass(self) -> None:
        """
        Performs the forward pass on the neural network, calculating all of 
        dot products and activating each value
        """
        A = self.X 
        self.network["A"] = [A]     # post-activations fed into the next layer 
        self.network["Z"] = []      # Stores pre-activations vals for backprop

        for i in range(len(self.network["weights"])):
            W = self.network["weights"][i]
            b = self.network["biases"][i]
            act = self.network["activations"][i]

            Z = np.dot(A, W) + b 
            A = self.activate(Z, act)     # apply the activation function

            # append for backprop 
            self.network["Z"].append(Z)
            self.network["A"].append(A)

        return A


    def activate(self, Z, activation) -> None:
        """
        Pattern matching for the correct activation function to use depending 
        on the specificed function passed in 
        """
        match activation:
            case "relu":    return self.relu(Z)
            case "sigmoid": return self.sigmoid(Z)
            case "softmax": return self.softmax(Z)
            case "linear":  return Z

    # TODO: Abstract updating out of here
    def backprop(self):
        m = self.y.shape[0]
        L = len(self.network["weights"])
        A = self.network["A"]
        Z = self.network["Z"]
        act = self.network["activations"]
        
        dA = None       # activation derivative val

        # TODO: move this out to a helper function and turn into cases
        if self.type == "binary":
            epsilon = 1e-8 
            A_L = np.clip(A[-1], epsilon, 1-epsilon)
            dA = -(np.divide(self.y, A_L) - np.divide(1-self.y, 1-A_L))
            dZ = dA * self.sigmoid_derivative(Z[-1])
        elif self.type == "multi":
            dZ = A[-1] - self.y
        else: 
            dA = -2*(self.y - A[-1])
            dZ = dA*self.linear_derivative(Z[-1])

        for l in reversed(range(L)):
            A_prev = A[l]
            W = self.network["weights"][l]

            dW = np.dot(A_prev.T, dZ) / m 
            db = np.sum(dZ, axis=0, keepdims=True) / m 

            self.network["weights"][l] -= self.learn_rate * dW 
            self.network["biases"][l] -= self.learn_rate * db

            if l != 0:
                dA = np.dot(dZ, W.T)
                match act[l-1]:
                    case "relu":    dZ = dA * self.relu_derivative(Z[-1])
                    case "sigmoid": dZ = dA * self.sigmoid_derivative(Z[-1])
                    case _:         dZ = dA * self.linear_derivative(Z[-1])

    def fit(self):
        for epoch in range(self.epochs):
            y_pred = self.forward_pass()
            loss = self.loss(self.y, y_pred)
            self.backprop()
            if epoch % 50 == 0 or epoch == self.epochs - 1:
                print(f"Epoch {epoch+1} / {self.epochs}, loss: {loss:.4f}")


    def loss(self, y_true, y_pred):
        m = y_true.shape[0]

        match self.type:
            case "binary": loss = self.binary_cross_entropy(m, y_true, y_pred)
            case "multi" : loss = self.category_cross_entropy(m, y_true, y_pred)
            case _       : loss = self.mean_squared_error(y_true, y_pred)

        return loss


    def binary_cross_entropy(self, m, y_true, y_pred):
        """
        Loss function for binary classification
        """
        epsilon = 1e-8 
        y_pred = np.clip(y_pred, epsilon, 1-epsilon)
        return -1/m * np.sum(y_true * np.log(y_pred) + (1-y_true) * np.log(1-y_pred))


    def category_cross_entropy(self, m, y_true, y_pred):
        """
        Loss function for multi class classification
        """
        epsilon = 1e-8 
        y_pred = np.clip(y_pred, epsilon, 1-epsilon)
        return -1/m * np.sum(y_true * np.log(y_pred))


    def mean_squared_error(self, y_true, y_pred):
        """
        Loss function for regression
        """
        return np.mean((y_true - y_pred) ** 2)


    def update_weights(self):
        pass


    def relu(self, Z):
        """"""
        return np.maximum(0, Z) 


    def relu_derivative(self, Z):
        """Get the derivate of the relu activation"""
        return (Z > 0).astype(float)


    def sigmoid(self, Z):
        """"""
        return 1 / (1 + np.exp(-Z))


    def sigmoid_derivative(self, Z):
        """Get the derivate of the sigmoid activation"""
        s = self.sigmoid(Z)
        return s * (1 - s)


    def linear_derivative(self, Z):
        """Get the derivate of linear regression"""
        return np.ones_like(Z)


    def softmax(self, Z):
        """"""
        z_exp = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return z_exp / np.sum(z_exp, axis=1, keepdims=True)


    # TODO: Rebuild function
    def predict(self, X):
        A = X 
        for i in range(len(self.network["weights"])):
            W = self.network["weights"][i]
            b = self.network["biases"][i]
            act = self.network["activations"][i]

            Z = np.dot(A, W) + b 
            A = self.activate(Z, act)

        if self.type == "binary":
            return (A > 0.5).astype(int)
        elif self.type == "multi":
            return np.argmax(A, axis=1)
        else: 
            return A 
