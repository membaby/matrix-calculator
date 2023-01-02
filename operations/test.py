from matplotlib import pyplot as plt
import numpy as np

def fixpt(f, x, epsilon=1.0E-4, N=500, store=False):
    y = f(x)
    n = 0
    if store: Values = [(x, y)]
    while abs(y-x) >= epsilon and n < N:
        x = f(x)
        n += 1
        y = f(x)
        if store: Values.append((x, y))
    if store:
        return y, Values
    else:
        if n >= N:
            return "No fixed point for given start value"
        else: 
            return x, n, y

# define f
def f(x):
    return 0.2*x*x

# find fixed point
res, points = fixpt(f, 3, store = True)
print(points)

# create mesh for plots
xx = np.arange(0, 6, 0.1)

#plot function and identity
plt.plot(xx, f(xx), 'b')
plt.plot(xx, xx, 'r')

# plot lines
for x, y in points:
    print((x, y))
    plt.plot([x, x], [x, y], 'g')
    plt.plot([x, y], [y, y], 'g')

# show result
plt.show()