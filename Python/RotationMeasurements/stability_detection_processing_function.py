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



def wait_until_irradiance_is_stable(sensor_object: MS, threshold: float = 1.5, attempts: int|bool = 5, measurement_amount: int = 30):

    print("Detecting whether sensor is stable.")

    # Initialise the arrays
    I = np.array([], dtype=float) # Irradiances
    t = np.array([], dtype=float) # Time (s)
    D = np.array([], dtype=float) # Derivatives


    # Retrieve the current time
    begin_time = time.time()

    # Count the amount of attempts 
    n_attempts = 0


    # Creating the conditional statement for the while-loop
    while_statement = n_attempts < attempts
    if n_attempts == False:
        while_statement = True


    while while_statement:

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

        
        # Calculate the derivative of each point (excluding the first value)
        D = (I[1:] - I[:-1]) / (t[1:] - t[:-1])

        # Check whether the signal is stable
        consecutive_values = 0
        for k in range(len(D) - 1):
            if abs(D[k]) <= threshold:
                consecutive_values += 1
            else:
                consecutive_values = 0
            
            if consecutive_values == int(1/2 * measurement_amount):
                print("The sensor is stable.")
                return True
            
        # Update the attempt count
        n_attempts += 1

        # Updating the conditional statement for the while-loop
        while_statement = n_attempts < attempts
        if attempts == False:
            while_statement = True

        print("The sensor is not yet stable.")

    return False



print(wait_until_stable(ref_sensor, 1.5, False))
