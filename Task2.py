import numpy as np


def get_2polynomal_from_3_points(p0: np.array, p1: np.array, p2: np.array) -> np.array:
    pass

# -- CODE --


point0 = np.array([0.147, 0.596])
point1 = np.array([0.7, 0.992])
point2 = np.array([2.06, 0.17])

polynomial_coefficients = get_2polynomal_from_3_points(point0, point1, point2)
assert (polynomial_coefficients.shape[0] == 3 and polynomial_coefficients.ndim == 1)

print("Polynomial: {:2f}x^2 + {:.2f}x + {:.2f}".format(*polynomial_coefficients))

if not np.isclose(polynomial_coefficients[0], -0.69, atol=0.01):
    print("x^2 coeff is wrong (a), should be close to -0.69")

if not np.isclose(polynomial_coefficients[1], 1.3, atol=0.01):
    print("x coeff is wrong (b), should be close to 1.3")

if not np.isclose(polynomial_coefficients[2], 0.42, atol=0.01):
    print("Constant factor (c) is wrong, should be close to 0.42")

if np.isclose(polynomial_coefficients, [-0.69, 1.3, 0.42], atol=0.01).all():
    print("Correct polynomial found.")