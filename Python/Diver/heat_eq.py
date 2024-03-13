import numpy as np
import matplotlib.pyplot as plt
import random

kappa = 384.1 # Thermal conductivity [W / m*K]
cp = 385 # Specific heat capacity [J / kg*K]
rho = 8850 # Density [kg / m^3]
alpha = kappa / (cp*rho) # Thermal diffusivity


        





x_range = 100
y_range = 100
t_range = 750
starting_condition = 10


# Create the empty field (array)
u = np.full((t_range, x_range, y_range), starting_condition)
alpha = np.full((x_range, y_range), alpha)



# Fill the arrays with starting conditions
u[0:5, 1:x_range - 1, 1:10] = 200

# Plot the first frame
plt.ion()
fig, ax = plt.subplots()
img = ax.imshow(u[0])
plt.show()

# u(t + 1, x, y) = u'(t, x, y) + u(t, x, y)

# u'(t, x, y,) = alpha * (u''x + u''y)
# u''x(t, x, y) = u(t, x + 1, y) - 2u(t, x, y) + u(t, x - 1, y)
# u''x(t, x, y) = u(t, x, y - 1) - 2u(t, x, y) + u(t, x, y - 1)

# Zodat:
# u(t + 1, x, y) = alpha * (u(t, x + 1, y) + u(t, x - 1, y) + u(t, x, y + 1) + u(t, x, y - 1) - 4u(t, x, y)) + u(t, x, y)
# --  = alpha * (A + B + C + D - 4E) + E

for t in range(1, t_range - 1):

    A = u[t, 2:, 1:-1]
    B = u[t, :-2, 1:-1]
    C = u[t, 1:-1, 2:]
    D = u[t, 1:-1, :-2]
    E = u[t, 1:-1, 1:-1]

    result = alpha[1:-1, 1:-1] * (A + B + C + D - 4*E) + E
    u[t + 1, 1:-1, 1:-1] = result
    print(t)
print("Done!")


# Update the plot after all values are initialized
for t in range(t_range):
    img.set_array(u[t])
    plt.pause(0.001)
    print("Showing")


# Keep the plot open
plt.ioff()
plt.show()



