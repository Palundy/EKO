from MS import MS
from TMCL import TMCL
import numpy as np
import time
import csv
import matplotlib.pyplot as plt





# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM4", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)




def wait_until_stable(sensor_object: MS, threshold: float = 0.9, attempts: int = 5, measurement_amount: int = 35, window_size: int = 15):

    # Initialise the arrays
    I = np.array([], dtype=float) # Irradiances
    t = np.array([], dtype=float) # Time (s)
    D = np.array([], dtype=float) # Derivatives

    # Define the function to calculate
    # the mean based on `windowsize` amount of 
    # preceding values
    def calculate_mean_by_window(array, index, window_size):
        window_size = index if window_size > index else window_size
        return None if index > len(array)-1 else np.mean(array[index-window_size:index+1])


    # Retrieve the current time
    begin_time = time.time()


    # Count the amount of attempts 
    n_attempts = 0

    print("Detecting whether sensor is stable.")
    while n_attempts < attempts:

        print("")
        print(f"Attempt {n_attempts + 1}")
        
        # Count the amount of measurements
        n_measurements = 0
        while n_measurements < measurement_amount:

            # Retrieve the compensated irradiance
            comp_irr_ref = sensor_object.compensated_irradiance()
            # Capture the current time 
            #   this is explicity done after the sensor readouts
            #   because they have blocking behaviour
            current_time = time.time() - begin_time          

            
            # Add the irradiance and the timestamp
            # to the array
            I = np.append(I, comp_irr_ref)
            t = np.append(t, current_time)
            n_measurements += 1        

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
            mean = calculate_mean_by_window(D, k, window_size)

            # Check whether the mean is smaller or equal to the threshold
            if abs(mean) <= threshold:
                consecutive_values += 1
            else:
                consecutive_values = 0
            
            if consecutive_values == int(measurement_amount / 4):
                print("The sensor is stable.")
                return True
        


        # Resetting the time
        begin_time = time.time()
        current_time = time.time() - begin_time
        print("The sensor is not yet stable.")
        n_attempts += 1

    return False



print(wait_until_stable(ref_sensor))
