import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the data from a file (assuming JSON format)
with open('traffic.jsonl', 'r') as f:
    data = [json.loads(line) for line in f.readlines()]

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Convert the time fields to datetime
df['depature'] = pd.to_datetime(df['depature'], format='%H:%M')
df['arrival'] = pd.to_datetime(df['arrival'], format='%H:%M')

# Calculate the duration in minutes
df['duration'] = (df['arrival'] - df['depature']).dt.total_seconds() / 60

# Create a scatter plot of departure time vs duration with route as color
# Create a scatter plot of departure time vs duration with route as color
scatter_fig = px.scatter(
    df[20:],
    x='depature',
    y='duration',
    color='road',
    title="Route Duration vs Departure Time by Road",
    labels={"depature": "Departure Time", "duration": "Duration (minutes)"}
)
# Display the scatter plot
scatter_fig.show()

# You could also create a histogram with route grouping
histogram_fig = px.histogram(
    df,
    x='duration',
    color='road',
    nbins=20,
    title="Distribution of Route Durations by Road",
    labels={"duration": "Duration (minutes)"}
)
histogram_fig.show()

# Line plot showing trends of departure time vs. duration
line_fig = px.line(
    df,
    x='depature',
    y='duration',
    color='road',
    title="Departure Time vs Route Duration",
    labels={"depature": "Departure Time", "duration": "Duration (minutes)"}
)
line_fig.show()

