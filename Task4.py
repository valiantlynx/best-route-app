import random
import numpy as np
import plotly.express as px
import tqdm


def predict(x, theta):
    # change to sum of 3 sin() terms.
    # use np.sin() and not math.sin().
    a, b = theta
    return a * x + b  # this is the model


def sample_theta(size_of_theta):
    # Do NOT CHANGE.
    theta = np.random.uniform(-4, 4, size=size_of_theta)
    return theta


def get_loss(y_hat, ys):
    # No change needed, returns quadratic loss.
    loss = ((y_hat - ys) ** 2).sum()
    return loss


xs = np.array(
    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2,
     3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5,
     5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4])
ys = np.array(
    [4.03, 4.19, 4.26, 4.25, 4.17, 4.03, 3.85, 3.63, 3.40, 3.16, 2.93, 2.72, 2.53, 2.39, 2.28, 2.21, 2.18, 2.19, 2.22,
     2.27, 2.33, 2.39, 2.44, 2.45, 2.43, 2.36, 2.22, 2.02, 1.75, 1.41, 1.00, 0.52, -0.01, -0.60, -1.22, -1.86, -2.50,
     -3.13, -3.72, -4.27, -4.75, -5.15, -5.45, -5.65, -5.74, -5.70, -5.55, -5.29, -4.92, -4.44, -3.89, -3.26, -2.58,
     -1.86, -1.12, -0.39, 0.32, 0.98, 1.60, 2.14, 2.61, 2.99, 3.28, 3.47, 3.57])
ys_h = np.array(
    [15.98, 21.42, 24.1, 23.87, 21.0, 16.11, 10.06, 3.79, -1.8, -6.01, -8.39, -8.82, -7.47, -4.77, -1.3, 2.31, 5.49,
     7.81, 9.04, 9.18, 8.44, 7.15, 5.72, 4.54, 3.89, 3.9, 4.52, 5.54, 6.63, 7.39, 7.49, 6.7, 4.97, 2.44, -0.54, -3.48,
     -5.8, -6.98, -6.61, -4.51, -0.79, 4.2, 9.8, 15.21, 19.57, 22.09, 22.2, 19.63, 14.52, 7.41, -0.83, -9.07, -16.11,
     -20.83, -22.36, -20.27, -14.59, -5.91, 4.72, 15.9, 26.06, 33.69, 37.58, 36.94, 31.64])

# change to the size of theta ( 9 ) (for h(x) how many parameters does it have?)
n_params = 2

best_loss = float('inf')
best_theta = sample_theta(n_params)

for _ in tqdm.tqdm(range(100000)):
    curr_theta = sample_theta(n_params)
    y_hat = predict(xs, curr_theta)
    curr_loss = get_loss(y_hat, ys)

    if best_loss > curr_loss:
        best_loss = curr_loss
        best_theta = curr_theta

print("best loss:", best_loss)
print("theta:", best_theta)

fig = px.line(x=xs, y=ys, title="f(x) vs Fortuna solution")
fig.add_scatter(x=xs, y=predict(xs, best_theta), mode='lines', name="y_hat")
fig.update_layout(xaxis_range=[xs.min(), xs.max()], yaxis_range=[-6, 6])
fig.show()

# to get a solid estimate -> you should train at least 100 models and take the average performance.

