import matplotlib.pyplot as plt
import numpy as np
import time
import random



def second_derivative(current_val, prev_val, next_val):
    return next_val - 2 * current_val + prev_val


def next_val(second_derivative, current_val, prev_val):
    return second_derivative + 2 * current_val - prev_val


def raindrop_generator(raindrop_chance, max_x, max_y, max_amplitude, max_drop_size, raindrops_enabled):
    if random.random() > raindrop_chance or raindrops_enabled == False:
        return 0, 0, 0, 0, 0
    
    # Determine the drop size
    drop_size = int(random.random() * max_drop_size - 1) + 1
    
    # Generate random spot to put the raindrop
    x = int(random.random() * (max_x - 1))
    y = int(random.random() * (max_y - 1))
    x_end = x + drop_size
    y_end = y + drop_size


    # Generate random amplitude for the raindrop
    amplitude = int(random.random() * max_amplitude)
    return amplitude, x, y, x_end, y_end



time_steps = 250
x_range = 50
y_range = 50


speed_constant = 0.5
raindrop_chance = 0.07
max_amplitude = 100
max_drop_size = 4
raindrops_enabled = True

grid = np.zeros((time_steps, x_range, y_range))
speed_constants = np.ones((x_range, y_range)) * 0.5
grid[0][int(x_range / 2), int(y_range / 2)] = max_amplitude



for t in range(1, time_steps - 1):
    # if t == 0 or t == time_steps-1:
    #     continue

    # Generate a random raindrop
    amplitude, x, y, x_end, y_end = raindrop_generator(raindrop_chance, x_range, y_range, max_amplitude, max_drop_size, raindrops_enabled)
    if amplitude > 0:
        print(f"Raindrop: (x={x}, y={y}, a={amplitude})")
        grid[t][x:x_end, y:y_end] = amplitude


    x_values = np.arange(1, x_range - 1)
    y_values = np.arange(1, y_range - 1)

    x_2nd_deriv = second_derivative(grid[t, x_values, y_values], grid[t, x_values - 1, y_values], grid[t, x_values + 1, y_values])
    y_2nd_deriv = second_derivative(grid[t, x_values, y_values], grid[t, x_values, y_values - 1], grid[t, x_values, y_values + 1])
    t_2nd_deriv = speed_constants[x_values, y_values] ** 2 * (x_2nd_deriv + y_2nd_deriv)

    grid[t + 1, x_values, y_values] = next_val(t_2nd_deriv, grid[t, x_values, y_values], grid[t - 1, x_values, y_values])
    print(t)
    
    # for x in range(x_range):
    #     for y in range(y_range):
                        
    #         # See if this is a boundary value
    #         if x == 0 or x == x_range-1:
    #             continue
    #         if y == 0 or y == y_range-1:
    #             continue


    #         # Calculate the second derivative of u with respect to x
    #         # also for u with respect to y
    #         x_2nd_deriv = second_derivative(grid[t, x, y], grid[t, x - 1, y], grid[t, x + 1, y])

    #         y_2nd_deriv = second_derivative(grid[t, x, y], grid[t, x, y - 1], grid[t, x, y + 1])
            
    #         # Calculate the second derivative of u with respect to time
    #         t_2nd_deriv = speed_constants[x, y]**2 * (x_2nd_deriv + y_2nd_deriv)
            
    #         # Calculate the next value
    #         grid[t + 1, x, y] = next_val(t_2nd_deriv, grid[t, x, y], grid[t - 1, x, y])
            


# Showing the animation
# Update the canvas
while True:
    plt.ion()
    fig, ax = plt.subplots()
    img = ax.imshow(grid[0])
    plt.show()

    for t in range(time_steps):
        print(f"Updating plot (t={t})")
        img.set_array(grid[t])
        plt.pause(0.001)

    plt.ioff()
    plt.show()