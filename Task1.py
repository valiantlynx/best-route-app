import numpy as np
import plotly.express as px

# Line Plot
# Plot the function f(x) = -0.69x^2 + 1.3x + 0.42 over the interval [0, 2.5], with 0.01 increments in x.
def f(x):
    return -0.69 * x ** 2 + 1.3 * x + 0.42


x_values = np.arange(0, 2.5, 0.1)
y_values = f(x_values)

fig = px.line(x=x_values, y=y_values, title="F(x)= -0.69x^2 + 1.3x + 0.42")
fig.show()

# Change this code into the correct Line Plot

xs = np.array([1, 1.5, 2, 2.5, 6.0])
ys = np.array([1, 2, 3, 3.1, 2.5])


fig = px.line(x=xs, y=ys, title="Line Plot")
fig.update_layout(xaxis_range=[0,8], yaxis_range=[0,4])
fig.show()
#%%
# Change this code into the correct Scatter Plot (please take care of the axis)
fib = [0,1]
n = 25
for i in range(2,n):
  fib.append(fib[i-1]+fib[i-2])

pairs = []

for i in range(n-1):
  pairs.append([fib[i],fib[i+1]])

pairs = np.array(pairs)

print("pairs 0", pairs[:,0])
print("pairs 1", pairs[:,1])

xs = np.array(pairs[:,0])
ys = np.array(pairs[:,1])


fig = px.scatter(x=xs, y=ys, title="Fibbonachi Scatter Plot")
fig.update_layout(xaxis_range=[0,pairs[:,0][-1] + 5000], yaxis_range=[0,pairs[:,1][-1] + 5000])
fig.show()