import numpy as np
import plotly.express as px
from Task4 import sample_theta, get_loss, xs, num_restarts, iterations_per_restart


# Denne funksjonen tar inn de gitte xs verdiene og kalkulerer y_hat med de curr_theta (de 4 randomiserte verdiene) som er y verdiene til de gitte xs verdiene.
def predict2(x, theta):
    mu, k, tau, lam = theta
    return mu - (np.sin(k * x) * (tau * (x + lam)))

ys_h = np.array([15.98, 21.42, 24.1, 23.87, 21.0, 16.11, 10.06, 3.79, -1.8, -6.01, -8.39, -8.82, -7.47, -4.77, -1.3, 2.31, 5.49, 7.81, 9.04, 9.18, 8.44, 7.15, 5.72, 4.54, 3.89, 3.9, 4.52, 5.54, 6.63, 7.39, 7.49, 6.7, 4.97, 2.44, -0.54, -3.48, -5.8, -6.98, -6.61, -4.51, -0.79, 4.2, 9.8, 15.21, 19.57, 22.09, 22.2, 19.63, 14.52, 7.41, -0.83, -9.07, -16.11, -20.83, -22.36, -20.27, -14.59, -5.91, 4.72, 15.9, 26.06, 33.69, 37.58, 36.94, 31.64])

n_params2 = 4

best_loss_h = float('inf')
best_theta_h = None

# Restart loop to find the best solution
for restart in range(num_restarts):
    # Initial random parameters for ys_h
    best_restart_theta_h = sample_theta(n_params2) # Lager 4 random parametere for ys_h

    # Predictions and losses for ys_h
    y_hat_h = predict2(xs, best_restart_theta_h) # Predikerer y-verdier for ys_h basert på de 4 random parametere
    best_restart_loss_h = get_loss(y_hat_h, ys_h) # Beregner loss fra de predikerte y-verdiene for ys_h og løsningen

    for _ in range(iterations_per_restart):
        delta_theta_h = sample_theta(n_params2) * 0.01 # Lager 10% av en ny random theta for ys_h
        temp_theta_h = best_restart_theta_h + delta_theta_h # Tar current theta og plusser på delta_theta for ys_h
        temp_theta_h = np.clip(temp_theta_h, -4, 4) # Sikrer at ingen av verdiene i theta går utenfor [-4, 4]
        temp_y_hat_h = predict2(xs, temp_theta_h) # Predikerer y-verdier for ys_h basert på vår nye midlertidige theta
        temp_loss_h = get_loss(temp_y_hat_h, ys_h) # Beregner midlertidig loss ut ifra de midlertidige predikerte y-verdiene for ys_h

        if temp_loss_h < best_restart_loss_h: # Sjekker om den midlertidige lossen er mindre enn nåværende beste loss for ys_h
            best_restart_theta_h = temp_theta_h # Setter best_restart_theta_h til temp_theta_h
            best_restart_loss_h = temp_loss_h # Setter til ny laveste loss, som tilhører ny beste theta for ys_h

            if best_restart_loss_h < best_loss_h: # Hvis den nye beste lossen er bedre enn den nåværende beste loss for ys_h
                best_loss_h = best_restart_loss_h # Setter best loss_h til ny best loss for ys_h
                best_theta_h = best_restart_theta_h.copy() # Setter best theta_h til ny best theta for ys_h

print(f"Best Loss for ys_h: {best_loss_h}")

# Plotting the results for ys_h
fig = px.line(x=xs, y=ys_h, title="h(x) vs Improved Fortuna solution")
fig.add_scatter(x=xs, y=predict2(xs, best_theta_h), mode='lines', name="y_hat")
fig.update_layout(xaxis_range=[xs.min(),xs.max()], yaxis_range=[-6,6])
fig.show()