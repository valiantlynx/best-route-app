import numpy as np
import plotly.express as px


# Change this code into the correct Line Plot

xs = np.array([1, 1.5, 2, 2.5, 6.0])
ys = np.array([1, 2, 3, 3.1, 2.5])


fig = px.line(x=xs, y=ys, title="Line Plot")
fig.update_layout(xaxis_range=[0,8], yaxis_range=[0,4])
fig.show()
#%%
# Change this code into the correct Scatter Plot (please take care of the axis)

xs = np.array([1, 2, 3, 4, 5])
ys = np.array([1, 1, 2, 3, 5])


fig = px.scatter(x=xs, y=ys, title="Fibbonachi Scatter Plot")
fig.update_layout(xaxis_range=[0,6], yaxis_range=[0,10])
fig.show()