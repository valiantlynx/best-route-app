import numpy as np
import plotly.express as px

# Line Plot
# Plot the function f(x) = -0.69x^2 + 1.3x + 0.42 over the interval [0, 2.5], with 0.01 increments in x.
def f(x):
    return -0.69 * x ** 2 + 1.3 * x + 0.42
x_values = np.arange(0, 2.5, 0.01)
y_values = f(x_values)
fig = px.line(x=x_values, y=y_values, title="F(x)= -0.69x^2 + 1.3x + 0.42")
fig.show()

#%%
# Change this code into the correct Scatter Plot (please take care of the axis)
fib = [0,1]
n = 25
for i in range(2,n+1):
    fib.append(fib[i-1]+fib[i-2])

xs = list(range(1, n + 2))
print(xs)

fig = px.scatter(x=xs, y=fib, title="Fibonacci Scatter Plot")
fig.show()