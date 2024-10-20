import numpy as np


# TASK: Create a numpy array containing the whole numbers between 1, 10 (inclusive)
a = 1,2,3,4,5,6,7,8,9,10
assert isinstance(a, np.ndarray)
assert np.isclose(a, [1,2,3,4,5,6,7,8,9,10]).all()
print("<ok>")


#%%
# TASK: Reshape the array a so that it is a 2 by 4 array
import numpy as np

a = np.array(range(0, 8))

# -- CODE --
a = a.reshape(2,4)

assert( a.shape == (2,4) )
print("<ok>")
#%%
# TASK: multiply all the numbers in a by 2.
a = np.array([[1,2,3,4], [5,6,7,8]])
a= a*2
assert a.shape == (2,4)
assert a.sum() == 72
print("<ok>")
#%%
# TASK:  create a numpy array b that contains the sum of each row (axis 1) in a

a = np.array([[1,2,3,4], [5,6,7,8]])

# -- CODE --
b = a.sum(axis=1, dtype='float')

assert b.shape == (2,)
assert (b == [10, 26]).all()
print("<ok>")
#%%
# TASK:  create a numpy array b that contains the mean value of each column (axis 0) in a
a = np.array([[1,2,3,4], [1,2,3,8]])
b = np.mean(a, axis=0)
assert b.shape == (4,)
assert (b == [1, 2, 3, 6]).all()
print("<ok>")
#%%
# TASK:  multiply each number that is equal to 2 by 10
a = np.array([[1,2,3,4], [1,2,3,8]])

#b = np.where(a == 2, a * 10, a)

# -- CODE --
b = np.where(a == 2, a * 10, a)

a_after_mul = np.array([[1,20,3,4], [1,20,3,8]])
assert (a_after_mul == b).all()
print("<ok>")
#%%
# TASK:  stack the arrays a, b and c into an array called s (vertically)
# s should be equal to s_true (hint, look at the numpy function vstack )


a = np.array([1, 3])
b = np.array([2, 4])
c = np.array([3, 5])
s = np.vstack((a, b, c))
s_true = np.array([[1, 3], [2, 4], [3, 5]])
assert (s_true == s).all()
print("<ok>")
#%%
# TASK:  Flatten the array a into a 1d array called f (hint: numpy has a function named flatten)

a = np.random.randn(2,2,2)
print(a)
f = a.flatten()
print("-"*50)
print(f)
assert f.ndim == 1
print("<ok>")
