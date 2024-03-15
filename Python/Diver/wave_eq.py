import numpy as np
import matplotlib.pyplot as plt
import random


def generate_raindrop(x_range, y_range):
        # See if a drop needs to be placed
        if random.random() > 0.3:
            return 0, 0, 0, 0, 0
        
        print("Added raindrop")

        # Pick random coordinate
        # to place the raindrop
        x = int(random.random() * (x_range - 1))
        y = int(random.random() * (y_range - 1))
    
        # Randomly chose a droplet size
        size = int(random.random() * 3)
        x_end = x + size
        if (x_end  > x_range - 1):
             x_end = x_end - x - x
        y_end = y + size
        if (y_end > y_range - 1):
             y_end = y_end - y - y 
        
        # Randomly calculate an amplitude
        amplitude = random.random() * 1000
        return x, y, x_end, y_end, amplitude
        





x_range = 250
y_range = 250
t_range = 650
starting_condition = 1
c_starting_condition = 0.65 # Speed constant


# Create the empty field (array)
u = np.full((t_range, x_range, y_range), starting_condition)
c = np.full((x_range, y_range), c_starting_condition)

# Fill the arrays with starting conditions
u[0, int(random.random() * (x_range - 1)),  int(random.random() * (y_range - 1))] = 100
# c[0:int(x_range / 2), 0:y_range] = c_starting_condition / 10

# Plot the first frame
plt.ion()
fig, ax = plt.subplots()
img = ax.imshow(u[0])
plt.show()


# u(t + 1, x, y) = u''(t, x, y) + 2u(t, x, y) - u(t - 1, x, y)
# u''(t, x, y,) = c**2 * (u''x + u''y)
# u''x(t, x, y) = u(t, x + 1, y) - 2u(t, x, y) + u(t, x - 1, y)
# u''x(t, x, y) = u(t, x, y - 1) - 2u(t, x, y) + u(t, x, y - 1)

# Zodat:
# u(t + 1, x, y) = c**2 * (u(t, x + 1, y) + u(t, x - 1, y) + u(t, x, y + 1) + u(t, x, y - 1) - 4u(t, x, y)) + 2u(t, x, y) - u(t - 1, x, y)
# --  = c**2 * (A + B + C + D - 4E) + 2E - F

for t in range(1, t_range - 1):

    x, y, x_end, y_end, amplitude = generate_raindrop(x_range, y_range)
    if amplitude > 0:
        u[t, x:x_end, y:y_end] = amplitude

    A = u[t, 2:, 1:-1]
    B = u[t, :-2, 1:-1]
    C = u[t, 1:-1, 2:]
    D = u[t, 1:-1, :-2]
    E = u[t, 1:-1, 1:-1]
    F = u[t - 1, 1:-1, 1:-1]

    result = c[1:-1, 1:-1]**2 * (A + B + C + D - 4*E) + 2*E - F
    u[t + 1, 1:-1, 1:-1] = result
    print(t)
print("Done!")


# Update the plot after all values are initialized
for t in range(t_range):
    img.set_array(u[t])
    plt.pause(0.002)
    print("Showing...")


# Keep the plot open
plt.ioff()
plt.show()



