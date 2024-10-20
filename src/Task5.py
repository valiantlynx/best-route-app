import numpy as np

# Step 1: Data Generation
rng = np.random.default_rng(42)  # Random number generator
n_examples = 40  # Number of examples

xs = rng.uniform(size=(n_examples, 2))  # Generate 40x2 random input data
b = (xs > 0.5).astype(int)  # Convert xs to binary values based on whether each value > 0.5
ys_true = np.logical_xor(b[:, 0], b[:, 1]).astype(int)  # Compute the XOR for the true labels


# Step 2: Define the Decision Tree with Fortuna Algorithm (randomized split selection)
class DecisionTreeFortuna:
    def __init__(self, depth=0, max_depth=4, num_random_splits=3):
        self.depth = depth
        self.max_depth = max_depth
        self.num_random_splits = num_random_splits  # Number of random splits to sample
        self.feature_index = None
        self.threshold = None
        self.left = None
        self.right = None
        self.predicted_class = None

    def fit(self, X, y):
        if self.depth >= self.max_depth or len(np.unique(y)) == 1:
            # If the depth limit is reached or all labels are the same, make a leaf node
            self.predicted_class = np.argmax(np.bincount(y))
        else:
            # Find the best split randomly sampled (Fortuna style)
            num_samples, num_features = X.shape
            best_gini = float('inf')
            best_index, best_threshold = None, None

            # Randomly sample features and thresholds
            for _ in range(self.num_random_splits):
                feature_index = np.random.randint(0, num_features)  # Random feature index
                threshold = np.random.uniform(np.min(X[:, feature_index]),
                                              np.max(X[:, feature_index]))  # Random threshold

                left_mask = X[:, feature_index] <= threshold
                right_mask = X[:, feature_index] > threshold
                gini = self._gini_index(y[left_mask], y[right_mask])

                if gini < best_gini:
                    best_gini = gini
                    best_index = feature_index
                    best_threshold = threshold

            if best_index is not None:
                # Set the best split
                self.feature_index = best_index
                self.threshold = best_threshold

                left_mask = X[:, self.feature_index] <= self.threshold
                right_mask = X[:, self.feature_index] > self.threshold

                # Recursively create the left and right subtrees
                self.left = DecisionTreeFortuna(depth=self.depth + 1, max_depth=self.max_depth,
                                                num_random_splits=self.num_random_splits)
                self.right = DecisionTreeFortuna(depth=self.depth + 1, max_depth=self.max_depth,
                                                 num_random_splits=self.num_random_splits)

                self.left.fit(X[left_mask], y[left_mask])
                self.right.fit(X[right_mask], y[right_mask])
            else:
                # If no split is found, create a leaf node
                self.predicted_class = np.argmax(np.bincount(y))

    def predict(self, X):
        if self.predicted_class is not None:
            return np.array([self.predicted_class] * len(X))
        else:
            left_mask = X[:, self.feature_index] <= self.threshold
            right_mask = X[:, self.feature_index] > self.threshold
            y_pred = np.zeros(len(X), dtype=int)

            y_pred[left_mask] = self.left.predict(X[left_mask])
            y_pred[right_mask] = self.right.predict(X[right_mask])

            return y_pred

    def _gini_index(self, left_y, right_y):
        # Calculate the Gini index for a split
        def gini(y):
            if len(y) == 0:
                return 0
            p = np.bincount(y) / len(y)
            return 1 - np.sum(p ** 2)

        n = len(left_y) + len(right_y)
        gini_left = gini(left_y)
        gini_right = gini(right_y)
        return (len(left_y) / n) * gini_left + (len(right_y) / n) * gini_right


# Step 3: Train the decision tree using Fortuna algorithm (randomized splits)
tree_fortuna = DecisionTreeFortuna(max_depth=4, num_random_splits=3)
tree_fortuna.fit(xs, ys_true)

# Step 4: Make predictions
ys_pred_fortuna = tree_fortuna.predict(xs)

# Step 5: Evaluate accuracy
accuracy_fortuna = np.sum(ys_pred_fortuna == ys_true) / len(ys_true)

# Step 6: Print results
print(f"Predictions: {ys_pred_fortuna}")
print(f"True Labels: {ys_true}")
print(f"Accuracy: {accuracy_fortuna * 100:.2f}%")
