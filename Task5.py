import numpy as np
rng = np.random.default_rng(42)
n_examples = 40

xs = rng.uniform(size=(n_examples, 2))

# make a true y
b = (xs>0.5).astype(int)
ys_true = np.logical_xor(b[:, 0], b[:, 1]).astype(int)



##################################
# here you implement a Decision Tree that is built using the fortuna algorithm.
# The depth of the tree should be less than 4
# The DT should reach 100% accuracy.


