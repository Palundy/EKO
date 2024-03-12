from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
import csv



# Initialize a sensor on port COM5
addresses_used = []

# Connect with first sensor
sensor_0 = MS("COM4", -1, addresses_used)
while (sensor_0.is_ready == False):
    time.sleep(1)
addresses_used.append(sensor_0.modbus_address)

x_begin = 1
x_max = 14
y_max = 21

x_factor = 2
y_factor = 2



# Open the .csv file
filename = "measurement_height_040_02.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)

    x = x_begin
    y = 1

    while True:


        coordinates = input(f"({x}, {y}) or type 'END' to finish: ")
        if coordinates == "END":
            break  # Break out of the loop to finish

        # Explode the coordinates
        coordinates = [x, y]
        irr = sensor_0.compensated_irradiance()
        coordinates.append(irr)

        print(f"I={irr} W/m²")
        writer.writerow(coordinates)
        
        y += 1 * y_factor
        if (y > y_max):
            x += 1 * x_factor
            y = 1
        if (x > x_max):
            break

        # Optional: Flush the file to ensure data is written.
        file.flush()

file.flush()
