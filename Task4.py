import json
import os
import tempfile
import tqdm
import numpy as np
import plotly.express as px


def predict(x, theta):
    # change to sum of 3 sin() terms.
    # use np.sin() and not math.sin().
    # psi = høyde på kurven, gamma = frekvens, omega = faseskifte
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
    # L2 Loss funksjon.
    loss = ((y_hat - ys) ** 2).sum()
    return loss


def save_params(params_file, theta, loss, label='best_theta'):
    """Save the best parameters and the best mean squared error as a JSON file."""
    #print(f"Hurra!! Found a better model for {label} with loss: {loss}")

    data = {
        'best_theta': theta.tolist(),
        'best_loss': loss
    }
    with tempfile.NamedTemporaryFile('w', delete=False, dir='.') as tmpfile:
        json.dump(data, tmpfile)
        temp_name = tmpfile.name
    os.replace(temp_name, params_file)
   # print(f"Saved parameters to {params_file}")


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


def load_params(params_file):
    """Reads the JSON file containing the best parameters and the best mean squared error."""
    try:
        with open(params_file, 'r') as f:
            params = json.load(f)
            return params['best_theta'], params['best_loss']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not load parameters: {e}")
        return None, None


best_loss = float('inf')
best_theta = sample_theta(n_params)

loaded_theta, loaded_loss = load_params(params_file='best_theta.json')
if loaded_theta is not None and loaded_loss is not None:
    best_theta = np.array(loaded_theta)
    best_loss = loaded_loss

best_loss2 = float('inf')
best_theta2 = sample_theta(n_params2)

loaded_theta2, loaded_loss2 = load_params(params_file='best_theta2.json')
if loaded_theta2 is not None and loaded_loss2 is not None:
    best_theta2 = np.array(loaded_theta2)
    best_loss2 = loaded_loss2

learning_rate = 0.1

for _ in tqdm.tqdm(range(100000)):


    curr_theta = best_theta + sample_theta(n_params) * learning_rate
    y_hat = predict(xs, curr_theta)
    curr_loss = get_loss(y_hat, ys)

    curr_theta2 = best_theta2 + sample_theta(n_params2) * learning_rate
    y_hat2 = predict2(xs, curr_theta2)
    curr_loss2 = get_loss(y_hat2, ys_h)



    # If we find a better solution, update the best theta and reset improvement count
    if best_loss > curr_loss:
        best_loss = curr_loss
        best_theta = curr_theta
        print("New best_loss: ",best_loss)
        save_params(params_file = 'best_theta.json', theta=best_theta, loss=best_loss)

    if best_loss2 > curr_loss2:
        best_loss2 = curr_loss2
        best_theta2 = curr_theta2
        print("New best_loss2: ",best_loss2)
        save_params(params_file = 'best_theta2.json', theta=best_theta2, loss=best_loss2)
    # Gradually reduce learning rates
  #  learning_rate *= 0.9
print("Best Loss = ", best_loss)
print("Best Loss 2 = ", best_loss2)

fig = px.line(x=xs, y=ys, title="f(x) vs Fortuna solution")
fig.add_scatter(x=xs, y=predict(xs, best_theta), mode='lines', name="y_hat for predict")
fig.update_layout(xaxis_range=[xs.min(), xs.max()], yaxis_range=[-6, 6])
fig.show()

fig2 = px.line(x=xs, y=ys_h, title="f(x) vs Fortuna solution ys_h")
fig2.add_scatter(x=xs, y=predict2(xs, best_theta2), mode='lines', name="y_hat for predict2")
fig2.update_layout(xaxis_range=[xs.min(), xs.max()], yaxis_range=[-6, 6])
fig2.show()

# to get a solid estimate -> you should train at least 100 models and take the average performance.
