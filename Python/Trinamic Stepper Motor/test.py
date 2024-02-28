from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time

# Initialize a sensor on port COM5
addresses_used = []

# Connect with first sensor
sensor_0 = MS("COM5", -1, addresses_used)
addresses_used.append(sensor_0.modbus_address)

# Connect with second sensor
sensor_1 = MS("COM5", -1, addresses_used)
addresses_used.append(sensor_1.modbus_address)


# Measure every 1/`fraction`-th second for `duration` amount of seconds
fraction = 10
duration = 20
count = 0

# Arrange the time and voltage arrays
t = np.arange(0, duration, 1/fraction)  # sec
I_0 = np.zeros(len(t))                  # W/m²
I_1 = np.zeros(len(t))                  # W/m²


# Configure the plot
plt.ion()
figure, ax = plt.subplots()
line1, = ax.plot(t, I_0)
line2, = ax.plot(t, I_1)
ax.autoscale(enable = True, axis = 'y', tight = None) # Enable autoscaling of the y-axis


while count < (duration * fraction):

    # Read the output voltage value
    I_0[count:] = sensor_0.compensated_irradiance()
    I_1[count:] = sensor_1.compensated_irradiance()
    # I[count:] set's every value in the list the same as the last,
    # so that the graph will lead on the same height

    # Update the plot
    line1.set_xdata(t)
    line1.set_ydata(I_0)
    line2.set_xdata(t)
    line2.set_ydata(I_1)
    ax.relim()
    ax.autoscale_view()

    # Draw the updated values
    figure.canvas.draw()
    figure.canvas.flush_events()

    # Update the count
    count += 1
    time.sleep(1/fraction)
