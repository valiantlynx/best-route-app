# # Task 4 -- Revisit the Fortuna Algorithm
#
# Below is a implementation of Fortuna that uses fits linear function $f_{\theta} = a x + b$ where $\theta = \{a,b\}$ to a function $g(x)$.
# However, as is evidently from the graph, $g(x)$ is not a linear function.
#
# 1) Change the code to instead use $f_{\theta}(x) = \sum\limits_{k=1}^{3} \Psi_k \sin(\gamma_k (x + \omega_k)) $.
#   Such that $|\theta| = 9$, where each parameter $c$ in $\theta$ is in $[-4. 4]$.
# That is, $f_{\theta}(x)$ is a sum of three sin terms. **Do not change the range of the sample\_theta function.**
#
# 3) However, it seems Fortuna (on average) struggles to find the optimal parameters $\theta$.
# Therefore you will have to innovate and change the Fortuna algorithm so that it faster finds "better solutions".
# What changes did you make and **why** did you make them, and how did you measure how efficient these changes were?
# A excellent solution here will have an expected best loss of less than 5 using 100000 guesses. (take the average over 100 runs).
# **But ANY improvment is sufficient to pass!**
#
# 4) Using your newly made modified Fortuna Algorithm optimize the function: $h(x) = \mu - (\zeta sin(\kappa x) )  (\tau (x + \lambda))$ .
# The y values for this function can be found in the numpy array ys_h (in the code below).
# Does your new and improved Fortuna outperform the regular fortuna on this function as well? Why?
# **Remember to change your model to match $h(x)$**
#
#
# 4) [**Optional**] Develop a multiprocces implemention of the Fortuna algorithm using python's multiprocessing library (https://docs.python.org/3/library/multiprocessing.html).
# How are the speed ups? Are Fortuna really suited to parallel execution?
#





import random
import numpy as np
import plotly.express as px
import tqdm
from dask.array import average


def predict(x, theta):
    # change to sum of 3 sin() terms.
    # use np.sin() and not math.sin().
    #psi = høyde på kurven, gamma = frekvens, omega = faseskifte
    psi1, psi2, psi3, gamma1, gamma2, gamma3, omega1, omega2, omega3 = theta
    return (
            psi1 * np.sin(gamma1 * (x + omega1)) +
            psi2 * np.sin(gamma2 * (x + omega2)) +
            psi3 * np.sin(gamma3 * (x + omega3))
    )  # this is the model


def predict2(x, theta):
    # theta = [mu, k, tau, lambda]
    mu, k, tau, lam = theta  # renamed `lambda` to `lam` to avoid conflicts with the reserved keyword `lambda`
    return mu - (np.sin(k * x) * (tau * (x + lam)))

def sample_theta(size_of_theta):
    # Do NOT CHANGE.
    # Velger random theta verdi mellom -4 og 4.
    theta = np.random.uniform(-4, 4, size=size_of_theta)
    return theta


def get_loss(y_hat, ys):
    # No change needed, returns quadratic loss.
    #L2 Loss funksjon.
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
n_params = 9
n_params2 = 4

best_loss = float('inf')
best_theta = sample_theta(n_params)

best_loss2 = float('inf')
best_theta2 = sample_theta(n_params2)

# Incorporating momentum and step size reduction
learning_rate = 0.1
no_improvement_count = 0
max_no_improvement = 5000
iterations = 100
iter_best_losses = []
for i in range(iterations):
    i += 1
    for _ in tqdm.tqdm(range(100000)):
        if no_improvement_count > max_no_improvement:
            break
        # Sample theta near the current best theta
        curr_theta = best_theta + sample_theta(n_params) * learning_rate
        y_hat = predict(xs, curr_theta)
        curr_loss = get_loss(y_hat, ys)
        # If we find a better solution, update the best theta and reset improvement count
        if best_loss > curr_loss:
            best_loss = curr_loss
            best_theta = curr_theta
            no_improvement_count = 0
        else:
            no_improvement_count += 1

        last_100_best_loss = []
        last_100_best_loss.append(best_loss)
        if (_ % 100):
            best_loss = np.mean(last_100_best_loss)
            last_100_best_loss = []

        # Gradually reduce learning rate
        learning_rate *= 0.999

        curr_theta2 = sample_theta(n_params2)
        y_hat2 = predict2(xs, curr_theta2)
        curr_loss2 = get_loss(y_hat2, ys)

        if best_loss2 > curr_loss2:
            best_loss2 = curr_loss2
            best_theta2 = curr_theta2

    iter_best_losses.append(best_loss)

best_loss = np.mean(iter_best_losses)

print("best loss:", best_loss)
print("theta:", best_theta)

print("best loss2:", best_loss2)
print("theta2:", best_theta2)

fig = px.line(x=xs, y=ys, title="f(x) vs Fortuna solution")
fig = px.line(x=xs, y=ys_h, title="f(x) vs Fortuna solution ys_h")
fig.add_scatter(x=xs, y=predict(xs, best_theta), mode='lines', name="y_hat for predict")
fig.add_scatter(x=xs, y=predict2(xs, best_theta2), mode='lines', name="y_hat for predict2")
fig.update_layout(xaxis_range=[xs.min(), xs.max()], yaxis_range=[-6, 6])
fig.show()

# to get a solid estimate -> you should train at least 100 models and take the average performance.
