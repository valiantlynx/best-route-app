import numpy as np
import plotly.express as px

# Denne funksjonen henter bare 9 random verdier(parametere) mellom -4 og 4.
def sample_theta(size_of_theta):
    return np.random.uniform(-4, 4, size=size_of_theta)

# Denne funksjonen tar inn de gitte xs verdiene, og kalkulerer y_hat med de curr_theta (de 9 randomiserte verdiene) som er y verdiene til de gitte xs verdiene. Punktene vil bli (xs [0], y_hat [0])
def predict(x, theta):
    psi1, psi2, psi3, gamma1, gamma2, gamma3, omega1, omega2, omega3 = theta
    return (
        psi1 * np.sin(gamma1 * (x + omega1)) +
        psi2 * np.sin(gamma2 * (x + omega2)) +
        psi3 * np.sin(gamma3 * (x + omega3))
    )

# Denne funksjonen kalkulerer mse loss, ut ifra de y verdiene du har fått ved hjelp av de 9 random verdiene og de gitte ys verdiene, som er «løsningen».
# Losset sier noe om hvor god tilnærming vår predikerte modell til den faktiske modellen.
def get_loss(y_hat, ys):
    return ((y_hat - ys) ** 2).sum()

xs = np.array([1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1,
               2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3,
               3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5,
               4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7,
               5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9,
               7.0, 7.1, 7.2, 7.3, 7.4])
ys = np.array([4.03, 4.19, 4.26, 4.25, 4.17, 4.03, 3.85, 3.63, 3.4, 3.16,
               2.93, 2.72, 2.53, 2.39, 2.28, 2.21, 2.18, 2.19, 2.22, 2.27,
               2.33, 2.39, 2.44, 2.45, 2.43, 2.36, 2.22, 2.02, 1.75, 1.41,
               1.0, 0.52, -0.01, -0.6, -1.22, -1.86, -2.5, -3.13, -3.72,
               -4.27, -4.75, -5.15, -5.45, -5.65, -5.74, -5.7, -5.55, -5.29,
               -4.92, -4.44, -3.89, -3.26, -2.58, -1.86, -1.12, -0.39, 0.32,
               0.98, 1.6, 2.14, 2.61, 2.99, 3.28, 3.47, 3.57])

n_params = 9
num_restarts = 10
iterations_per_restart = 100000 // num_restarts

best_loss = float('inf')
best_theta = None


if __name__ == "__main__":

    for restart in range(num_restarts): #10 restarts som begynner på forskjellige punkter for å utforske bredere områder av theta
        best_restart_theta = sample_theta(n_params) # Lager 9 random parametere
        y_hat = predict(xs, best_restart_theta) # Predikerer y-verdier basert på de 9 random parametere
        best_restart_loss = get_loss(y_hat, ys) # Beregner loss fra de predikerte y-verdiene og løsningen

        for _ in range(iterations_per_restart): # 10 000 iterasjoner som utfører små justeringer for å finne en bedre løsning
            delta_theta = sample_theta(n_params) * 0.01 # Lager 1% av en ny random theta
            temp_theta = best_restart_theta + delta_theta # Tar current theta og plusser på delta_theta

            temp_theta = np.clip(temp_theta, -4, 4) # Sikrer at ingen av verdiene i theta går utenfor [-4, 4]
            temp_y_hat = predict(xs, temp_theta) # Predikerer y-verdier basert på vår nye midlertidige theta
            temp_loss = get_loss(temp_y_hat, ys) # Beregner midlertidig loss ut ifra de midlertidige predikerte y-verdiene

            # Update if a better loss is found
            if temp_loss < best_restart_loss: # Sjekker om den midlertidige lossen er mindre enn nåværende beste loss
                best_restart_theta = temp_theta # Setter best_restart_theta til temp_theta
                best_restart_loss = temp_loss # Setter til ny laveste loss, som tilhører ny beste theta

                if best_restart_loss < best_loss: # Hvis den nye beste lossen er bedre enn den nåværende beste loss
                    best_loss = best_restart_loss # Setter best loss til ny best loss
                    best_theta = best_restart_theta.copy() # Setter best theta til ny best theta

    print(f"Best Loss: {best_loss}")

    # Plotting
    fig = px.line(x=xs, y=ys, title="f(x) vs Improved Fortuna solution")
    fig.add_scatter(x=xs, y=predict(xs, best_theta), mode='lines', name="y_hat")
    fig.update_layout(xaxis_range=[xs.min(),xs.max()], yaxis_range=[-6,6])
    fig.show()
    # Kjør Task4ys_h for å se begge grafene.
    import Task4ys_h