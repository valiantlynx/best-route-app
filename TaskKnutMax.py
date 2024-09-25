import json
import random
from datetime import datetime, timedelta


# Read data from 'traffic.jsonl'
def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            data.append(record)
    return data


# Fortuna algorithm: Random routes within timewindow, which is input_time -> input_time +30min.
def fortuna_algorithm(routes, n_iterations):
    best_route = None
    best_travel_time = None

    for _ in range(n_iterations):
        # Randomly select a route from the list
        route = random.choice(routes)
        dep_time = datetime.strptime(route['depature'], "%H:%M")
        arr_time = datetime.strptime(route['arrival'], "%H:%M")
        travel_time = arr_time - dep_time

        # Update best route if this one is better
        if best_travel_time is None or travel_time < best_travel_time:
            best_travel_time = travel_time
            best_route = route

    return best_route, best_travel_time


# Function to implement the solution with n iterations
def get_the_best_route_as_a_text_informatic(dep_hour, dep_min, n_iterations=1000):
    data = read_data('traffic.jsonl')

    # Convert input departure time to a datetime object
    input_time = datetime.strptime(f"{dep_hour}:{dep_min}", "%H:%M")

    # Define departure time_window (input time to input time + 30 minutes)
    time_window_start = input_time
    time_window_end = input_time + timedelta(minutes=30)
    # Filter routes within the time window
    matching_routes = []
    for record in data:
        # Convert departure time string to datetime
        record_dep_time = datetime.strptime(record['depature'], "%H:%M")
        # Check if departure time is within the window
        if time_window_start <= record_dep_time <= time_window_end:
            matching_routes.append(record)

    # If no routes match, return a message
    if not matching_routes:
        return "No matching routes found for the given departure time."

    # Run Fortuna algorithm simulation
    best_route, best_travel_time = fortuna_algorithm(matching_routes, n_iterations)

    # Format the travel time
    hours, remainder = divmod(best_travel_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    best_time_formatted = f"{hours}h {minutes}m"

    # Return the results
    return {
        'best_time': best_time_formatted,
        'route': best_route['road'],
        'departure': best_route['depature'],
        'arrival': best_route['arrival']
    }

