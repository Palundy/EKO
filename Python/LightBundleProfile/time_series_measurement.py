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


measurement_time = 20 * 60 # seconds
time_step = 0.4

begin_time = time.time()
current_time = time.time()


# Open the .csv file
filename = "time_measurement.csv"
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)

    while current_time - begin_time <= measurement_time:

        current_time = time.time()

        # Retrieve the compensated intensity
        compensated_intensity = sensor_0.compensated_irradiance()
        print(f"I = {compensated_intensity}")

        writer.writerow([current_time, current_time - begin_time, compensated_intensity])

        # Optional: Flush the file to ensure data is written.
        file.flush()
        time.sleep(time_step)
file.flush()
