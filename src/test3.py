import json
from datetime import datetime, timedelta
import random
import plotly.express as px

# Load traffic data from the JSONL file
with open('traffic.jsonl', 'r') as file:
    traffic_data = [json.loads(line) for line in file]


# Helper function to calculate travel time in minutes
def calculate_travel_time(departure, arrival):
    time_format = "%H:%M"
    departure_time = datetime.strptime(departure, time_format)
    arrival_time = datetime.strptime(arrival, time_format)

    # If arrival is the next day
    if arrival_time < departure_time:
        arrival_time += timedelta(days=1)

    return (arrival_time - departure_time).seconds / 60


# Helper function to calculate waiting time in minutes
def calculate_waiting_time(input_departure, actual_departure):
    time_format = "%H:%M"
    input_time = datetime.strptime(input_departure, time_format)
    actual_time = datetime.strptime(actual_departure, time_format)

    # If actual departure is earlier on the next day
    if actual_time < input_time:
        actual_time += timedelta(days=1)

    return (actual_time - input_time).seconds / 60


# Extract features (roads and time of departure) and observed outcomes (travel time)
xs = []
ys = []

for route in traffic_data:
    # Example feature: road and departure time as separate features
    road_feature = hash(route['road']) % 100  # Hash the road to a number for simplicity
    departure_time = datetime.strptime(route['depature'], "%H:%M").hour  # Hour of departure

    # Calculate the travel time in minutes
    travel_time = calculate_travel_time(route['depature'], route['arrival'])

    # Feature vector: road and departure time (two separate features)
    features = (road_feature, departure_time)
    xs.append(features)  # Store features
    ys.append(travel_time)  # Observed outcome: travel time


# Loss function (L2 loss)
def loss_function(ys, ys_hat):
    return sum((y - y_hat) ** 2 for y, y_hat in zip(ys, ys_hat))


# Define the model function (multivariable linear model)
def f(x, theta):
    a_road, a_time, c = theta
    return a_road * x[0] + a_time * x[1] + c


# Number of iterations for the Fortuna-like algorithm
N = 100000
best_loss = float('inf')
best_theta = None
best_loss_log = []

# Fortuna algorithm to find the best parameters
for n in range(N):
    # Randomly guess parameters (a_road, a_time, c)
    a_road = random.uniform(-10, 10)
    a_time = random.uniform(-10, 10)
    c = random.uniform(-100, 100)
    theta = (a_road, a_time, c)

    # Calculate the predicted outcomes (y_hat)
    ys_hat = [f(x, theta) for x in xs]

    # Calculate the loss (L2 loss)
    loss = loss_function(ys, ys_hat)

    # Keep track of the best parameters if the current loss is lower
    if loss < best_loss:
        best_loss = loss
        best_theta = theta

    best_loss_log.append(best_loss)

# Output the best parameters and corresponding loss
print(f"Best parameters: {best_theta}")
print(f"Best loss: {best_loss}")

# Plot the loss over iterations to show model improvement
fig = px.line(y=best_loss_log, labels={'y': 'Best Loss'}, title="Improvement of Route Selection Over Iterations")
fig.show()


# Function to select the best route based on input departure time
def find_best_route(input_departure, traffic_data, best_theta):
    best_route = None
    best_total_time = float('inf')

    for route in traffic_data:
        # Calculate waiting time
        waiting_time = calculate_waiting_time(input_departure, route['depature'])

        # Calculate travel time
        travel_time = calculate_travel_time(route['depature'], route['arrival'])

        # Calculate total time (waiting time + travel time)
        total_time = waiting_time + travel_time

        # Compare with predicted outcome from the model
        route_feature = (hash(route['road']) % 100, datetime.strptime(route['depature'], "%H:%M").hour)
        predicted_travel_time = f(route_feature, best_theta)

        # If total time is better, select this route
        if total_time < best_total_time:
            best_total_time = total_time
            best_route = {
                'road': route['road'],
                'depature': route['depature'],
                'arrival': route['arrival'],
                'total_time': total_time,
                'predicted_time': predicted_travel_time
            }

    return best_route


# Example: Input departure time
input_departure = "10:00"
best_route = find_best_route(input_departure, traffic_data, best_theta)
print(f"Best route based on input departure {input_departure}:")
print(f"Route: {best_route['road']}")
print(f"Depature: {best_route['depature']}")
print(f"Arrival: {best_route['arrival']}")
print(f"Total time (including waiting time): {best_route['total_time']} minutes")
print(f"Predicted travel time by the model: {best_route['predicted_time']} minutes")
