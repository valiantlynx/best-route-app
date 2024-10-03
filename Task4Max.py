import numpy as np
import random
import matplotlib.pyplot as plt

#KODE FRA OPPGAVE START
rng = np.random.default_rng(42)
n_examples = 40
xs = np.random.uniform(low=0.0, high=1.0, size=(n_examples, 2))
b = (xs > 0.5).astype(int)
ys_true = np.logical_xor(b[:, 0], b[:, 1]).astype(int)
#KODE FRA OPPGAVE SLUTT

# Decision Tree implementation with randomness
class DecisionTreeNode:
    def __init__(self, depth=0, max_depth=4):
        self.left = None
        self.right = None
        self.feature_index = None
        self.threshold = None
        self.prediction = None
        self.depth = depth
        self.max_depth = max_depth

    def fit(self, X, y):
        # If all labels are the same, make a leaf node
        if np.all(y == y[0]):
            self.prediction = y[0]
            return

        # If maximum depth is reached, make a leaf node with majority class
        if self.depth >= self.max_depth:
            self.prediction = np.round(np.mean(y)).astype(int)
            return

        # Introduce randomness in feature selection
        self.feature_index = random.choice([0, 1])

        # Introduce randomness in threshold selection
        feature_values = X[:, self.feature_index]
        min_val, max_val = feature_values.min(), feature_values.max()
        self.threshold = random.uniform(min_val, max_val)

        # Split the data
        left_indices = feature_values <= self.threshold
        right_indices = feature_values > self.threshold

        # If either side is empty, make a leaf node with majority class
        if len(y[left_indices]) == 0 or len(y[right_indices]) == 0:
            self.prediction = np.round(np.mean(y)).astype(int)
            return

        # Recursively build left and right subtrees
        self.left = DecisionTreeNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.left.fit(X[left_indices], y[left_indices])

        self.right = DecisionTreeNode(depth=self.depth + 1, max_depth=self.max_depth)
        self.right.fit(X[right_indices], y[right_indices])

    def predict(self, x):
        if self.prediction is not None:
            return self.prediction
        if x[self.feature_index] <= self.threshold:
            return self.left.predict(x)
        else:
            return self.right.predict(x)

class DecisionTree:
    def __init__(self, max_depth=4, n_attempts=1000):
        self.max_depth = max_depth
        self.n_attempts = n_attempts
        self.best_tree = None
        self.best_accuracy = 0

    def fit(self, X, y):
        # Try building the tree multiple times to find the best one
        for _ in range(self.n_attempts):
            tree = DecisionTreeNode(max_depth=self.max_depth)
            tree.fit(X, y)
            y_pred = np.array([tree.predict(x) for x in X])
            accuracy = np.mean(y_pred == y)
            if accuracy > self.best_accuracy:
                self.best_accuracy = accuracy
                self.best_tree = tree
            # Early stopping if 100% accuracy is achieved
            if self.best_accuracy == 1.0:
                break

    def predict(self, X):
        return np.array([self.best_tree.predict(x) for x in X])

# Convert inputs and outputs to numpy arrays
X = xs
y = ys_true

# Initialize and train the decision tree
dt = DecisionTree(max_depth=4, n_attempts=1000)
dt.fit(X, y)

# Check the best accuracy achieved
print(f"Best accuracy achieved: {dt.best_accuracy * 100:.2f}%")

# Make predictions on the training data
y_pred = dt.predict(X)

# Calculate accuracy
accuracy = np.mean(y_pred == y)
print(f"Accuracy on training data: {accuracy * 100:.2f}%")

# Display the predictions alongside true labels
for i in range(len(y)):
    print(f"Input: {X[i]}, True Label: {y[i]}, Predicted: {y_pred[i]}")