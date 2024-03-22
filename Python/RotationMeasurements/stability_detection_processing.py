from MS import MS
from TMCL import TMCL
import numpy as np
import time
import csv
import matplotlib.pyplot as plt


def mean_by_window(array, index, windowsize):
    if windowsize > index:
        windowsize = index

    if index > len(array)-1:
        return None
    
    return np.mean(array[index-windowsize:index+1])


# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM4", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)


# Set the amount of minutes
amount_of_minutes = .2

# Open the .csv file
begin_time = time.time()
current_time = time.time() - begin_time

# Initialise the arrays
I = np.array([], dtype=float) # Irradiances
t = np.array([], dtype=float) # Time (s)
D = np.array([], dtype=float) # Derivatives


i = 0
is_stable = False
threshold = 0.005
# Open the file
while i < 5:
    print("")
    print("Starting scan")
    j = 0
    while j < 30:

        # Retrieve the irradiances
        # of both the reference and test sensor
        comp_irr_ref = ref_sensor.compensated_irradiance()
        # Capture the current time 
        #   this is explicity done after the sensor readouts
        #   because they have blocking behaviour
        current_time = time.time() - begin_time
        print(comp_irr_ref, current_time)
        

        
        # Add the irradiance to the array
        I = np.append(I, comp_irr_ref)
        t = np.append(t, current_time)
        j += 1

    

    print("")
    print("Stopping scan and starting data evaluation")
    

    # Evaluate the data
    # Normalize the data
    norm_I = I - np.min(I)
    norm_I = norm_I / np.max(norm_I)
    
    # Calculate the derivative of each point (excluding the first value)
    D = (norm_I[1:] - norm_I[:-1]) / (t[1:] - t[:-1])

    # For every point, calculate the mean
    # and see if the mean falls under the threshold
    consecutive_values = 0
    for k in range(len(D)):
        mean = mean_by_window(D, k, 20)
        print(f"The mean is {mean}")

        if abs(mean) < threshold:
            consecutive_values += 1
        else:
            consecutive_values = 0
        
        if consecutive_values == 10:
            is_stable = True
            break
    
    if is_stable:
        # A stable point has been reached
        print("An equilibrium has been reached.")
        break


    # Resetting the time
    begin_time = time.time()
    current_time = time.time() - begin_time